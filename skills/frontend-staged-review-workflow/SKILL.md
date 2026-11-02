---
name: frontend-staged-review-workflow
description: Review only git-staged frontend changes with independent sub-agents, at least two passes per selected risk scope, frozen index evidence and validated findings. Excludes file edits and unit-test-only suggestions.
license: MIT
---

# Frontend Staged Review Workflow

Use for staged frontend review. For heavy redundancy use [heavy staged](../frontend-heavy-staged-review-workflow/SKILL.md); for committed contributions use [branch review](../frontend-branch-review-workflow/SKILL.md). Do not use this workflow to review its own documentation or implement fixes.

Preferred entrypoint: **Frontend Review**, staged mode, selected as the top-level agent in VS Code Local. Direct invocation in another compatible top-level agent uses installed named workers with complete prompts; in Local explicitly set `agentName` on `#tool:agent/runSubagent`. Do not omit it as an anonymous fallback or delegate this workflow/coordinator to a subagent that would need nested workers. Read the [harness compatibility rules](references/vscode-copilot-compatibility.md); native Copilot requires an adapted configuration and its own `task` schema. If required workers/delegation are unavailable, return `Incomplete`; do not simulate reviewer personas or count coordinator analysis as review.

Read the [shared review contract](references/review-contract.md) before preparing the packet. It defines immutable staged evidence, Skill routing, coverage cells, output validity, severity adjudication and validator gates.

## Prepare

- Capture repository root and status; freeze HEAD, raw index manifest and cached diff as defined in the contract. Reject unresolved index stages. Empty staged diff means there is nothing to review.
- Scope is only the captured `git diff --cached`. Unstaged/untracked changes are excluded; pinned index/base blobs supply full-file and package/config context.
- Select `code-review-and-quality` once, plus only evidence-backed specialist Skills from the shared matrix. Upgraded RHF, i18n and design guidance applies conditionally. TDD is for inspecting changed behavior tests, never a mandate for new tests.
- Record exact installed Skill paths, criteria, trigger/risk, snapshot/scope IDs, file/hunk coverage cells, reviewer IDs, angles and waves before dispatch. Budget for two independent completed seats per required cell and one aggregation validator.
- If a cap prevents required coverage, mark that gap; do not silently lower the standard.
- Follow the shared [runtime/evidence protocol](references/runtime-and-evidence.md) for the optional Azure description worker, bounded automatic recovery, version-matched dependency source and self-contained schema-v2 packets. Azure unavailability alone is a disclosed skip, not a code-review failure.

## Review and validate

1. Dispatch **Frontend Reviewer**, or **Frontend Security Reviewer** for selected security/privacy risks. Use [the reviewer prompt](templates/subagent-prompt.md), fully populated with the frozen packet.
2. Each selected Skill/scope needs at least two independent, completed, valid outputs covering every assigned hunk. Sharding never reduces per-cell quorum.
3. Each reviewer remains blind to other findings. Automatically retry failed, timed-out, truncated, invalid or repairably incomplete responses once with a fresh complete packet and the same snapshot/assignment; count only the accepted attempt. Apply the shared deterministic-blocker/size rules and leave exhausted seats incomplete.
4. Reject schema/snapshot/scope mismatches, missing criteria and incomplete coverage. A syntactically valid `blocked` or `degraded` result does not count.
5. Aggregate evidence-backed issues, deduplicate root causes and reconcile severity from impact. Remove test-only advice; preserve defects in tests that conceal real behavior errors.
6. Complete one logical **Frontend Review Validator** pass using bounded coverage, claim and final-manifest batches with complete assigned raw records and pinned evidence. Require per-finding confirmed/rejected/unresolved decisions under the shared gate; schema/quorum validation alone is insufficient. Apply the shared bounded retry/correction policy. A failed/missing batch or unresolved claim prevents a fully validated verdict.
7. Recheck HEAD/index identity. A changed snapshot requires `Incomplete` and a fresh run, without mixing outputs.

## Report

Use [the final report template](templates/final-report.md): Chinese findings, reviewed snapshot, verdict, material limits and fix order when useful. Keep dispatch/quorum ledgers internal unless requested.

`Incomplete` takes precedence over a findings-based verdict; confirmed findings may still be reported. `Approve` requires unchanged snapshot, complete coverage/quorum and valid aggregation validation. No findings is not proof that unverified behavior works.

Never edit, stage, commit, push, checkout, merge, rebase, reset or run mutating checks.
