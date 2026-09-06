---
name: dispatching-parallel-agents
description: Use when two or more independent tasks can run without shared mutable state.
license: MIT
---

# Dispatching Parallel Agents

Use VS Code Chat's `#tool:agent/runSubagent` tool to isolate independent investigations and run them concurrently.

## Preconditions

- Confirm `agent/runSubagent` is enabled in the Chat tools picker; use `#tool:agent/runSubagent` in executable prompt instructions.
- Split work only when tasks do not depend on each other's output and do not edit the same files or shared resources.
- Prefer specialized custom agents from `~/.copilot/agents`; agent names are case-sensitive.

## Procedure

1. Partition the work by independent problem domain, file set, or evidence source.
2. Prepare a complete prompt for each subagent. Include the exact goal, relevant paths and symptoms, constraints, expected output, and completion criteria. Subagents do not inherit the parent conversation reliably enough to omit these details.
3. Invoke all independent subagents in the same model turn so VS Code can run them in parallel.
4. Keep dependent work sequential. Never run competing editing agents against overlapping files.
5. When results return, verify each result against the repository, reconcile conflicts, and run integration-level checks.

## Statelessness

Each invocation is a one-shot task. A subagent cannot ask the user a question, manage the parent's todo list, or receive a follow-up. If a result is blocked or needs correction, start a fresh invocation containing the original task plus the missing context or findings.

Nested subagents are disabled by default. Do not ask a worker to delegate again unless `chat.subagents.allowInvocationsFromSubagents` is intentionally enabled and recursion is bounded.

## Verification

Before claiming completion, account for every dispatched task, confirm no overlapping edits were lost, and run the relevant combined test, lint, typecheck, build, or runtime checks.
