---
type: principle
title: "Validate at the boundary, trust inside"
description: "When you add validation, error handling, or an adapter to an outside system."
source: adapted from pstack (MIT), https://github.com/backnotprop/pstack
owner: engineering
last-verified: 2026-11-02
---

# Validate at the boundary, trust inside

Check input where it enters: CLI arguments, config, network, and external APIs. Inside the system, use typed data and do not check it again. Keep business logic in pure functions.

Reason: checks spread everywhere are noise and give false safety.

Example: parse and check a webhook body once in the handler, then pass a typed object on.
