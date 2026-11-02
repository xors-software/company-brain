---
type: principle
title: "Test what users can observe"
description: "When you write, change, or keep a test."
source: adapted from pstack (MIT), https://github.com/backnotprop/pstack
owner: engineering
last-verified: 2026-11-02
---

# Test what users can observe

Assert results a caller can see: return values, errors, saved state, and outside effects. A good test fails when that behavior breaks and still passes when only the internals change.

Reason: a test pinned to internals breaks on every refactor and still misses real bugs.

Example: assert that an empty cart sends no charge, not that a private helper was called.
