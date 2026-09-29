#!/usr/bin/env python3
"""Report mechanical STE plain-language and AI-writing-pattern signals.

Checks STE plain-language rules plus AI writing patterns: AI-frequency
vocabulary, negative parallelism, inline-header
lists, Title Case headings, curly quotes, and chat artifacts.
"""

from __future__ import annotations

import glob
import json
import os
import re
import sys

MARKETING = [
    "seamless",
    "seamlessly",
    "robust",
    "powerful",
    "cutting-edge",
    "effortless",
    "effortlessly",
    "world-class",
    "next-generation",
    "revolutionary",
    "blazing",
    "lightning-fast",
    "elegant",
    "delightful",
    "best-in-class",
    "state-of-the-art",
    "game-changing",
    "first-class",
    "battle-tested",
    "enterprise-grade",
    "supercharge",
    "unlock",
    "unleash",
    "empower",
    "empowers",
    "stunning",
    "breathtaking",
    "renowned",
    "must-visit",
    "nestled",
    "vibrant",
]
BANNED = [
    "commence",
    "commences",
    "commencing",
    "initiate",
    "initiates",
    "utilize",
    "utilizes",
    "utilizing",
    "leverage",
    "leverages",
    "leveraging",
    "facilitate",
    "facilitates",
    "ensure",
    "ensures",
    "ensuring",
    "prior to",
    "subsequent to",
    "obtain",
    "obtains",
    "acquire",
    "acquires",
    "demonstrate",
    "demonstrates",
    "additionally",
    "furthermore",
    "moreover",
    "comprehensive",
    "comprehensively",
    "utilization",
    "aforementioned",
    "henceforth",
    "therein",
    "whilst",
    "amongst",
    "numerous",
    "myriad",
    "plethora",
    "in order to",
    "a variety of",
    "in the event that",
    "due to the fact that",
    "it is important to note",
]
AI_VOCAB = [
    "delve",
    "delves",
    "delving",
    "tapestry",
    "testament",
    "pivotal",
    "crucial",
    "interplay",
    "intricate",
    "intricacies",
    "showcase",
    "showcases",
    "showcasing",
    "underscore",
    "underscores",
    "underscoring",
    "foster",
    "fosters",
    "fostering",
    "garner",
    "garners",
    "enduring",
    "boasts",
    "stands as",
    "serves as a",
    "evolving landscape",
    "indelible",
    "groundbreaking",
]
PHRASAL = [
    "spin up",
    "spin down",
    "reach out",
    "dive into",
    "dives into",
    "diving into",
    "kick off",
    "kicks off",
    "roll out",
    "rolls out",
    "tear down",
    "ramp up",
    "circle back",
    "drill down",
    "spun up",
    "reaching out",
]
MODAL_HEDGE = [
    "it is important to note",
    "it should be noted",
    "it is worth noting",
    "it's worth noting",
    "please note that",
    "as mentioned",
    "as noted above",
]
CHAT_ARTIFACT = [
    "i hope this helps",
    "let me know if",
    "would you like",
    "want me to",
    "great question",
    "you're absolutely right",
    "let's dive in",
    "let's dive into",
    "let's explore",
    "let's break this down",
    "here's what you need to know",
    "without further ado",
    "exciting times lie ahead",
    "the future looks bright",
    "the real question is",
    "at its core",
    "here's the thing",
]
BE = r"(?:am|is|are|was|were|be|been|being)"
IRREGULAR_PARTICIPLE = (
    r"(?:done|made|sent|read|built|kept|held|set|put|run|written|shown|given|"
    r"taken|found|got|gotten|seen|known|thrown|drawn)"
)
MINOR_HEADING_WORDS = {
    "a", "an", "and", "as", "at", "but", "by", "for", "in", "nor", "of",
    "on", "or", "per", "the", "to", "via", "vs", "with",
}


def strip_code(text: str) -> str:
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    return re.sub(r"`[^`]*`", " ", text)


def sentences(text: str) -> list[str]:
    output: list[str] = []
    for line in text.splitlines():
        sentence = line.strip()
        if not sentence:
            continue
        sentence = re.sub(r"^\s*#{1,6}\s*", "", sentence)
        sentence = re.sub(r"^\s*(?:[-*+]|\d+[.)])\s+", "", sentence)
        if not sentence:
            continue
        parts = re.split(r"(?<=[.!?:])\s+(?=[A-Z0-9\"'\-])", sentence)
        output.extend(part.strip() for part in parts if part.strip())
    return output


def word_count(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'\-/]*", text))


def count_phrases(text: str, phrases: list[str]) -> tuple[int, list[str]]:
    count = 0
    hits: list[str] = []
    lowered = text.lower()
    for phrase in phrases:
        matches = list(
            re.finditer(r"(?<![a-z])" + re.escape(phrase) + r"(?![a-z])", lowered)
        )
        count += len(matches)
        hits.extend(phrase for _ in matches)
    return count, hits


def title_case_headings(raw: str) -> int:
    count = 0
    for line in raw.splitlines():
        match = re.match(r"^\s*#{1,6}\s+(.*)$", line)
        if not match:
            continue
        words = [w for w in re.findall(r"[A-Za-z][A-Za-z'\-]*", match.group(1))]
        if len(words) < 3:
            continue
        capitalized = [
            w for w in words[1:]
            if w[0].isupper() and w.lower() in MINOR_HEADING_WORDS
        ]
        if capitalized:
            count += 1
    return count


def inline_header_bullets(raw: str) -> int:
    return len(
        re.findall(r"^\s*(?:[-*+]|\d+[.)])\s+\*\*[^*\n]+:\*\*", raw, re.M)
    ) + len(
        re.findall(r"^\s*(?:[-*+]|\d+[.)])\s+\*\*[^*\n]+\*\*:", raw, re.M)
    )


def lint(text: str) -> dict[str, object]:
    raw = text
    text = strip_code(text)
    parsed_sentences = sentences(text)
    words = sum(word_count(sentence) for sentence in parsed_sentences) or 1
    long_sentences = [
        (word_count(sentence), sentence)
        for sentence in parsed_sentences
        if word_count(sentence) > 20
    ]
    violations: dict[str, int] = {
        "long_sentence(>20w)": len(long_sentences),
        "semicolon": text.count(";"),
        "contraction": len(
            re.findall(r"\b\w+['’](?:t|re|ve|ll|d|m)\b", text)
        ),
        "passive_voice": len(
            re.findall(
                rf"\b{BE}\s+(?:\w+ed|{IRREGULAR_PARTICIPLE})\b", text, re.I
            )
        ),
        "ing_main_verb": len(re.findall(rf"\b{BE}\s+\w+ing\b", text, re.I)),
        "nominalization": len(
            re.findall(
                r"\b(?:perform(?:s|ed)?|conduct(?:s|ed)?|"
                r"carry out|carries out|make use of|makes use of)\b",
                text,
                re.I,
            )
        )
        + len(re.findall(r"\b\w{4,}(?:tion|ment|ance|ence)\s+of\b", text, re.I)),
        "negative_parallelism": len(
            re.findall(
                r"\bnot (?:just|only|merely)\b[^.!?\n]*\bbut\b", text, re.I
            )
        )
        + len(re.findall(r"\bit(?:'s| is) not (?:just |merely )?about\b", text, re.I)),
        "ing_tack_on": len(
            re.findall(
                r",\s+(?:highlighting|underscoring|emphasizing|ensuring|"
                r"reflecting|symbolizing|showcasing|fostering|cultivating|"
                r"encompassing|contributing to)\b",
                text,
                re.I,
            )
        ),
    }
    violations["phrasal_verb"], _ = count_phrases(text, PHRASAL)
    violations["banned_word"], banned_hits = count_phrases(text, BANNED)
    violations["marketing_adjective"], marketing_hits = count_phrases(text, MARKETING)
    violations["ai_vocabulary"], ai_hits = count_phrases(text, AI_VOCAB)
    violations["modal_hedge"], _ = count_phrases(text, MODAL_HEDGE)
    violations["chat_artifact"], _ = count_phrases(text, CHAT_ARTIFACT)
    violations["title_case_heading"] = title_case_headings(raw)
    violations["inline_header_bullet"] = inline_header_bullets(raw)
    violations["curly_quote"] = len(re.findall(r"[“”‘’]", strip_code(raw)))
    violations["emoji"] = len(
        re.findall(r"[\U0001F300-\U0001FAFF✅❌✨⚠]", raw)
    )
    paragraphs = [p for p in re.split(r"\n\s*\n", raw) if p.strip()]
    violations["long_paragraph(>6s)"] = sum(
        1 for paragraph in paragraphs if len(sentences(strip_code(paragraph))) > 6
    )
    total = sum(violations.values())
    longest_sentence = max(
        (word_count(sentence) for sentence in parsed_sentences), default=0
    )
    return {
        "words": words,
        "sentences": len(parsed_sentences),
        "violations": violations,
        "total": total,
        "total_per100w": round(total * 100.0 / words, 2),
        "em_dash(hard-fail)": raw.count("—") + raw.count("–") + raw.count(" -- "),
        "longest_sentence_words": longest_sentence,
        "sample_marketing": list(dict.fromkeys(marketing_hits))[:6],
        "sample_banned": list(dict.fromkeys(banned_hits))[:6],
        "sample_ai_vocab": list(dict.fromkeys(ai_hits))[:6],
    }


def main(arguments: list[str]) -> int:
    verbose = "-v" in arguments or "--verbose" in arguments
    arguments = [a for a in arguments if a not in ("-v", "--verbose")]
    if not arguments:
        print(json.dumps(lint(sys.stdin.read()), indent=2))
        return 0

    paths: list[str] = []
    for argument in arguments:
        if any(character in argument for character in "*?["):
            paths.extend(sorted(glob.glob(argument)))
        else:
            paths.append(argument)

    for path in paths:
        with open(path, encoding="utf-8") as handle:
            result = lint(handle.read())
        if verbose:
            print(os.path.basename(path))
            print(json.dumps(result, indent=2))
        else:
            print(
                f"{os.path.basename(path):32} "
                f"words={result['words']:4d} "
                f"total={result['total']:3d} "
                f"per100w={result['total_per100w']:6.2f} "
                f"em_dash={result['em_dash(hard-fail)']:2d}"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
