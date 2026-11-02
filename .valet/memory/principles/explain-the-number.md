---
type: principle
title: "Explain a number before you trust it"
description: "Before you report or act on a measured number: a speedup, a latency, a cost, or an eval score."
source: adapted from pstack (MIT), https://github.com/backnotprop/pstack
owner: engineering
last-verified: 2026-11-02
---

# Explain a number before you trust it

Name what limits the number, and rule out what else it could measure: errors, cached or skipped work, or noise. Keep the run count and the spread with the number.

Reason: a number without a cause is easy to misread and easy to misuse.

Example: "2x faster over 5 runs, spread 4 percent, limited by disk reads", not just "2x faster".
