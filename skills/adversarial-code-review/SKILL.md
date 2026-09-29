---
name: adversarial-code-review
description: "Attack a change and try to prove it wrong. Use when asked to tear a PR apart, red-team a diff, try to break a change, find what will blow up in prod, or stress a change before a risky merge. Assumes the diff is broken and hunts for the proof: missed edge cases, unhandled errors, security holes, broken invariants, untested paths. NOT for a standard review grade — 'review this PR' routes to basic-code-review instead."
metadata:
  tags: "code-review adversarial red-team pull-request security edge-cases"
---

# Adversarial Code Review

## Overview

This review does not grade the change; it attacks it. Start from the assumption that **the diff is wrong** — an edge case is missed, an error path is unhandled, an invariant is silently broken — and work to find the proof. Success is a concrete failure scenario, not a list of observations. If you genuinely cannot break it after a real attempt, that is the finding: say what you attacked and why it held.

The output contract matters as much as the hunt: numbered findings so the author can reply "fix 1–4", each finding anchored to a failure scenario, and a merge-readiness verdict at the end.

## Procedure

### 1. Understand the change and its blast radius

Read the PR description and full diff (`inspect_pull_request` with `includePatch`, or `gh pr diff`). Then read *around* the diff: the callers of changed functions, the consumers of changed data shapes, the config that gates the code path. The attack surface is the changed behavior, not the changed lines.

### 2. Attack through named lenses

Work through each lens deliberately. For each, actively try to construct a failure, not just note a smell:

- **Edge cases** — empty, zero, negative, maximum, unicode, concurrent, duplicate. What input did the author not think about?
- **Error paths** — what happens when the network call fails, the row is missing, the JSON doesn't parse? Is the failure handled, swallowed, or does it corrupt state?
- **Security** — injection, authz checks skipped on the new path, secrets in logs, trust of client-supplied data.
- **Broken invariants** — what did the old code guarantee that the new code no longer does? Check callers that relied on the guarantee.
- **Untested paths** — which branches of the new code does no test exercise? An untested error branch is a standing target.
- **What breaks in prod** — scale, retries, partial deploys, backwards compatibility with in-flight data, migrations racing traffic.

### 3. Prove findings by execution when you can

You have a sandbox with a shell. A demonstrated failure outranks a suspected one:

- Write and run a minimal repro (a failing test, a script poking the edge case) to confirm a suspected break.
- Feed the actual weird input to the actual function.
- If a repro attempt shows the code handles the case fine, the finding dies — kill it rather than reporting a hunch.

Label each surviving finding **demonstrated** (you ran it) or **suspected** (reasoned but not executed). Time-box repro attempts; a lens with a clear failure scenario you couldn't wire up to run still counts as suspected.

### 4. Report: numbered findings + verdict

Number every finding. Each one states a concrete failure scenario: the inputs or state, the path taken, and the wrong outcome. Vague unease ("this feels fragile") is not a finding.

End with a **merge-readiness verdict**, one of:

- **Do not merge** — at least one demonstrated or high-confidence break.
- **Merge after fixes** — name which finding numbers block.
- **Merge-ready** — the attack failed; say what you attacked and why it held.

### 5. Triage protocol

The numbered list is the interface for follow-up:

- A reply like "fix 1–4" means fix exactly those.
- "Fix what's worth fixing" grants triage authority: use your judgment, fix the ones that matter, and **say explicitly which findings you skipped and why**.
- When a fix for one finding reveals the same flaw elsewhere, sweep the repo for the whole class before reporting done.

## Output format

```
### Adversarial review

1. [demonstrated] <failure scenario: given <input/state>, <path> produces <wrong outcome>>
   <file link / repro command>

2. [suspected] <failure scenario>
   <file link>

Verdict: Merge after fixes — findings 1 and 2 block.
Attacked but held: <lenses/scenarios that didn't break, one line each>
```

Post to the PR with `github.create_review` (or `github.create_comment`); fall back to `gh pr comment`. When the review was requested conversationally rather than on a PR, report in the session instead. For every review posted to GitHub, append the `Review provenance` section and follow the posting-identity rules in `basic-code-review`.

## Gotchas

- **Do not soften into a normal review.** Style, naming, and documentation are out of scope here. If the request was actually "review this PR", hand off to `basic-code-review`.
- **Findings without failure scenarios are noise.** Every item needs inputs/state → wrong outcome. If you can't articulate the scenario, you haven't found anything yet.
- **"It held" is a real result.** Reporting zero findings after a genuine attack, with the attack documented, is a successful adversarial review — never invent findings to fill the list.
- **Pre-existing weaknesses** are in scope only when the diff makes them reachable or worse; say so explicitly when you include one.
- Run repros in the sandbox, not against shared/production systems.

## Related skills

- `basic-code-review` — the grading counterpart: five fixed lenses, confidence scoring, high-bar filtering. Use it when the request is a standard review; use this skill when the request is to break the change.
