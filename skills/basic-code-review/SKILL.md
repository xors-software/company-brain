---
name: basic-code-review
description: "Review a pull request and report only high-confidence issues. Use when asked to review a PR, code review a change, take a look at a diff, or give a second pass before merge — the 'Basic Code Review' preset routes here. Grades the change against repo guidance, obvious bugs, and git history. It does NOT attack the change; for 'tear this apart', 'red-team this', or 'try to break it', use adversarial-code-review instead."
metadata:
  tags: "code-review pull-request github quality confidence-scoring"
---

# Basic Code Review

## Overview

Review a pull request through five fixed lenses, score every candidate issue for confidence, and report only what survives a high bar. The goal is a short, trustworthy review — a senior engineer's pass, not a lint dump. Findings you post must be real, cited, and worth the author's time.

Run the lenses as **sequential passes yourself**. Do not depend on spawning subagents: in Valet, the `task` tool is unavailable inside child sessions, and this skill must work at any session depth.

## Procedure

Work through these steps in order. Make a todo list from them first.

### 1. Eligibility check

Do not review if the PR is (a) closed, (b) a draft, (c) not in need of review (automated PRs like dependency bumps, or trivially obvious changes), or (d) already reviewed by you and unchanged since. Fetch state with the GitHub plugin's `inspect_pull_request` (includes files, comments, and check runs) or `gh pr view`. If ineligible, stop and say why.

### 2. Locate agent-instruction files

Find the repo's agent guidance: **`AGENTS.md` or `CLAUDE.md`, whichever the repo uses** (some repos have both; some symlink one to the other). Collect the root file plus any in directories the PR touches. List the paths — you will read them during the compliance pass and cite them in findings.

### 3. Summarize the change

Read the PR description and diff (`inspect_pull_request` with `includePatch`, or `gh pr diff`). Write a two-to-three-sentence summary of what the change does and why, so later passes judge findings against intent.

### 4. Five review passes

Run each lens as its own pass over the diff. Record every candidate issue with the lens that flagged it.

1. **Instruction-file compliance.** Check the changes against each AGENTS.md/CLAUDE.md collected in step 2. These files guide code *authoring*, so not every rule applies at review time — flag only rules the diff plainly violates.
2. **Shallow bug scan.** Read the file changes and look for obvious bugs in the changed lines themselves. Do not chase context beyond the diff. Large bugs only; skip nitpicks.
3. **Historical context.** Read `git blame` and the history of the modified code. Flag changes that contradict the reason the old code was written the way it was.
4. **Prior PR feedback.** Look at previous pull requests that touched these files and check whether review comments on them apply to this PR too.
5. **In-code guidance.** Read the code comments in the modified files and verify the changes comply with any guidance stated there.

### 5. Score each candidate

Score every candidate issue 0–100 for confidence that it is real. Re-examine the code while scoring — do not score from memory. Use this rubric verbatim:

- **0:** Not confident at all. This is a false positive that doesn't stand up to light scrutiny, or is a pre-existing issue.
- **25:** Somewhat confident. This might be a real issue, but may also be a false positive. You weren't able to verify it. If the issue is stylistic, it is one not explicitly called out in the relevant instruction file.
- **50:** Moderately confident. You verified this is a real issue, but it might be a nitpick or rarely happen in practice. Relative to the rest of the PR, it's not very important.
- **75:** Highly confident. You double-checked and it is very likely a real issue that will be hit in practice. The existing approach is insufficient. It directly impacts functionality, or is directly named in the relevant instruction file.
- **100:** Absolutely certain. You double-checked and confirmed a real issue that will happen frequently in practice. The evidence directly confirms it.

For issues flagged by the compliance lens, verify the instruction file actually calls out that specific rule before scoring above 25.

### 6. Filter

Drop every issue scoring below 80. If nothing remains, the review reports no issues — that is a valid, useful outcome. Do not lower the bar to have something to say.

### 7. Re-check eligibility, then post

Repeat the step 1 check (the PR may have closed or changed while you worked). Then post the review on the PR:

- **Preferred:** the GitHub plugin's `github.create_review` with `updateExisting: true`, so a re-run replaces your prior review instead of stacking a new one. Use `github.create_comment` when a plain comment fits better.
- **Fallback:** `gh pr comment`.

## Review provenance

Every review that an agent posts to GitHub must end with a short `Review provenance` section. Summarize the human's questions by theme. Use no more than a few bullets, even when the review followed a long conversation.

Separate the baseline request from directed questions when useful. The baseline pass is expected work, while directed questions show the human's concerns.

```markdown
### Review provenance

Human asked about:
- <brief summary of the baseline request and directed questions>
- <another theme, if needed>

Answered by: <model> via <harness>
Reviewed commit: `<full 40-character SHA>`
```

Provenance applies only to the named SHA. If the branch moves, treat prior answers as advisory.

### Posting identity

Post automated reviews with the GitHub App or organization identity by default. The provenance section carries the human's questions without implying human sign-off.

A human can use their own identity when they run an agent locally, check its output, and vouch for the review. Otherwise, use the App identity.

## Output format

Keep it brief, no emojis, cite everything. Follow this shape, then append the required `Review provenance` section:

```
### Code review

Found 2 issues:

1. <brief description> (AGENTS.md says "<quoted rule>")

<link to file and lines>

2. <brief description> (bug: <file and snippet>)

<link to file and lines>
```

Or, when nothing survived the filter:

```
### Code review

No issues found. Checked for bugs and instruction-file compliance.
```

Code links must use the full 40-char commit SHA, literally, in the form `https://github.com/<owner>/<repo>/blob/<full-sha>/<path>#L<start>-L<end>` — shell substitution like `$(git rev-parse HEAD)` will not render. Include at least one line of context on each side of the flagged lines.

## False positives — do not report these

- Pre-existing issues on lines the PR did not modify
- Something that looks like a bug but isn't
- Pedantic nitpicks a senior engineer wouldn't raise
- Anything a linter, typechecker, compiler, or CI would catch (imports, type errors, formatting). Do not run builds or typechecks yourself; CI covers that.
- General quality wishes (test coverage, documentation) unless the repo's instruction file explicitly requires them
- Rules the code explicitly silences (e.g. a lint-ignore comment)
- Functionality changes that are clearly intentional parts of the broader change

## Gotchas

- The five lenses are passes *you* run sequentially. Do not spawn subagents for them; `task` is unavailable in Valet child sessions and the skill must work everywhere.
- Do not build, typecheck, or run the test suite. This review is judgment on the diff; CI owns build signal.
- "No issues found" beats a padded review. The 80-point bar is the point of the skill.

## Related skills

- `adversarial-code-review` — when the request is to attack the change rather than grade it ("tear this apart", "what breaks in prod"). This skill confirms a change looks right; that one assumes it is wrong and hunts for proof.
