---
type: principle
title: "Make code easy to trace"
description: "When you write or review code that is hard to follow."
source: adapted from pstack (MIT), https://github.com/backnotprop/pstack
owner: engineering
last-verified: 2026-11-02
---

# Make code easy to trace

Count the layers a reader must trace to answer a question, and the hidden state they must hold. Inline a wrapper with one caller. Prefer pure functions and the smallest scope for state.

Reason: maintenance cost is the work a reader does to understand the code.

Example: a service that only forwards calls to another service adds a layer and hides nothing. Remove it.
