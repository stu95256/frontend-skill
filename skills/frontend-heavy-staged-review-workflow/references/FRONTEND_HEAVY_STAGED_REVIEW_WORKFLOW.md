# 前端 Heavy Staged Review Workflow

最後更新：2026-10-29

Read the [shared contract](../../frontend-staged-review-workflow/references/review-contract.md). It owns snapshot capture, conditional Skill selection, evidence, coverage cells, schemas and verdict precedence. This procedure owns heavy configuration and reviewer waves.

## Runtime configuration

```yaml
heavy_review_config:
  review_target: git diff --cached
  reviewers_per_skill: 5
  min_valid_reviewers_per_skill: same_as_reviewers_per_skill
  replacement_budget_per_skill: 3
  retry_invalid_output_once: true
  retry_failed_reviewer_once: false
  allow_degraded_report: false
  max_parallel_subagents: environment_limit
  wave_size: same_as_max_parallel_subagents
  max_total_reviewer_passes: auto_from_coverage_plan
  max_selected_skills: auto_or_user_override
  aggregation_validator_count: 2
  require_strict_json: true
  no_unit_test_suggestions: true
  review_only_no_file_edits: true
  primary_reviewer_isolation: true
  final_report: findings_only
```

Resolve values before dispatch. User overrides persist; reviewer target and minimum are each at least two, with minimum no greater than target. A deliberately lower minimum is recorded and disclosed as reduced redundancy, never described as five-pass completion. Validator count defaults to two; an explicit waiver is disclosed as a validation limit and cannot produce a fully validated approval.

Budget from actual coverage groups, not just the number of Skills. Each Skill's required file/hunk cells need the configured minimum. A large shard may need additional seats to cover every cell. Total pass caps include all primary, retry and replacement reviewer invocations; validators have their own declared budget. A configured cap must never be silently exceeded.

Each initial seat may have at most one schema retry. New replacement seats are limited to `replacement_budget_per_skill` across that Skill's coverage groups, each eligible for at most one schema retry within the total cap. A retry supersedes its previous attempt; it adds no independent seat. Exhausted budget with uncovered cells means `Incomplete`, or `Degraded` only when authorized.

## Freeze and select

1. Freeze the non-empty staged packet under the shared contract; HEAD/index/patch identity is mandatory.
2. Select baseline plus concrete risks from the shared matrix. Do not select all React/UI Skills merely because a TSX file changed.
3. Upgraded `frontend-design` reviews surface purpose and approved visual direction; RHF reviews dirty/reset/server-value lifecycle; i18n reviews the existing framework and message format. TDD may inspect actual assertions/mocks without generating test-only suggestions.
4. Record exact Skill paths, criteria/resources, risk evidence, snapshot/scope IDs, complete coverage cells, IDs, angles, expected/minimum seats, waves, caps and replacement budget.
5. If real `#tool:agent/runSubagent` calls are unavailable, stop with `Incomplete`.

## Independent waves

Default angles within each selected Skill's actual scope:

| Seat | Angle |
|---|---|
| H01 | Correctness and reachable runtime defects |
| H02 | Empty/boundary data, async failures and races |
| H03 | Integration, architecture fit and local contracts |
| H04 | Relevant rendering/runtime cost and resource lifecycle |
| H05 | Assigned Skill's specific deep checks |

Do not invent an issue to fill an angle. Keep all counted seats blind to others' conclusions. Spread waves within the runtime concurrency limit; record actual tool invocation and attempt IDs. Every retry/replacement receives the full frozen packet and preserves the missing angle. Consensus/adjudication passes can resolve conflicts after primary review but never count toward quorum.

Use [the prompt](../templates/subagent-prompt.md). Validate JSON, snapshot, scope, criteria, actual file/hunk coverage and finding evidence after each wave. Only `completed` outputs with complete assigned coverage count; `degraded` and `blocked` outputs do not.

## Aggregate and validate

Deduplicate by root cause and affected behavior. Severity follows demonstrated impact and preconditions, not maximum claimed severity or majority vote. Keep credible single-reviewer findings.

Run two independent **Frontend Review Validator** passes by default. Give both the raw outputs, coverage cells, dispatch/attempt ledger, draft aggregation and pinned before/after/caller/contract evidence for retained and credibly disputed/dropped candidates. Require `finding_checks` decisions under the shared gate; every final finding must be confirmed by both required passes on the corrected draft. Neither is a primary reviewer. Unresolved disagreements or missing decisive context are completion gaps, not majority votes. Resolve errors and validate the corrected draft; apply the shared limit of one fresh replacement per required validator pass. Required validator failure is a completion gap even when the reviewer count was reached.

Recheck HEAD/index before finalizing. A changed staged snapshot requires a fresh run; never silently refresh the packet while retaining old outputs.

## Result

Use [the report template](../templates/final-report.md). Include reviewed snapshot, verdict and material evidence/redundancy limits. Return confirmed findings even when the workflow is incomplete. Do not print runtime config, dispatch ledgers or worker identities unless asked for an audit log.

- `Incomplete`: a snapshot, scope, coverage, quorum or required validator gap.
- `Degraded`: incomplete workflow explicitly accepted by the user; never `Approve`.
- `Request changes`: completed review with a critical/high blocking issue.
- `Comment`: completed review with other concrete issues.
- `Approve`: no findings and all required gates satisfied.

An empty findings array is meaningful only after these gates. Reviewers do not modify files, run mutating checks or provide unit-test-only advice.
