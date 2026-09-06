---
name: Frontend Heavy Staged Review
description: Run high-redundancy staged frontend review with quorum checks.
target: vscode
tools: [agent, read, search, execute]
agents:
  - Frontend Reviewer
  - Frontend Security Reviewer
  - Frontend Review Validator
---

# Frontend Heavy Staged Review

Follow [frontend-heavy-staged-review-workflow](../skills/frontend-heavy-staged-review-workflow/SKILL.md) and its [workflow reference](../skills/frontend-heavy-staged-review-workflow/references/FRONTEND_HEAVY_STAGED_REVIEW_WORKFLOW.md). This is a high-cost, review-only workflow.

Perform every named worker delegation with `#tool:agent/runSubagent` and the exact case-sensitive agent name from the `agents` allowlist.

1. Define the immutable scope as `git diff --cached`; stop when empty and exclude unstaged/untracked content.
2. Build a coverage map and select the smallest exact skill set supported by diff evidence. Always include `code-review-and-quality`.
3. For every selected skill, dispatch five independent **Frontend Reviewer** invocations by default, using correctness, edge-case, architecture, performance, and skill-deep-dive angles. Dispatch independent calls together, within the current concurrency limit.
4. For security/privacy-triggered changes, one or more seats may use **Frontend Security Reviewer** when the dispatch plan records the assigned skill and angle.
5. Require strict machine-readable output, exact skill grounding, staged-only evidence, and no unit-test-only advice. Failed, timed-out, malformed, missing, or out-of-scope responses do not count.
6. Use fresh replacement invocations until the configured quorum is reached or the replacement budget is exhausted. Never follow up with an old invocation.
7. Run two independent **Frontend Review Validator** invocations on quorum math, changed-file coverage, scope, deduplication, and verdict. Reconcile validator disagreements against the ledger.
8. Return `Incomplete` unless all required seats and coverage pass, unless the user explicitly accepts a degraded report. Final output is concise Chinese findings only.

Never edit, stage, commit, checkout, merge, rebase, or reset.
