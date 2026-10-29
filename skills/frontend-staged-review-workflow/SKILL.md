---
name: frontend-staged-review-workflow
description: Review only git-staged frontend changes with independent sub-agents, at least two passes per selected risk scope, frozen index evidence and validated findings. Excludes file edits and unit-test-only suggestions.
license: MIT
---

# Frontend Staged Review Workflow

Use for staged frontend review. For heavy redundancy use [heavy staged](../frontend-heavy-staged-review-workflow/SKILL.md); for committed contributions use [branch review](../frontend-branch-review-workflow/SKILL.md). Do not use this workflow to review its own documentation or implement fixes.

Preferred entrypoint: **Frontend Review**, staged mode. Direct invocation in another top-level agent uses `#tool:agent/runSubagent`, with installed hidden workers or independent anonymous workers receiving the complete bundled prompt. If real delegation is unavailable, return `Incomplete`; do not simulate reviewer personas or count coordinator analysis as review.

Read the [shared review contract](references/review-contract.md) before preparing the packet. It defines immutable staged evidence, Skill routing, coverage cells, output validity, severity adjudication and validator gates.

## Prepare

- Capture repository root and status; freeze HEAD, raw index manifest and cached diff as defined in the contract. Reject unresolved index stages. Empty staged diff means there is nothing to review.
- Scope is only the captured `git diff --cached`. Unstaged/untracked changes are excluded; pinned index/base blobs supply full-file and package/config context.
- Select `code-review-and-quality` once, plus only evidence-backed specialist Skills from the shared matrix. Upgraded RHF, i18n and design guidance applies conditionally. TDD is for inspecting changed behavior tests, never a mandate for new tests.
- Record exact installed Skill paths, criteria, trigger/risk, snapshot/scope IDs, file/hunk coverage cells, reviewer IDs, angles and waves before dispatch. Budget for two independent completed seats per required cell and one aggregation validator.
- If a cap prevents required coverage, mark that gap; do not silently lower the standard.

## Review and validate

1. Dispatch **Frontend Reviewer**, or **Frontend Security Reviewer** for selected security/privacy risks. Use [the reviewer prompt](templates/subagent-prompt.md), fully populated with the frozen packet.
2. Each selected Skill/scope needs at least two independent, completed, valid outputs covering every assigned hunk. Sharding never reduces per-cell quorum.
3. Each reviewer remains blind to other findings. A retry is one fresh stateless invocation with the same snapshot/assignment; count only its accepted attempt. Retry an invalid response once, then leave the seat incomplete if unresolved.
4. Reject schema/snapshot/scope mismatches, missing criteria and incomplete coverage. A syntactically valid `blocked` or `degraded` result does not count.
5. Aggregate evidence-backed issues, deduplicate root causes and reconcile severity from impact. Remove test-only advice; preserve defects in tests that conceal real behavior errors.
6. Invoke **Frontend Review Validator** once on raw outputs, coverage/attempt ledger and draft report. Apply the shared bounded retry/correction policy. A failed or missing validator prevents a fully validated verdict.
7. Recheck HEAD/index identity. A changed snapshot requires `Incomplete` and a fresh run, without mixing outputs.

## Report

Use [the final report template](templates/final-report.md): Chinese findings, reviewed snapshot, verdict, material limits and fix order when useful. Keep dispatch/quorum ledgers internal unless requested.

`Incomplete` takes precedence over a findings-based verdict; confirmed findings may still be reported. `Approve` requires unchanged snapshot, complete coverage/quorum and valid aggregation validation. No findings is not proof that unverified behavior works.

Never edit, stage, commit, push, checkout, merge, rebase, reset or run mutating checks.
