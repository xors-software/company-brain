---
type: principle
title: "Turn a repeated correction into a check"
description: "When you give, or get, the same correction a second time."
source: adapted from pstack (MIT), https://github.com/backnotprop/pstack
owner: engineering
last-verified: 2026-11-02
---

# Turn a repeated correction into a check

Encode the rule as a lint, a test, a type, a config flag, or a script, so it cannot be missed again. If the rule needs judgment, make it more visible and add an example of the mistake.

Reason: written advice is forgotten. A check is not.

Example: after a second missing changelog line, add a CI check, not a longer guide.
