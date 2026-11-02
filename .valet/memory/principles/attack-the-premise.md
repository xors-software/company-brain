---
type: principle
title: "Test the premise after two failed fixes"
description: "When two or more fixes built on the same belief have failed the same check."
source: adapted from pstack (MIT), https://github.com/backnotprop/pstack
owner: engineering
last-verified: 2026-11-02
---

# Test the premise after two failed fixes

Write down the one belief every failed fix assumed. Before the next fix, make an observation that would come out differently if that belief were false.

Reason: each failed fix is evidence against its premise. A third fix on the same premise spends effort where the evidence says the cause is not.

Example: two cache fixes did not stop the stale page. Check whether the page reads the cache at all before you write a third.
