---
type: principle
title: Answer every review comment before merge
description: Before you merge a pull request that has review comments.
source: general practice
owner: engineering
last-verified: 2026-11-02
---

# Answer every review comment before merge

Read every review comment, from people and from review bots. Fix it, or reply with the reason you did not. Do not merge with an open comment.

Reason: an unanswered comment is a known problem that ships.

Example: a reviewer flags a missing null check. Add the check and a test, then reply with the commit.
