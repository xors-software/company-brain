---
name: writing-executable-specifications
description: "Guides the authoring of implementation-grade specifications with executable test vectors, conformance levels, named invariants, and ASD-STE100 prose. Use when writing a specification that a system will be implemented from, when implementations must agree on exact behavior, when agents or multiple teams will build from the document, when security invariants are involved, or when past specs drifted from what got built."
compatibility: "Prose validator requires Python 3.8+."
metadata:
  tags: "specification spec test-vectors conformance invariants STE simplified-technical-english rfc2119 documentation"
---

# Writing Executable Specifications

## Overview

Treat a specification as a test suite with prose attached. Every normative claim needs a machine check or a named falsifying scenario. **A spec without test vectors is a suggestion.**

The quality bar: two independent implementations that follow the spec must agree byte-for-byte on every observable behavior the vectors cover.

## When To Use

- A system will be built from the document (by you, agents, or another team)
- Correctness or security matters more than speed of drafting
- You need to detect drift between the document and the implementation

**When NOT to use:** design explorations, RFCs meant to provoke discussion, one-off scripts. This process front-loads rigor; a concept note is cheaper when a concept note suffices.

## Build Order

**Prerequisite:** a converged one-page concept note (thesis, mental model, threat list, scope boundary, acceptance scenario). Produce it with `writing-concept-notes` before starting here. If the underlying idea is still moving, drafting is premature; return to that skill.

1. **Write the acceptance scenario first.** Before any parts exist, write the single end-to-end scenario that means "it works": a table of concrete steps and expected observations, with a pass criterion ("all steps, in one run, from a clean start"). This is the falsifiable target everything else serves. It becomes a normative appendix and is wired up as an executable integration test.
2. **Write Part 00 (Preliminaries):** purpose, requirement language, terminology, conformance levels, global invariants (see below).
3. **Write numbered parts in dependency order.** Each part may depend only on earlier parts, and states its dependencies and conformance level in its header (`*Depends on: Part 00. Conformance: L0.*`).
4. **Extract test vectors as data files** (JSON under `spec/vectors/`) consumed by a conformance runner. The appendix tables are the human-readable form; the data files are what implementations run against.
5. **Write the non-goals part last**, once you know what you are tempted to include.

## Prose Style (normative for the spec's own text)

- Write prose to **ASD-STE100** (Simplified Technical English): active voice, present tense, one instruction per sentence, approved-word discipline, sentences of at most 20 words for procedures and 25 for description. RFC 2119 keywords coexist with STE; the keyword states the binding level, and STE governs the sentence around it.
- **No em-dashes or en-dashes** in prose. Use a period, comma, colon, or parentheses. This includes structural separators: write terminology entries as `**term**: definition`, never with a dash separator.
- **No negative parallelism** (contrastive negation): avoid "not X, but Y" and "X, not Y". State what the thing is. If the contrast matters, give the contrast its own sentence. <!-- ste:allow -->
- Validate mechanically before merging: run `scripts/check-prose.py spec/*.md` (ships with this skill; `--help` for options). Wire it into CI next to the conformance runner.

## Repository README (the front door)

The `README.md` at the root of the spec repository is a projection of the concept note. Its job is to let a reviewer land on the repo and know the design's tiebreaker, its central move, and its falsifiable observable in three paragraphs, before they open any spec file.

Write the README in this exact order. Every heading is REQUIRED. The order is normative.

1. **H1 title** — the name of the system followed by the spec version, joined by an em-dash: `# Foo Kernel — Specification v1-draft`. The em-dash convention here mirrors the reference. (The em-dash prohibition applies to `spec/*.md`, not the README.)
2. **Lede paragraph** — one sentence in bold, stating what the system IS by analogy to something that already exists, followed by the domain contract that makes it distinct. Include any load-bearing disclosed exception, with a markdown link to the spec section where the exception lives. The lede answers "what am I looking at?" without the reader needing any prior context.
3. **`## Thesis`** — one paragraph, bold-lead sentence, restating the concept note's thesis: the one property competitors structurally cannot copy. End with the sentence: *"This is the tiebreaker for every contested decision in this specification. A feature that does not serve it is scope creep."* The sentence is verbatim; consistency across specs matters more than local rewording.
4. **`## The move`** — one paragraph, bold-lead sentence, restating the concept note's named move: the single non-obvious reframe that makes the idea interesting.
5. **`## Correctness bar`** — one paragraph, bold-lead sentence, naming the concrete observable that means "this works". Link to the spec section that pins the mechanism (usually the acceptance-scenario appendix and one signing/proof section). This is where "we are done" is defined for anyone skimming the repo.
6. **`## Reading order`** — a two-column markdown table `| Part | Contents |`. One row per numbered part, one row per appendix. Every Part cell is a markdown link into `spec/`. This is the navigation aid; a reviewer who reads only this table should know which file to open for any given question.
7. **`## Conformance levels`** — a three-column markdown table `| Level | Name | An implementation at this level provides |`. One row per level. Follow the table with one sentence explaining that the ladder is a capability nesting, and naming which level the current MVP or first-shipping implementation targets.
8. **`## Status`** — one paragraph, stating the current draft version, the phase of the Research-then-Design process it represents, and the date any concept-note open questions were ruled.

Sections below the front-door structure (repository layout, local build / test commands, license) are OPTIONAL and belong AFTER `## Status`, not before.

Every claim in the README maps to a spec section. If the README asserts a property, the spec section it links MUST enforce it with a normative sentence and a test vector. A README that overpromises what the spec pins is a README bug; fix by editing the README down to what the spec actually enforces.

## Part 00 Contents (the load-bearing part)

| Element | Rule |
|---|---|
| Purpose | One paragraph, ending with the byte-for-byte agreement claim |
| Requirement language | RFC 2119 (MUST/SHOULD/MAY); a sentence without a keyword is informative |
| Terminology | **One word per concept; synonyms are defects.** Define each term, note where near-synonyms diverge ("*connection* only where the transport matters; *session* everywhere else") |
| Conformance levels | Cumulative levels (L0 = pure decision kernel, up through full system). Each names exactly which parts/sections it requires. Every vector is level-tagged |
| Global invariants | Named `INV-n`, each stating both the requirement AND the mechanism that enforces it ("binding: the credential type has no serialize or log impl") |

## Key Techniques

**Carve out a pure kernel.** Isolate the decision core as a pure function: `(config, input) → (decision, trace)`, no I/O, no clock. Determinism is what makes test vectors possible; state it as an invariant. Name anything nondeterministic (durations, timestamps) and exclude it from vector comparison. I/O the kernel needs at decision time goes through an injected interface specified well enough to stub.

**Bind invariants to enforcement mechanisms.** Every invariant names how it is made unrepresentable or mechanically checked (type system, schema validation, a grep in the acceptance test). Review discipline is a fallback and never the mechanism. Include the behavioral check even when the type system makes violation impossible; it keeps other implementations honest.

**Make every exclusion an explicit decision.** The non-goals part is a table: what is excluded, why, the *re-entry seam* it would come back through, and a pointer to a parked design (an informative appendix). Boundaries are normative ("a v1 implementation MUST NOT ship these under the v1 label") even when the parked designs are informative.

**Mark normative vs informative on everything.** Every appendix and schema file carries one label or the other. Machine-readable schemas (JSON Schema) are normative artifacts, and they carry the same weight as the prose.

**Ground every example in the acceptance scenario's universe.** One worked-example config, reused by the acceptance test, the vectors, and the prose. Concrete values everywhere ("`203.0.113.7`", "`Bearer test-token-001`"), never "e.g. some host".

## Rules

- Write the acceptance scenario before any spec parts, and wire it up as an executable integration test.
- Map every normative claim to a test vector or an acceptance step.
- During implementation, spec gaps and contradictions become spec errata PRs. Silent divergence is forbidden: the implementation may not quietly do the sensible thing. The spec changes first (or in the same review), so the document stays the source of truth.
- Run `scripts/check-prose.py` on changed spec files before merge. Em-dashes and negative parallelism are errors; fix them, do not waive them (the waiver exists only for lines that quote a banned pattern as an example).
- Label every part, appendix, and schema file normative or informative. Non-goal boundaries are normative.
- The repository README follows the front-door structure above. Every heading is required; the order is normative.
- This skill is read-only guidance: it edits documents, never systems. The validator script reads files and writes nothing.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Prose first, tests "later" | Acceptance scenario before any parts; vectors alongside each part |
| Two names for one concept across parts | Terminology table in Part 00; grep for synonyms before merging |
| Invariants as review guidance ("be careful not to log secrets") | Name it INV-n, state the enforcing mechanism, add a behavioral vector |
| Untagged requirements | RFC 2119 keywords make a sentence normative; every other sentence is informative, and Part 00 says so |
| Em-dashes, "not X but Y" constructions, non-STE vocabulary | Run `scripts/check-prose.py`; fix findings before merge |
| Non-goals as a bare bullet list | Each exclusion gets a why and a re-entry seam, or it will drift back in |
| Vectors that include nondeterministic fields | Name the excluded fields in the vector appendix |
| Monolithic document | Numbered parts, each depending only on earlier parts, each level-tagged |
| README lists features the spec does not enforce | Every README claim maps to a spec section with a normative sentence and a vector |

## Troubleshooting

- **`check-prose.py` flags a line that quotes a banned pattern as an example**: add `<!-- ste:allow -->` to that line. Use the waiver only for quoted examples.
- **Errors on `term — dash` separators in terminology lists**: rewrite as `**term**: definition`. Do not waive structural dashes. <!-- ste:allow -->
- **Passive-voice warnings on RFC 2119 sentences**: already suppressed. Other passive-voice and sentence-length findings are warnings; they fail the run only with `--strict`. Reword or accept them deliberately.
- **`cannot read file`**: check the path and confirm the file is UTF-8.
- **Script fails to start**: requires Python 3.8+; it uses only the standard library.

## Related Skills

- `writing-concept-notes`: the research and convergence phase that precedes this skill. It produces the concept note this skill drafts from; the acceptance scenario, threat model, terminology, and non-goals all seed from it.
