---
type: principle
title: "Work in small units that each end in a check"
description: "When work has many steps: a migration, a sweep, a stack of commits or pull requests."
source: adapted from pstack (MIT), https://github.com/backnotprop/pstack
owner: engineering
last-verified: 2026-11-02
---

# Work in small units that each end in a check

Make each unit one change, then run its check before the next. Order commits so a reviewer can follow the proof, for example the failing test first, then the fix.

Reason: a break found at the unit that caused it is cheap to find. A break found after a batch is buried.

Example: migrate one table, run its checks, then the next, not all ten at once.
