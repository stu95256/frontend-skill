---
name: frontend-heavy-staged-review-workflow
description: Review git-staged frontend changes with heavy independent redundancy, defaulting to five completed reviewers per selected risk scope, bounded replacements and two aggregation validators. Excludes checkout edits and unit-test-only advice.
license: MIT
---

# Frontend Heavy Staged Review Workflow

Use when explicitly requested or selected for high-risk staged review. Ordinary staged mode is [here](../frontend-staged-review-workflow/SKILL.md); committed branch review is [here](../frontend-branch-review-workflow/SKILL.md).

Preferred entrypoint: **Frontend Review**, heavy staged mode, selected as the top-level agent in VS Code Local. Direct invocation in another compatible top-level agent uses installed named workers with complete prompts; in Local explicitly set `agentName` on `#tool:agent/runSubagent`. Do not omit it as an anonymous fallback or delegate this workflow/coordinator to a subagent that would need nested workers. Read the [harness compatibility rules](../frontend-staged-review-workflow/references/vscode-copilot-compatibility.md); native Copilot requires an adapted configuration and its own `task` schema. If required workers/delegation are unavailable, return `Incomplete`.

Read the [shared contract](../frontend-staged-review-workflow/references/review-contract.md) and [heavy-mode procedure](references/FRONTEND_HEAVY_STAGED_REVIEW_WORKFLOW.md) before dispatch. The contract supplies frozen index evidence, upgraded Skill routing, per-hunk coverage, independent-seat counting, semantic result validation and findings adjudication.

Defaults remain **five completed independent seats per selected Skill/risk scope** and **two aggregation validator passes**. User configuration and bounded replacement rules are in the procedure. Never use consensus/adjudication reviewers to fill independent quorum.

Apply the shared [runtime/evidence protocol](../frontend-staged-review-workflow/references/runtime-and-evidence.md): one optional Azure description worker, tiered bounded recovery and schema-v3 evidence packets. Persist frozen sources, packet/ledger versions and exact worker text in the append-only store outside the checkout before parsing. Prefer compact JSON; permit only lossless presentation normalization, with readable `raw_ref`, any `normalized_ref` and provenance supplied to coverage validators. Counts/end markers are optional diagnostics. Each logical validator pass retains complete coverage/claim/final-manifest batches. Auxiliary Azure unavailability alone is a disclosed skip, not a required coverage gap.

The shared candidate evidence gate overrides assigned Skill checklist demands. Both validator passes verify individual findings against pinned source, including reachable triggers, before/after regressions and checked protections; agreement or confidence alone is insufficient. Publish only candidates confirmed by both required passes on the corrected draft. Unsupported claims are removed; unresolved decisive evidence prevents a fully validated verdict.

Use [the reviewer prompt](templates/subagent-prompt.md) for each stateless invocation and [the final report template](templates/final-report.md) for concise Chinese findings. Snapshot/coverage/quorum/required-validator gaps prevent `Approve`; keep confirmed findings visible with `Incomplete` or explicitly authorized `Degraded`.

Keep the reviewed checkout read-only: no edits, staging, commits, pushes, checkout, merge, rebase, reset, auto-fix or mutating verification commands. Coordinator evidence-store persistence follows the shared protocol.
