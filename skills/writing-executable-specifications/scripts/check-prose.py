#!/usr/bin/env python3
"""Validate specification prose against the skill's style rules.

Checks (see SKILL.md, "Prose Style"):
  errors   - em/en dashes; negative parallelism ("not X but Y", "X, not Y")
  warnings - non-STE vocabulary; sentences over the STE length limit;
             passive voice; lowercase RFC 2119 keywords

Fenced code blocks, inline code spans, table rows, headings (length check
only), and YAML frontmatter are skipped. Waive a single line by putting
`<!-- ste:allow -->` anywhere on it.

Exit status: 1 if any errors (or, with --strict, any warnings), else 0.
"""

import argparse
import re
import sys

# Non-STE vocabulary -> suggested replacement. Curated subset of common
# offenders; extend per project.
STE_WORDS = {
    r"utili[sz]e": "use",
    r"commence": "start",
    r"terminate": "stop / end",
    r"prior to": "before",
    r"subsequent(?:ly| to)": "after / then",
    r"in order to": "to",
    r"leverage": "use",
    r"facilitate": "help / enable",
    r"via": "through / with",
    r"etc\.": "list all items",
    r"e\.g\.": "for example",
    r"i\.e\.": "that is",
    r"ensure": "make sure",
    r"approximately": "about",
    r"additionally": "also",
    r"whilst": "while",
    r"upon": "on / when",
    r"in the event (?:that|of)": "if",
}

RFC2119 = r"(?:must(?: not)?|shall(?: not)?|should(?: not)?|may|required|recommended|optional)"

# "not X but Y" and "X, not Y" within one sentence.
CONTRASTIVE = [
    (re.compile(r"\bnot\b[^.;:!?]{1,60}\bbut\b", re.I), 'negative parallelism ("not X but Y")'),
    (re.compile(r",\s*not\b", re.I), 'negative parallelism ("X, not Y")'),
    (re.compile(r"\brather than\b", re.I), 'contrastive "rather than"'),
    (re.compile(r"\binstead of\b", re.I), 'contrastive "instead of"'),
]

PASSIVE = re.compile(r"\b(?:is|are|was|were|be|been|being)\s+(?:\w+ly\s+)?\w+(?:ed|wn|en)\b")
LOWER_KEYWORD = re.compile(r"(?<![A-Za-z])(must(?: not)?|shall(?: not)?|should(?: not)?)(?![A-Za-z])")

INLINE_CODE = re.compile(r"`[^`]*`")
WAIVER = "<!-- ste:allow -->"


def strip_frontmatter(lines):
    if lines and lines[0].strip() == "---":
        for i, line in enumerate(lines[1:], start=1):
            if line.strip() == "---":
                return [""] * (i + 1) + lines[i + 1:]
    return lines


def prose_lines(lines):
    """Yield (lineno, text, is_heading) for prose lines only."""
    in_fence = False
    for n, raw in enumerate(lines, start=1):
        stripped = raw.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or WAIVER in raw:
            continue
        if stripped.startswith("|"):  # table row
            continue
        yield n, INLINE_CODE.sub("`code`", raw), stripped.startswith("#")


def sentences(paragraph):
    """Split a paragraph into sentences, tolerant of abbreviations we check anyway."""
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+(?=[A-Z`\"'(])", paragraph) if s.strip()]


def check_file(path, max_words, findings):
    try:
        lines = open(path, encoding="utf-8").read().splitlines()
    except OSError as exc:
        findings.append((path, 0, "error", f"cannot read file: {exc}"))
        return
    lines = strip_frontmatter(lines)

    # Line-level checks.
    para, para_start = [], None
    paragraphs = []  # (start_lineno, text, is_heading)
    for n, text, is_heading in prose_lines(lines):
        for ch, name in (("—", "em-dash"), ("–", "en-dash")):
            if ch in text:
                findings.append((path, n, "error", f"{name}: use period, comma, colon, or parentheses"))
        is_list_item = bool(re.match(r"\s*(?:[-*+]|\d+\.)\s", text))
        if is_heading or not text.strip():
            if para:
                paragraphs.append((para_start, " ".join(para)))
                para, para_start = [], None
            continue
        if is_list_item and para:  # each list item is its own paragraph
            paragraphs.append((para_start, " ".join(para)))
            para = []
        if not para:
            para_start = n
        para.append(text.strip())
    if para:
        paragraphs.append((para_start, " ".join(para)))

    # Sentence-level checks.
    for start, text in paragraphs:
        for sent in sentences(text):
            for rx, msg in CONTRASTIVE:
                if rx.search(sent):
                    findings.append((path, start, "error", f"{msg}: {sent[:80]}"))
            for rx, repl in STE_WORDS.items():
                if re.search(rf"\b{rx}", sent, re.I):
                    word = re.search(rf"\b{rx}", sent, re.I).group(0)
                    findings.append((path, start, "warning", f'non-STE word "{word}": prefer "{repl}"'))
            words = len(re.findall(r"[A-Za-z0-9'`-]+", sent))
            if words > max_words:
                findings.append((path, start, "warning",
                                 f"sentence has {words} words (STE limit {max_words}): {sent[:80]}"))
            if PASSIVE.search(sent) and not re.search(RFC2119, sent):
                findings.append((path, start, "warning", f"possible passive voice: {sent[:80]}"))
            m = LOWER_KEYWORD.search(sent)
            if m:
                findings.append((path, start, "warning",
                                 f'lowercase requirement keyword "{m.group(1)}": uppercase it or reword'))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+", help="markdown files to check")
    ap.add_argument("--max-words", type=int, default=25,
                    help="STE sentence length limit (20 procedural, 25 descriptive; default 25)")
    ap.add_argument("--strict", action="store_true", help="treat warnings as errors")
    ap.add_argument("--no-warnings", action="store_true", help="report errors only")
    args = ap.parse_args()

    findings = []
    for path in args.files:
        check_file(path, args.max_words, findings)

    errors = 0
    for path, line, level, msg in findings:
        if level == "warning" and args.no_warnings:
            continue
        if level == "error" or args.strict:
            errors += 1
        print(f"{path}:{line}: [{level}] {msg}")

    total_warn = sum(1 for f in findings if f[2] == "warning")
    print(f"\n{sum(1 for f in findings if f[2] == 'error')} error(s), {total_warn} warning(s)", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
