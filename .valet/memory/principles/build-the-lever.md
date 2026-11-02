---
type: principle
title: "Build the tool that does or checks the work"
description: "When work is more than a few obvious edits: a migration, a sweep, an analysis, or a check."
source: adapted from pstack (MIT), https://github.com/backnotprop/pstack
owner: engineering
last-verified: 2026-11-02
---

# Build the tool that does or checks the work

Do the first unit by hand to learn the recipe. Then write the script, codemod, or query that does the rest the same way, and that a reviewer can rerun.

Reason: a hand-made change can only be checked by doing it again. A tool turns "trust me" into "run this".

Example: rename a field in 40 files with a codemod, and show its run, not 40 hand edits.
