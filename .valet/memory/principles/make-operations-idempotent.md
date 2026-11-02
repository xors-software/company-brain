---
type: principle
title: "Make each operation safe to run twice"
description: "When you design a command, a job, or a step that can crash, restart, or retry."
source: adapted from pstack (MIT), https://github.com/backnotprop/pstack
owner: engineering
last-verified: 2026-11-02
---

# Make each operation safe to run twice

Read the current state, compare it to the goal, and apply only the difference. Make anything a run leaves behind, such as a lock or a half-written record, easy for the next run to recognize.

Reason: retries and restarts are normal. An operation that breaks on a second run turns each restart into an incident.

Example: "create the bucket if it does not exist", not "create the bucket".
