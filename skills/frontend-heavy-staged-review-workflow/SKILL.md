---
name: frontend-heavy-staged-review-workflow
description: Review git-staged frontend changes with heavy independent redundancy, defaulting to five completed reviewers per selected risk scope, bounded replacements and two aggregation validators. Excludes file edits and unit-test-only advice.
license: MIT
---

# Frontend Heavy Staged Review Workflow

Use when explicitly requested or selected for high-risk staged review. Ordinary staged mode is [here](../frontend-staged-review-workflow/SKILL.md); committed branch review is [here](../frontend-branch-review-workflow/SKILL.md).

Preferred entrypoint: **Frontend Review**, heavy staged mode. Direct top-level invocation uses `#tool:agent/runSubagent` with installed hidden workers or independent anonymous workers receiving the full packet. Without real delegation, return `Incomplete`.

Read the [shared contract](../frontend-staged-review-workflow/references/review-contract.md) and [heavy-mode procedure](references/FRONTEND_HEAVY_STAGED_REVIEW_WORKFLOW.md) before dispatch. The contract supplies frozen index evidence, upgraded Skill routing, per-hunk coverage, independent-seat counting, JSON validation and findings adjudication.

Defaults remain **five completed independent seats per selected Skill/risk scope** and **two aggregation validator passes**. User configuration and bounded replacement rules are in the procedure. Never use consensus/adjudication reviewers to fill independent quorum.

Use [the reviewer prompt](templates/subagent-prompt.md) for each stateless invocation and [the final report template](templates/final-report.md) for concise Chinese findings. Snapshot/coverage/quorum/required-validator gaps prevent `Approve`; keep confirmed findings visible with `Incomplete` or explicitly authorized `Degraded`.

This is read-only: no edits, staging, commits, pushes, checkout, merge, rebase, reset, auto-fix or mutating verification commands.
