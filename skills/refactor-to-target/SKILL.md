---
name: refactor-to-target
description: >
  Refactor a PR branch to meet a specific diff-size target while improving performance,
  correctness, and simplicity. Use when finishing PR work, when a diff is too large,
  when asked to "clean this up before merge", "reduce the changeset", "simplify this PR",
  "get this ready for review", "finish up this PR", "make this smaller", "optimize this branch",
  or any request to shrink a branch's footprint while preserving or improving its value.
  Always invoke before marking PR work complete or saying a PR is ready for review.
metadata:
  version: "1.0"
  tags: ["refactor", "PR", "diff", "code-quality"]
---

# Refactor to Target

## Goal

Improve this project's **performance, correctness, and simplicity** while reducing this branch's diff to **fewer than the specified target net new lines**.

**Do not stop until that target is reached.**

When the user does not specify a target line count, ask for it before proceeding. Common targets: 200, 300, 500 lines depending on PR scope.

---

## Method

### 1. Understand first

- Read the architecture, documented invariants, and real calling contracts
- Identify what the code *must* do vs. what it defensively handles
- Find duplication, dead code, unnecessary restrictions, and accidental complexity

### 2. Simplify around real contracts

- Remove handling for states that valid callers cannot produce
- Eliminate defensive code for impossible conditions
- Extract duplication into shared helpers
- Delete dead code paths and unused abstractions
- Remove unnecessary configuration, flags, or escape hatches

### 3. Document new assumptions

When a simpler design depends on an assumption about how the code is called:

- Make that assumption **explicit** in a doc comment, assertion, or precondition check
- Document the usage contract so future maintainers understand the boundary

### 4. Measure and iterate

- Check the current net line diff against the base branch (typically `main` or `master`):
  ```bash
  git diff <base-branch> --shortstat
  ```
  Look for the pattern `X insertions(+), Y deletions(-)`. Net lines = X - Y.
- Apply one simplification at a time
- Run tests after each change
- Repeat until diff is under the target net new lines

---

## Preserve

- **Intended feature set**: the user-facing behavior and capabilities
- **Correctness**: the code still does what it's supposed to do
- **Safety**: no new undefined behavior, data races, or vulnerabilities
- **Compatibility**: public APIs, config formats, wire protocols unchanged (unless that's the point of the PR)
- **Observability**: keep logs, metrics, and error messages that serve a real purpose
- **Meaningful tests**: keep coverage that exercises real scenarios; remove tests of deleted code or impossible states

---

## Do Not

- **Game the line count** by removing protections, types, diagnostics, or coverage that serve a real purpose
- **Delete error handling** that guards against real failure modes
- **Remove types or validation** that catch actual bugs
- **Strip logs or metrics** that are used in production
- **Weaken tests** just to make the diff smaller
- **Add complexity** (clever tricks, indirection, macros) to hide lines

---

## Gotchas

1. **"Dead" code may be reachable through reflection, dynamic dispatch, or config.**  
   Verify before deleting. Check call-sites, plugin systems, and feature flags.

2. **Defensive checks may be redundant *today* but were added after a real bug.**  
   Look for commit history, issue links, or TODO comments before removing.

3. **Duplication may exist because two call-sites have subtly different needs.**  
   Unify only when the contract is truly identical.

4. **A simpler design may require a stricter contract.**  
   Document the new assumption. Add a precondition check if the cost is low.

5. **Net lines = additions − deletions.**  
   Deleting old code while adding new code can still meet the target.

6. **Tests inflate the diff.**  
   It's fine to refactor test helpers or deduplicate test setup to reduce lines, as long as real coverage remains.

---

## Success Criteria

- [ ] Net diff is **under the target line count**: `git diff <base> --shortstat`
- [ ] All existing tests pass
- [ ] No new compiler warnings or lint violations
- [ ] Feature set and user-facing behavior unchanged (or intentionally improved)
- [ ] Code is simpler, clearer, or faster than before
- [ ] Any new assumptions are documented in comments or enforced by assertions

**Do not mark the PR as ready or report completion until all criteria are met.**

---

## Example refactorings that reduce lines while improving quality

- **Extract repeated logic** into a helper function (net negative if called 3+ times)
- **Delete unused parameters** from internal functions
- **Inline single-use helpers** that don't clarify intent
- **Remove feature flags** for code that shipped and stabilized
- **Collapse nested conditionals** with early returns
- **Replace defensive error-enum variants** with simpler error types when only one failure mode is possible
- **Delete compatibility shims** for versions no longer supported
- **Merge duplicate test cases** that exercise the same code path with trivial input variation

---

## Workflow

```bash
# 1. Check current diff size
git fetch origin
git diff origin/main --shortstat  # or appropriate base branch

# 2. Identify simplification opportunities
# Read the code, find duplication, unused code, over-defensive checks

# 3. Apply one refactoring at a time
# Edit, test, commit

# 4. Measure progress
git diff origin/main --shortstat

# 5. Repeat until under target
```

---

## Validation loop

After each change:

1. **Build**: `cargo build` / `npm run build` / equivalent
2. **Test**: `cargo test` / `npm test` / full test suite
3. **Lint**: `cargo clippy` / `eslint` / project linter
4. **Diff check**: `git diff origin/main --shortstat` — are we under the target yet?

If any step fails, fix or revert the change before continuing.

---

## When to stop

Stop when:

- Net diff is under the target lines, AND
- All tests pass, AND
- The code is simpler/clearer/faster than before

Do not stop before all three conditions are met.

---

## Reusable Quality Principle

> Understand the real contracts first. Simplify around them, document them when needed, and do not add complexity for hypothetical callers or impossible states. Preserve real correctness and behavior while improving performance, clarity, and maintainability. Remove accidental complexity without gaming superficial metrics. Continue until the stated objective and measurable target are actually met.
