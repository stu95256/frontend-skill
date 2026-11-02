---
name: dispatching-parallel-agents
description: Use when two or more independent tasks can run without shared mutable state.
license: MIT
---

# Dispatching Parallel Agents

In VS Code Local, use `#tool:agent/runSubagent` to isolate independent investigations. Native Copilot uses its own `task` tool; check the selected harness and actual schema rather than copying Local arguments. See [compatibility rules](../frontend-staged-review-workflow/references/vscode-copilot-compatibility.md).

## Preconditions

- In Local, confirm `agent/runSubagent` is enabled in the Chat tools picker and actually invoke it when delegating; a `#tool:agent/runSubagent` prompt reference alone does not execute it. Other harnesses need their own available delegation capability.
- Split work only when tasks do not depend on each other's output and do not edit the same files or shared resources.
- Prefer specialized custom agents from `~/.copilot/agents`; agent names are case-sensitive.
- In Local, pass the named worker as `agentName`, the complete assignment as `prompt`, and a short `description`. Omitting `agentName` inherits the current role/tools; it is not a neutral-worker selector. Review workflow quorum requires named review workers.

## Procedure

1. Partition the work by independent problem domain, file set, or evidence source.
2. Prepare a complete prompt for each subagent. Include the exact goal, relevant paths and symptoms, constraints, expected output, and completion criteria. Subagents do not inherit the parent conversation reliably enough to omit these details.
3. Issue independent calls together when the host supports it, in bounded waves. Actual parallel execution depends on the host/model limits; do not invent a concurrency API parameter or assume that a declared wave is already running.
4. Keep dependent work sequential. Never run competing editing agents against overlapping files.
5. When results return, verify each result against the repository, reconcile conflicts, and run integration-level checks.

## Statelessness

Local invocations are one-shot tasks. A Local subagent cannot ask the user a question, manage the parent's todo list, or receive a follow-up. If a result is blocked or needs correction, start a fresh invocation containing the original task plus the missing context or findings. Do not assume that other harnesses expose identical lifecycle tools.

Nested subagents are disabled by default. Do not ask a worker to delegate again unless `chat.subagents.allowInvocationsFromSubagents` is intentionally enabled and recursion is bounded.

## Verification

Before claiming completion, account for every dispatched task, confirm no overlapping edits were lost, and run the relevant combined test, lint, typecheck, build, or runtime checks.
