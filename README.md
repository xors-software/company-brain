# company-brain

General-purpose agent skills in the [Agent Skills](https://agentskills.io/specification) format. Each skill is one folder under `skills/` with a `SKILL.md`, so any agent that loads Agent Skills can use them. In Valet, add this repository as a skill source, and Valet syncs every `SKILL.md` it finds.

## Skills

- `basic-code-review/`: review a pull request and report only high-confidence issues.
- `adversarial-code-review/`: attack a change and try to prove it wrong, with numbered findings and a merge verdict.
- `ship-loop/`: take an issue and deliver a CI-green pull request without waiting to be nudged.
- `refactor-to-target/`: shrink a branch to a net-line target while keeping or improving its behavior.
- `writing-concept-notes/`: compress a raw idea into a one-page concept note before specification.
- `writing-executable-specifications/`: write an implementation-grade specification with test vectors, conformance levels, and named invariants.
- `writing-guidelines/`: write, rewrite, or audit human-facing prose, with a register guide, an AI-pattern catalog, and a linter.
- `writing-brain-skills/`: the standard for writing, editing, and reviewing a skill in this repository.

## Add a skill

Read `skills/writing-brain-skills/SKILL.md` first. Then:

1. Create `skills/<skill-name>/SKILL.md`. The `name` field must match the folder name.
2. Validate the skill: `npx --yes skills-ref validate ./skills/<skill-name>`.
3. Add the skill to the list above in the same pull request.

## License

[MIT](LICENSE)
