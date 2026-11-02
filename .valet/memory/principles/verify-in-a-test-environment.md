---
type: principle
title: Verify a change in a test environment before merge
description: Before you merge a change to a branch that deploys.
source: general practice
owner: engineering
last-verified: 2026-11-02
---

# Verify a change in a test environment before merge

Deploy the change to a test environment and use it the way a person will: click through the flow, or run the job. Report what you checked. Passing CI alone is not enough.

Reason: tests check what their authors thought of. The real flow finds the rest.

Example: "Deployed to the test environment, created a workflow with the Granola tool, ran it, and saw the notes in the output."
