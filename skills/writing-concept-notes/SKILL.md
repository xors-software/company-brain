---
name: writing-concept-notes
description: "Guides the research and convergence phase that precedes a specification: compressing a raw idea into a one-page concept note with a named thesis, a borrowed mental model, a threat list, a deliberately narrow scope, and a falsifiable acceptance scenario. Use when an idea for a system exists only as a riff, voice memo, transcript, or braindump, when deciding whether an idea is ready to specify, or when spec drafting keeps churning because the underlying idea is still moving."
metadata:
  tags: "research concept-note thesis convergence scope acceptance-test threat-model ideation specification pipeline"
---

# Writing Concept Notes

## Overview

A spec is a set of decisions. The document is a projection of the decisions. This skill covers the phase that generates candidate decisions and kills the bad ones cheaply, before any spec prose exists. The deliverable is a **one-page concept note** that states the thesis, the wedge, and the deliberately narrow scope.

The discipline has two halves. Keep the idea moving until you have pressure-tested it. Stop the idea from moving before you start drafting. Writing prose before the decisions are stable means spending all your effort rewriting prose.

You are not writing the spec in this phase. You are earning the right to write it. The spec-drafting phase is a separate skill: `writing-executable-specifications`.

## When To Use

- An idea exists only as a riff, voice memo, meeting transcript, or rant
- You are deciding whether an idea deserves a full specification
- A spec draft keeps churning and you suspect the underlying decisions are still moving
- A project needs a thesis and scope boundary before a team or agent starts building

**When NOT to use:** the concept is already converged and documented (go straight to `writing-executable-specifications`), or the work is a small change to an existing system whose thesis is settled.

## The Concept Note (the deliverable)

One page, containing all of:

| Element | What it is |
|---|---|
| One-liner | What it is, in one sentence, by analogy to something that already exists |
| The move | The single non-obvious reframe that makes the idea interesting, named explicitly |
| Thesis | The one property competitors structurally cannot copy |
| Mental model | The proven system this design generalizes, and what it inherits from it |
| Threat list | The enumerated hard problems and failure modes |
| Scope | "Scope for v1 (deliberately narrow)", with explicit exclusions |
| Acceptance scenario | The concrete end-to-end scenario that means "this works" |

## Method

### 1. Capture the raw riff verbatim, then compress

Write the unpolished idea down before you clean it up. Then compress to two artifacts:

- **The one-liner**: what it is, in one sentence, using an analogy to something that already exists ("a package manager, but for datasets").
- **The move**: the single non-obvious reframe that makes the idea interesting. Example: "stop treating the dashboard as the product; the dashboard is one view over a queryable event log." Every good spec has exactly one of these. Find it and name it.

### 2. Find the thesis

Ask: what is the one property this design has that competitors structurally cannot copy? Example: offline verifiability (any consumer can check an artifact's integrity without contacting the publisher, so no vendor can revoke access). The thesis becomes the name, the README's first line, and the tiebreaker for every later design decision. A feature that does not serve the thesis is scope creep.

### 3. Steal the mental model from something proven

Do not invent a new conceptual universe. Find the closest well-understood system and generalize it. Example: "a package registry, generalized from code artifacts to datasets." This does three things:

- Makes the design tractable: you inherit the proven system's answers to hard problems (versioning, dependency resolution, lockfiles)
- Makes it explainable: everyone already knows the source system
- Gives you a ready-made correctness bar ("does the same lockfile reproduce the same bytes?")

### 4. Enumerate the hard problems as a threat model, early

Before drafting, list what could go wrong: history rewrite, unauthorized mutation, fabrication, key loss, disclosure beyond scope, regulatory conflict. This list becomes a spec appendix later. Doing it now means every design decision in the drafting phase can point at the threat it mitigates. A spec whose decisions do not map to threats is decoration.

### 5. Cut scope violently

The last section of the concept note is "Scope for v1 (deliberately narrow)". Example: "Spec v1 exists to enable ONE MVP implementation, no more. Local demo only. Federation explicitly out of scope." A cut feature may return later; that return is a deliberate, dated decision made from a stable base. The rule: **you can always add scope later from a stable base; you cannot finish an unbounded first draft.**

### 6. Write the acceptance test before the spec

Define the concrete end-to-end scenario that means "this works": a short ordered list of steps with observable outcomes (publish, fetch, verify, the tamper-detection path, the offline path, and so on). This is the single most valuable artifact of the phase. It converts a vibe into a falsifiable target, and it later becomes the executable integration test in the spec. **If you cannot write the acceptance test, you do not understand the idea yet. Stay in this phase.**

## Exit Criteria

All of the following, on roughly one page:

- A one-liner with an analogy
- A named move
- A named thesis
- A stolen mental model
- A threat list
- An explicit scope boundary with exclusions
- A concrete acceptance scenario

Only then start drafting, using `writing-executable-specifications`.

## Rules

- Hold a hard boundary between phases. Do not draft spec prose during research. When spec drafting reveals a decision still moving, stop, say so out loud, and return to this skill.
- The thesis is the tiebreaker. Every contested decision resolves toward the property nobody else can claim.
- Record reversals loudly. Keep a project hub note with a dated correction banner when a decision changes ("the name is settled, the repo is pushed"). Never silently edit a settled decision; future readers need both the current state and the fact that it changed.
- Capture the raw riff before compressing it. Compression discards information; keep the original.
- Every element of the concept note is required. A missing acceptance scenario or threat list means the phase is not done.
- This skill is read-only guidance: it produces documents and edits nothing else.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Drafting spec parts "while researching" | Stop. Finish the concept note first; prose written on moving decisions gets rewritten |
| A thesis that reads as a feature list | Reduce until one property remains that competitors structurally cannot copy |
| Inventing a novel conceptual universe | Generalize the closest proven system instead; inherit its answers |
| Threat model deferred to "after the design" | Enumerate threats now so each later decision can name the threat it mitigates |
| Scope defined by enthusiasm | Scope for v1 enables one implementation; everything else is an explicit exclusion |
| Vague acceptance criteria ("it should feel fast") | Ordered concrete steps with observable outcomes, executable later |
| Silently reversing an earlier decision | Dated correction banner in the project hub note |

## Troubleshooting

- **Cannot find "the move"**: re-read the raw riff and look for the sentence where the idea diverges from the obvious approach. If every sentence is obvious, the idea may be a feature; give a feature a ticket and skip the spec.
- **Cannot write the acceptance scenario**: the idea is not understood yet. Pick the smallest end-to-end path a demo would walk and write only that. If it still will not come, keep researching.
- **Two candidate mental models**: write the acceptance scenario in both vocabularies and keep the model that inherits more answers to your threat list.
- **Scope keeps growing during review**: every "what about X" gets one line in the exclusions with a reason, and the scope section stays one paragraph.
- **The note exceeds one page**: you are drafting, and the extra material belongs in the spec. Cut the note back to the seven elements.

## Related Skills

- `writing-executable-specifications`: the drafting phase that consumes the concept note. Its acceptance-scenario appendix, threat-model appendix, terminology, and non-goals part are seeded directly from the concept note's elements.
