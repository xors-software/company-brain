---
type: principle
title: "Move callers, then delete the old API"
description: "When you replace an internal API and nothing outside depends on the old one."
source: adapted from pstack (MIT), https://github.com/backnotprop/pstack
owner: engineering
last-verified: 2026-11-02
---

# Move callers, then delete the old API

Move every caller to the new API and delete the old one in the same change. Do not keep a compatibility layer for internal code.

Reason: a kept legacy path doubles what readers and tests must cover, and it rarely gets removed later.

Example: switch all six callers to the new client, then delete the old client and its tests.
