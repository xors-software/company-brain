---
name: writing-brain-skills
description: "Use when creating a new skill, editing an existing skill, or reviewing a skill before it ships. Covers the Agent Skills file format (SKILL.md frontmatter, folder layout, progressive disclosure), how to write a description that triggers reliably, when to bundle scripts, and the effective-instruction patterns (gotchas, checklists, defaults-not-menus, validation loops). Use even when the request says 'turn this runbook into a skill', 'standardize this process', 'write a SKILL.md', or 'make this reusable', without naming the format."
metadata:
  tags: "skills authoring skill-md agent-skills frontmatter description progressive-disclosure scripts"
---

# Writing skills

## Overview

A skill is a folder an agent loads to perform a task: procedural knowledge, not a one-off answer. This skill teaches how to author one that conforms to the **Agent Skills** open format, so it works in any compatible agent (Claude Code, Codex, VS Code, Valet), not just one.

This is the format standard. It links out for the exhaustive reference and keeps the working rules inline. Read the source docs once for depth:

- Format spec: https://agentskills.io/specification
- Quickstart: https://agentskills.io/skill-creation/quickstart
- Best practices: https://agentskills.io/skill-creation/best-practices
- Optimizing descriptions: https://agentskills.io/skill-creation/optimizing-descriptions
- Using scripts: https://agentskills.io/skill-creation/using-scripts

## When To Use

- Writing a new skill
- Editing, refactoring, or splitting an existing skill
- Reviewing a skill before it merges
- Turning a runbook, transcript, or a task you keep re-explaining into something reusable

**When NOT to use:** a one-off instruction that will not be reused (just do the task); deterministic code with no agent judgment (that is a script the skill *calls*, not a skill); a task the agent already handles well unaided (a skill there adds noise, not value).

## Anatomy of a skill

A skill is a directory whose name matches its `name` field:

```
<skill-name>/
  SKILL.md          required: frontmatter + instructions
  references/       optional: deep docs, loaded on demand
  scripts/          optional: executable code the skill runs
  assets/           optional: templates, schemas, data files
```

`SKILL.md` is YAML frontmatter followed by a Markdown body.

### Frontmatter

Only `name` and `description` are required.

| Field | Required | Rule |
|---|---|---|
| `name` | yes | 1-64 chars, lowercase `a-z0-9` and single hyphens, no leading/trailing/double hyphen, matches the folder name |
| `description` | yes | 1-1024 chars; says what it does *and when to use it* (see below) |
| `license` | no | short: a license name or bundled file |
| `compatibility` | no | only if there are real environment requirements (packages, network, product) |
| `metadata` | no | free-form string map (author, tags, version) |
| `allowed-tools` | no | experimental; space-separated pre-approved tools |

Most skills need only `name`, `description`, and a small `metadata` block.

### The description is the trigger

At startup an agent reads only each skill's `name` and `description`. That text decides whether the skill loads at all. It carries the entire triggering burden, so write it deliberately:

- **Imperative and intent-first:** "Use when the user wants to X", not "This skill does X."
- **List real phrasings, including implicit ones:** name what a user would actually say, and cover cases where they describe the need without naming the domain ("even if they don't say 'CSV'").
- **Bound it:** enough scope to catch the right prompts, tight enough not to fire on near-misses. If two skills are adjacent, say what this one does *not* do.
- **Under 1024 chars.** Descriptions grow during editing; check the limit.

Weak: `description: Helps with PDFs.`
Strong: `description: Extract text and tables from PDFs, fill forms, merge files. Use when the user has a PDF or mentions forms or document extraction, even without naming the format.`

### The body

The Markdown after the frontmatter is the instructions. No required structure, but keep it **under ~500 lines / ~5000 tokens**, because it all loads into context on activation. Recommended shape: overview, when-to-use, stepwise method with a worked example, gotchas, and edge cases.

## A complete minimal skill

This is a whole valid skill. Most skills need little more than this:

```markdown
---
name: release-notes-draft
description: Draft release notes from merged PRs. Use when asked to write or update release notes, a changelog, or a "what shipped" summary, even if the user just says "summarize this release."
---

To draft release notes:

1. List PRs merged since the last tag:
   gh pr list --state merged --search "merged:>$(git log -1 --format=%cI $(git describe --tags --abbrev=0))"
2. Group them under Added / Changed / Fixed.
3. Write one line per change, for users, not for committers.
4. Flag any PR labeled "breaking" at the top.
```

## Progressive disclosure: put depth in references

Load only what each run needs.

1. **Metadata** (~100 tokens): `name` + `description`, always loaded.
2. **Body** (<5000 tokens): loaded on activation.
3. **`references/`, `scripts/`, `assets/`**: loaded only when the task reaches them.

When the body wants to exceed 500 lines, move detail into `references/` and **tell the agent when to load it**: "Read `references/errors.md` if the API returns a non-200" beats a bare "see references/". A trigger the agent can recognize is the whole point; without it, the file never gets read at the right moment.

## When to bundle a script

Prose is for judgment; scripts are for determinism.

- If a step is the same every time and can be checked, write a script and have the skill run it. Do not narrate in prose what code should enforce.
- Reference scripts by **relative path** and list them so the agent knows they exist.
- Design scripts for agentic use: **no interactive prompts** (agents run non-interactive shells and will hang), a real `--help`, clear error messages that say what to try next, **structured output** (JSON/CSV) to stdout with diagnostics to stderr, idempotency, and `--dry-run` for anything destructive.
- Pin versions in one-off commands (`npx eslint@9`) so behavior is stable over time.

Not every skill needs a script. Many are pure guidance.

## Calibrate control to fragility

Match how prescriptive you are to how easily the step breaks.

- **Give freedom** where several approaches work: explain *why*, list what to check, let the agent choose. Explaining purpose beats rigid steps when the task tolerates variation.
- **Be exact** where the operation is fragile or order matters: give the precise command and say "run exactly this, do not add flags."

Most skills mix both. Calibrate each part independently.

## Patterns worth using

Pull these in when they fit; skip the rest.

- **Gotchas**: the highest-value content. Environment facts that defy reasonable assumptions ("the `/health` endpoint returns 200 even when the DB is down; use `/ready`"). Keep them in `SKILL.md` so they are read *before* the situation. When you correct an agent mistake, add the correction here.
- **Defaults, not menus**: pick one tool, mention alternatives briefly. "Use pdfplumber; for scanned PDFs use pdf2image" beats listing four equal options.
- **Procedures over declarations**: teach the reusable method, not the answer to one instance.
- **Checklists**: for multi-step workflows with gates, so the agent does not skip a step.
- **Validation loops**: do the work, run a check, fix, repeat until it passes; provide the check (a script or a reference to verify against).
- **Plan-validate-execute**: for batch or destructive work, write an intermediate plan, validate it against a source of truth, then execute.
- **Triage gate (optional)**: for skills where one request could mean several different actions, open by restating the intent, routing to the one right path (or handing off to a sibling skill), and escalating to a human when ambiguous. Use it in routing skills; leave it out of single-purpose ones.

## Where skills live

In this repository, each skill is one folder under **`skills/<skill-name>/`**. The skill file is canonical. Skills that are purely generic can also live wherever your agent discovers skills.

**Register the skill in the root `README.md`.** That README is the human-facing index of the skills. Add your skill to the list in the same PR as the skill itself:

```
- `<skill-name>/` — one-line description of what it does and when to use it.
```

An unlisted skill is invisible to anyone reading the repository. Keep the two in sync: adding, renaming, or removing a skill updates this list.

## Authoring checklist

- [ ] Folder `<name>/` created; `name` matches the folder and is valid
- [ ] `name` does not collide with anything in `skills/` or with skills your agents already load (runtime built-ins, other skill libraries)
- [ ] `description` is imperative, intent-first, lists real phrasings, under 1024 chars
- [ ] Body under ~500 lines; depth pushed to `references/` with explicit "load when..." pointers
- [ ] Deterministic steps are scripts (non-interactive, `--help`, structured output), not prose
- [ ] Control calibrated: exact where fragile, free where flexible
- [ ] A worked example is included
- [ ] Gotchas captured for anything that defies assumptions
- [ ] Validated: `npx --yes skills-ref validate ./<skill-name>` passes
- [ ] Registered in the root `README.md`
- [ ] PR opened (SKILL.md + README entry together), folder owner tagged

## Rules

- `name` matches the folder and follows the charset rules exactly, or the skill will not load.
- The `description` is the trigger. If it does not name real user phrasings, the skill never activates, no matter how good the body is.
- Keep `SKILL.md` focused and short; move reference depth into `references/` and say when to load it.
- Deterministic work is a script the skill calls, not prose the skill narrates.
- One skill is one coherent unit. If describing its scope needs "and also", split it.
- Link out for the generic format; do not paste the external spec into the repo (it drifts).

## Common Mistakes

| Mistake | Fix |
|---|---|
| Vague description ("helps with X") | Imperative, intent-first, list the phrasings that should trigger it |
| `name` mismatched with folder or bad charset | Lowercase, single hyphens, equal to the folder name |
| Reusing a name an agent already loads | Check runtime built-ins and `skills/` before naming |
| 800-line SKILL.md | Cut to the core; move depth to `references/` with load-when pointers |
| "See references/ for details" | Name the trigger: "read X when Y happens" |
| Deterministic steps written as prose | Bundle a script; have the skill run it |
| Interactive script (prompts for input) | Take flags/stdin; agents hang on prompts |
| Menu of four equal tools | Pick a default, mention alternatives briefly |
| Answer to one instance, not a method | Teach the reusable procedure |
| New skill not added to the root `README.md` | Register it under `## Skills` in the same PR |
| Skipping validation before ship | Run `npx --yes skills-ref validate ./<skill-name>` |

## Troubleshooting

- **Skill never triggers:** two possible causes. Either the description is too narrow or not intent-framed (add real phrasings and implicit cases), or the task is simple enough that the agent handles it without consulting any skill. Agents typically only reach for skills on tasks beyond their unaided ability, so a perfect description may still not fire on a trivial request. Test with prompts that genuinely need the skill's knowledge.
- **Skill fires on the wrong prompts:** too broad. Add what it does *not* do and the boundary with the adjacent skill.
- **Body keeps growing:** you are documenting every edge case. Cut to the common path plus a gotchas list; let the agent's judgment handle the rest.
- **Agent ignores a bundled file:** you did not give it a load trigger. Replace "see references/" with "read it when <condition>".
- **Not sure it should be a skill at all:** if the agent already does the task well unaided, or it is one-off, it is not a skill.

## Related Skills

- Agent runtimes may ship their own generic skill-writing skill (often named `writing-skills`). This skill is deliberately named `writing-brain-skills` so the two never collide; this file is the working standard for this repository, and https://agentskills.io remains the full format reference.
- `writing-concept-notes` / `writing-executable-specifications`: use those when the artifact is a system spec, not a skill.
