---
name: writing-guidelines
description: "Use when writing, rewriting, or auditing any human-facing prose: specs, runbooks, READMEs, PR descriptions, release notes, error messages, UI copy, Slack messages, emails, issue comments. Triggers include AI tells or slop, text flagged as robotic or AI-generated, disorganized or inconsistent structure, buried warnings, verbose or promotional prose, uncertainty about how formal or strict the writing should be, or a request to humanize, de-slop, simplify, or apply STE/plain-language rules. Not for code, identifiers, command syntax, or marketing copy with a deliberate distinct voice."
---

# Writing guidelines

Combines Simplified Technical English rigor (lintable rules, sentence limits) with a catalog of AI writing patterns to detect and remove.

**Core principle: preserve the information, not the shape.** Every fact, requirement, warning, command, link, and caveat in the source survives into the rewrite. Structure, order, formatting, and phrasing do not have to. When keeping the information and keeping the original's shape pull in different directions, the information wins.

## Choose a register

Pick by what the text is for, not where you happen to be writing it. Apply per part when a document mixes registers (a procedure pasted into Slack gets full STE for the steps and humanized prose around them).

| Signal | Register |
|---|---|
| Tells a reader what to do, and a misreading has real cost: procedures, runbooks, safety text, error messages, spec normative text | **Full STE** |
| Durable reference prose someone will read later: READMEs, API docs, design docs, release notes, PR descriptions, spec narrative | **Modified STE** |
| Ephemeral or conversational: Slack, chat, email to colleagues, issue comments, standup notes | **Humanized** |

**Full STE.** Instructions at 20 words or fewer, descriptions at 25 or fewer. One instruction per sentence. Condition before action. No contractions, no semicolons. Numbered lists for sequences.

**Modified STE.** All the language rules below, but vary sentence length for flow, allow contractions when they match the voice, and let paragraphs breathe.

**Humanized.** Remove AI patterns only. Skip the sentence limits and word substitutions that would make a chat message sound stiff: contractions, fragments, and casual phrasing are the correct register here, and flattening them into procedure-speak is its own kind of tell. Keep the author's natural voice; still cut em dashes, sycophancy, filler, signposting, and AI vocabulary, and still never invent facts.

When unsure between two registers, ask what a misreading costs. High cost pushes up a tier; a Slack message explaining a production rollback still gets its steps written in full STE.

## Restructure when the structure is wrong

You are expected to redraft, reorder, merge, split, and delete, not just polish sentences in place. Rewrite from a blank page when the source is disorganized. Restructure whenever you see:

- A condition, prerequisite, or warning placed after the action it governs. Move it before the action, or reference it from the step it protects.
- Sections in an order that fights the reader's task (prerequisites after steps, rollback constraints after the conclusion).
- `**Bold Label:** content that restates the label` lists. Collapse to plain prose or a plain list.
- Formulaic sections that exist for shape, not content ("Challenges and Future Prospects", generic conclusions, a one-line paragraph restating its heading). Cut them, or keep only the concrete facts inside.
- Uniform paragraph depth. Compress the dull parts; dwell where the reader needs detail.

Original formatting earns preservation only when it serves the reader. "It's the established formatting" is not a reason to keep an AI-shaped structure. AI-shaped structure is a tell, the same as AI-shaped vocabulary. The author's voice is worth preserving; the template a chatbot poured the content into is not.

## Workflow

1. Read the full source. Build an inventory: facts, numbers, requirements, warnings, commands, links, caveats.
2. Choose the register (per part if mixed).
3. Assess the structure against the list above. Decide what to keep, reorder, or redraft.
4. Rewrite in the selected register, applying the language rules below.
5. Scan for AI patterns using [references/ai-patterns.md](references/ai-patterns.md). Fix every cluster.
6. Self-audit: answer "what still reads as AI-generated?" and "does the rewrite state any fact, name, number, or date not in the source?" Fix what you find.
7. Lint: `python3 scripts/prose_lint.py path/to/draft.md`. Inspect each finding; fix real violations. The linter is a diagnostic, not a certification: code samples and deliberate choices create false positives, and in the humanized register the contraction and sentence-length counts are expected, not violations.
8. Diff your inventory from step 1 against the rewrite. Restore anything lost.
9. Deliver only the requested artifact unless asked for an audit.

## Language rules

**Words.** One name for one thing, one meaning per word. Short common words: `use` not `utilize`, `start` not `commence`, `help` not `facilitate`. Cut marketing adjectives (`seamless`, `robust`, `powerful`, `cutting-edge`) and AI-frequency words (`delve`, `pivotal`, `tapestry`, `testament`, `underscores`, `showcases`, `vibrant`, `landscape` as abstraction). Keep necessary technical terms; define unfamiliar ones at first use.

**Actors and actions.** Active voice when the actor is known. A verb for an action: `analyze the log`, not `perform an analysis of the log`. Simple copulas: `is`/`has`, not `serves as`/`boasts`. Keep passive voice only when the actor is unknown or irrelevant.

**Sentences and structure.** One topic per paragraph, at most six sentences. Sentence-case headings. No em or en dashes anywhere. Replace each with a period, comma, colon, or parentheses. Straight quotes.

**Substance.** Never invent facts, numbers, quotes, sources, or examples. Never drop caveats, limitations, or warnings to shorten text. Say what isn't known or cut the sentence; never dress a guess as fact. Don't flatten a real author's voice into generic corporate prose, and don't add personality where neutral prose is correct.

## Final check

- Does every sentence add information or direct an action?
- Is the register right for what the text is for?
- Is every condition and warning positioned before what it governs?
- Did every fact, constraint, and warning from the inventory survive?
- Any surviving AI cluster: bold-label lists, rule-of-three, `-ing` tack-ons, negative parallelism, generic conclusion, em dashes, Title Case?
- In full STE, does any sentence exceed its length limit? In humanized, does anything sound like a procedure that shouldn't?

This skill improves form. It cannot make weak ideas true or unsupported claims credible.
