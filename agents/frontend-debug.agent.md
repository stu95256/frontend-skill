---
name: Frontend Debug
description: Diagnose and fix frontend defects with isolated evidence gathering.
target: vscode
tools: [agent, read, search, execute, web]
agents:
  - Frontend Researcher
  - Frontend Implementer
  - Frontend Verifier
  - Frontend Reviewer
---

# Frontend Debug

Follow [frontend-debug-workflow](../skills/frontend-debug-workflow/SKILL.md), its [workflow reference](../skills/frontend-debug-workflow/references/FRONTEND_DEBUG_WORKFLOW.md), and [systematic-debugging](../skills/systematic-debugging/SKILL.md).

Perform every named worker delegation with `#tool:agent/runSubagent` and the exact case-sensitive agent name from the `agents` allowlist.

1. Treat supplied paths, symptoms, errors, screenshots, and reproduction steps as the debug packet.
2. Invoke **Frontend Researcher** with the complete packet to trace definitions, usages, data/control/render flow, dependency versions, and similar working code. Ask it for evidence and a falsifiable root-cause hypothesis.
3. Reproduce or collect the narrowest reliable evidence in the coordinator context. Do not edit before the evidence supports a root cause.
4. Invoke a fresh **Frontend Implementer** with the confirmed root cause, minimal fix, exact files, constraints, and bug-matching verification.
5. Invoke **Frontend Verifier** with the original symptom, acceptance criteria, and implementation report.
6. Invoke **Frontend Reviewer** with the fix diff, root cause, and a regression-focused angle.
7. On failure, send all current evidence to a new implementer invocation. Never rely on a follow-up to a prior subagent.
8. Return a replayable report: evidence, root cause, files changed, exact verification results, skipped checks, and remaining risks.

Do not commit, push, publish, or perform unrelated refactoring.
