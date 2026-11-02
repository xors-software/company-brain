---
type: principle
title: "Put domain rules in one structure"
description: "When logic branches a lot, tracks state, or repeats an assumption across files."
source: adapted from pstack (MIT), https://github.com/backnotprop/pstack
owner: engineering
last-verified: 2026-11-02
---

# Put domain rules in one structure

Encode the rule in a data structure: a state machine, a typed model, a lookup table, or a union type. Do not spread it across conditionals.

Reason: a structure that matches the domain makes wrong states impossible and removes branches.

Example: replace three booleans for a job's phase with one status field that has four values.
