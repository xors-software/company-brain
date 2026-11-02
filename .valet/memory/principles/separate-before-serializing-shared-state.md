---
type: principle
title: "Remove shared state before you add locks"
description: "When two workers, agents, or jobs might write the same file, branch, key, or record."
source: adapted from pstack (MIT), https://github.com/backnotprop/pstack
owner: engineering
last-verified: 2026-11-02
---

# Remove shared state before you add locks

First ask if they need the same object. Usually they do not: give each one its own file, branch, or key, and merge where results are read. Add a lock only when one shared writer is a real requirement.

Reason: shared writes cause rare, hard races. Separation removes them, and a lock only manages them.

Example: give each parallel attempt its own worktree, not one branch with a lock.
