---
name: executing-plans
description: Use when a written implementation plan must be executed and verified in the current workspace.
license: MIT
---

# Executing Plans

Execute an approved plan in dependency order and prove each acceptance criterion with repository evidence.

## Procedure

1. Read the complete plan and any authoritative specification. Identify contradictions, missing prerequisites, and protected side effects before editing.
2. Confirm an isolated feature branch or worktree. Do not implement directly on the protected default branch without explicit approval.
3. Create one tracked task per plan item and record the starting Git SHA.
4. For each task:
   - mark it in progress;
   - inspect relevant code and usages;
   - implement only the stated scope;
   - run the specified targeted verification;
   - record changed files and actual results;
   - mark it complete only when its criteria pass.
5. Use `subagent-driven-development` when `agent/runSubagent` and the required worker agents are available. Keep dependent tasks sequential and use fresh invocations for every repair.
6. After all tasks, review the full diff and run relevant integration tests, lint, typecheck, build, and runtime checks.
7. Report completed tasks, exact verification results, skipped checks, coordinator rulings, and remaining risks.

## Stop Conditions

Stop for an irreversible or destructive operation, a security-sensitive action, an external side effect that requires approval, or a plan so incomplete that every implementation path would be a guess. Resolve ordinary technical ambiguity from repository evidence and record the ruling.

## Verification

The plan is complete only when every task and acceptance criterion is accounted for and the final integrated workspace passes the relevant checks.
