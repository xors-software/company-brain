# .valet

Content that Valet syncs from this repository into agent memory. Valet reads it when this repository is a content source with the memories kind.

## What lives here

- `memory/principles/`: principles. A principle is a rule that guides open-ended work. Valet lists each one in every assistant's prompt, and an agent reads the body before it follows the rule.

Valet mounts `memory/<path>` at `lib/<path>` in the memory of the source's owner, so these files are read-only in Valet. To change a principle, open a pull request here.

## Principle format

Each file is Markdown with frontmatter:

- `type: principle`
- `title`: the rule in a few words. The index shows it.
- `description`: when the rule applies, in one line. The index shows it.
- `source`, `owner`, `last-verified`: provenance, as for other curated content.

The body gives the rule, the reason, and one example. Keep each principle short. Run `valet validate` to check the files before you merge.

## Owner and canonical source

Canonical source: this folder.
