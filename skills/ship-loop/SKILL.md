---
name: ship-loop
description: "Ship a Linear issue end-to-end: take an issue link or ID and deliver a CI-green pull request without waiting to be nudged. Use when given an issue URL or identifier with instructions to ship, fix, implement, or 'pick this up' — even if the message is just the link — and again before claiming any work done, reviewed, or merge-ready. Not a review skill: for reviewing someone else's change, use basic-code-review or adversarial-code-review."
metadata:
  tags: "shipping delivery pipeline linear pull-request ci autonomy triage"
---

# Ship Loop

## Overview

Take a Linear issue and run the whole delivery pipeline: read the issue as the spec, implement, validate, gate the hand-off behind an adversarial review, open the PR, babysit CI to green, and finish without waiting to be nudged.

## Reading the issue

Fetch the issue with the Linear tools (`get_issue`, comments included) before touching code.

- **The issue is the spec.** The description plus its evidence — pasted transcripts, screenshots, logs, root-cause blocks, linked PRs — replaces prose requirements. Extract IDs, file:line chains, and repro steps from it before searching the codebase.
- **Comments are the changelog of intent.** Later comments override the description where they conflict. A "done when" list is the acceptance criteria; treat it as the checklist for finishing.
- **Prior art is the requirements doc.** A reference to an existing implementation ("like v1 had", a linked issue or PR) means: read that implementation first, mirror its pattern, fix the named flaw. Do not design greenfield.
- **Linked and blocking issues bound the scope.** Work scoped to a related issue stays there — note it, do not absorb it.
- If the issue does not name the target repo and it is not obvious from the evidence, that is the one thing worth a question; everything else you resolve yourself.

## The loop

1. **Claim it.** Move the issue to In Progress and assign yourself, so the board reflects reality while you work.
2. **Isolate.** Branch off the integration branch using the issue's git branch name (Linear provides one; it also makes Linear auto-link the PR). When you have the `task` tool (top-level sessions only) and the work splits cleanly, a child session with its own `repo`/`branch` is the parallel option; otherwise one branch in one sandbox is the default.
3. **Implement.** When a correction names one bad instance, sweep the repo for the whole class before continuing.
4. **Validate in the background.** Run the project's canonical validation (e.g. the full test suite) as a long-running command — anything over 60s runs in job mode automatically — and keep working while it runs.
5. **Adversarial review before hand-off.** Invoke the `adversarial-code-review` skill against your own change. Output numbered findings plus a merge-readiness verdict; fix what blocks.
6. **Open the PR** with `create_pull_request` (or `gh pr create`), using the repo's PR template when one exists. Reference the issue identifier in the title or body so Linear links it.
7. **Babysit CI.** Poll the PR's check runs (`inspect_pull_request` includes them, or `gh pr checks`) until every check concludes. A failing check is yours: read the failure log, distinguish your breakage from flakes or pre-existing failures, fix and push, and watch the next run. Re-run genuinely flaky checks once before investigating deeper. Do not report done, and do not ask for review, while CI is red or pending.
8. **Watch for review comments** and handle them without being asked. Resolve threads only after the fix is pushed and verified.
9. **Close the loop on the issue.** Comment on the Linear issue with the PR link, what shipped, and exact verification steps — a URL, a click path, or a paste-ready smoke prompt. Check every "done when" item; anything deliberately not done gets named there, not silently dropped. Move the issue to its review/done state per the team's flow.
10. **Deliverable = observable behavior.** Exit code 0 is not "done". If the user says it does not work, they are right — check which checkout and process are actually serving before re-arguing.

## Triage protocol

Number findings and open questions so the reply can be "fix 1–4". "Fix what's worth fixing" grants triage authority — use it, and say what you skipped.

## Momentum rules

- Keep going until the pipeline completes; do not pause for permission mid-route. When an action genuinely requires sign-off, raise a single `ask_approval` gate with the decision framed, then resume the moment it resolves.
- Complexity tripwire: a wrapper, a fallback, or a third variant appearing means stop and propose the simple fix-forward version instead.
- Answer a "why" question with the reason before taking any action.
- Corrected twice on the same class of mistake → propose an AGENTS.md/CLAUDE.md or memory rule that captures it.

## Cross-session handoff

When asked to describe a failure "for the implementer", emit a fix brief: symptom, root cause (file:line chain), proposed fix, risks, test plan — self-contained, ready to paste into a fresh session or a Linear comment.

## Related skills

- `adversarial-code-review` — the review gate in step 5; also the right skill when someone asks you to attack a change you didn't write.
- `basic-code-review` — the standard grading review; use it on other people's PRs when asked to "review", not to ship.
