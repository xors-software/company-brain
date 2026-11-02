---
type: principle
title: "Remove before you build"
description: "When you plan an addition, a refactor, or a rewrite."
source: adapted from pstack (MIT), https://github.com/backnotprop/pstack
owner: engineering
last-verified: 2026-11-02
---

# Remove before you build

Delete dead code, unused checks, and stale references first. Then build on the smaller base. Build for the use you see, not for edge cases you imagine.

Reason: new work on top of dead weight inherits its cost and hides what is real.

Example: before you add a fourth adapter, delete the two that nothing calls.
