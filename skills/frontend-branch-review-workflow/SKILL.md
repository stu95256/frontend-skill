---
name: frontend-branch-review-workflow
description: Review a source branch's committed frontend contribution against a target by pinning source, target and merge-base SHAs. Requires two independent passes per selected risk scope and validated findings; excludes uncommitted changes, edits and unit-test-only suggestions.
license: MIT
---

# Frontend Branch Review Workflow

Use for frontend pre-merge branch review, without creating a PR, merging or editing files. Default source is the current branch; default target is `master` unless the user supplies another target. Staged review belongs to [staged mode](../frontend-staged-review-workflow/SKILL.md).

Preferred entrypoint: **Frontend Review**, branch mode, selected as the top-level agent in VS Code Local. Direct invocation in another compatible top-level agent uses installed named workers with complete prompts; in Local explicitly set `agentName` on `#tool:agent/runSubagent`. Do not omit it as an anonymous fallback or delegate this workflow/coordinator to a subagent that would need nested workers. Read the [harness compatibility rules](../frontend-staged-review-workflow/references/vscode-copilot-compatibility.md); native Copilot requires an adapted configuration and its own `task` schema. If required workers/delegation are unavailable, return `Incomplete`.

Read the [branch procedure](references/FRONTEND_BRANCH_REVIEW_WORKFLOW.md) for ref resolution, fetch and pinned evidence. Read the [shared contract](../frontend-staged-review-workflow/references/review-contract.md) for upgraded Skill selection, coverage, worker schemas, aggregation and validator gates.

Core requirements:

1. Pin `source_sha`, `target_sha` and a unique `merge_base_sha`; use only `git diff --find-renames <merge_base_sha> <source_sha>` as contribution content.
2. Never replace that definition with a target-to-source endpoint diff. Target-only changes are integration context, not source findings by themselves.
3. Exclude index, worktree and untracked content. Read full-file/package/config context from pinned commits.
4. Use baseline `code-review-and-quality` plus evidence-backed specialist Skills from the shared matrix. Design, RHF, i18n and TDD criteria stay within the read-only review scope.
5. Dispatch at least two independent completed seats for each selected Skill's required file/hunk cells. Disjoint file assignments do not satisfy redundant coverage.
6. Require schema-v2 JSON tied to the exact snapshot and three SHAs, actual evidence excerpts and verified delivery counts/end marker. Automatically retry failed, timed-out, truncated, invalid or repairably incomplete outputs once, fresh and complete, under the shared runtime rules; unresolved required gaps are `Incomplete`.
7. Complete one logical **Frontend Review Validator** pass using bounded coverage, claim and final-manifest batches with complete assigned raw records and pinned candidate evidence. Require per-finding confirmed/rejected/unresolved decisions against source, target and merge-base context under the shared gate. Unsupported claims are removed; unresolved decisive evidence prevents a fully validated verdict. Follow the shared bounded correction/replacement policy.
8. Refs moving later do not change the pinned review. Identify exactly which commits were reviewed.
9. Apply the shared [runtime/evidence protocol](../frontend-staged-review-workflow/references/runtime-and-evidence.md), including one optional Azure description worker. Verify PR commit identities before claiming a full comparison; unavailable MCP alone is a disclosed skip, not a code-review failure.

Use [the reviewer prompt](templates/subagent-prompt.md) and [the Chinese final report](templates/final-report.md). Report confirmed issues and material evidence limits even when incomplete. Keep operational ledgers internal unless requested.

Never checkout, switch, merge, rebase, reset, stage, edit, auto-fix, commit, push or run mutating verification commands. Do not suggest adding unit tests or coverage; concrete defects in changed tests remain reviewable.
