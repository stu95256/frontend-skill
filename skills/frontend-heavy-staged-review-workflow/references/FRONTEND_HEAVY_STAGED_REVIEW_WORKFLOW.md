# 前端 Heavy Staged Review Workflow

最後更新：2026-11-03

Read the [shared contract](../../frontend-staged-review-workflow/references/review-contract.md). It owns snapshot capture, conditional Skill selection, evidence, coverage cells, schemas and verdict precedence. This procedure owns heavy configuration and reviewer waves.

## Runtime configuration

```yaml
heavy_review_config:
  review_target: git diff --cached
  reviewers_per_skill: 5
  min_valid_reviewers_per_skill: same_as_reviewers_per_skill
  replacement_budget_per_skill: 3
  recovery_policy: shared_tiered_v3
  allow_degraded_report: false
  max_parallel_subagents: environment_limit
  wave_size: same_as_max_parallel_subagents
  max_total_reviewer_passes: auto_from_coverage_and_recovery_plan
  max_selected_skills: auto_or_user_override
  aggregation_validator_count: 2
  azure_description_check: optional_one_auxiliary_worker
  max_validator_findings_per_batch: 3
  max_total_validator_invocations: auto_from_batches_recovery_and_one_correction_cycle
  max_auxiliary_invocations: 2
  schema_version: 3
  response_format: compact_json_preferred
  evidence_store: external_append_only
  no_unit_test_suggestions: true
  reviewed_checkout_read_only: true
  primary_reviewer_isolation: true
  final_report: findings_only
```

Resolve values before dispatch. User overrides persist; reviewer target and minimum are each at least two, with minimum no greater than target. A deliberately lower minimum is recorded and disclosed as reduced redundancy, never described as five-pass completion. Validator count defaults to two; an explicit waiver is disclosed as a validation limit and cannot produce a fully validated approval.

Budget from actual coverage groups, not just the number of Skills. Each Skill's required file/hunk cells need the configured minimum. A large shard may need additional seats to cover every cell. Total pass caps include all primary, retry and replacement reviewer invocations; validators have their own declared budget. A configured cap must never be silently exceeded.

Apply the authoritative [tiered recovery table](../../frontend-staged-review-workflow/references/runtime-and-evidence.md#automatic-bounded-recovery), with separate class counters and a finite total cap. New replacement seats remain limited to `replacement_budget_per_skill` across that Skill's coverage groups. Shards and replacements inherit ancestor counters and remaining global capacity; they cannot restart exhausted recovery allowances. A retry supersedes its previous attempt and adds no independent seat. Exhausted required coverage means `Incomplete`, or `Degraded` only when authorized. Integrity/foreign-snapshot responses are quarantined; deterministic blockers receive no unchanged retry.

Resolve finite primary/validator/auxiliary caps before dispatch. Count coverage, claim and final-manifest batches, class-specific recovery invocations, one corrected-draft cycle per pass, and size-driven replanning. The per-batch finding count is a planning target, never permission to drop findings; replan smaller scopes within the total cap. Optional Azure work has at most two invocations and never consumes a primary seat or validator pass.

## Freeze and select

1. Freeze the non-empty staged packet under the shared contract; HEAD/index/patch identity is mandatory. Persist exact source bytes/provenance and packet/ledger versions in the shared protocol's append-only evidence store outside the checkout.
2. Select baseline plus concrete risks from the shared matrix. Do not select all React/UI Skills merely because a TSX file changed.
3. Upgraded `frontend-design` reviews surface purpose and approved visual direction; RHF reviews dirty/reset/server-value lifecycle; i18n reviews the existing framework and message format. TDD may inspect actual assertions/mocks without generating test-only suggestions.
4. Record exact Skill paths, criteria/resources, risk evidence, snapshot/scope IDs, complete coverage cells, IDs, angles, expected/minimum seats, waves, caps and replacement budget.
5. Use the actual host's delegation tool/schema, with `#tool:agent/runSubagent` for VS Code Local. Keep the coordinator top-level; no nested delegation. Without real delegation, stop with `Incomplete`.

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

Use [the prompt](../templates/subagent-prompt.md). Persist each exact returned raw result before parsing or presentation normalization. Prefer compact JSON; lossless normalization may expose explicit complete records but never invent IDs, status, coverage or findings. Validate snapshot, scope, criteria, actual file/hunk coverage and finding evidence after each wave. Counts/end markers are optional diagnostics. Only `completed` outputs with complete assigned coverage count; `degraded` and `blocked` outputs do not.

## Aggregate and validate

Deduplicate by root cause and affected behavior. Severity follows demonstrated impact and preconditions, not maximum claimed severity or majority vote. Keep credible single-reviewer findings.

Run two independent logical **Frontend Review Validator** passes by default, each comprising the shared coverage, claim and final-manifest batches. Across each pass supply readable immutable `raw_ref` records, any `normalized_ref` and normalization provenance, cells/attempts, draft and pinned evidence for retained and credibly disputed/dropped candidates. Coverage validators compare accepted records to the exact raw output and audit preservation of content. Require `finding_checks` under the shared gate; every final finding must be confirmed by both required passes on the corrected draft. Neither is a primary reviewer, and neither sees the other's conclusions. Unresolved disagreement or missing decisive context is a completion gap. Apply tiered recovery and one corrected-draft cycle per pass within the finite validator cap. Required batch failure is a gap even when reviewer quorum was reached.

Recheck HEAD/index before finalizing. A changed staged snapshot requires a fresh run; never silently refresh the packet while retaining old outputs.

## Result

Use [the report template](../templates/final-report.md). Include reviewed snapshot, verdict and material evidence/redundancy limits. Return confirmed findings even when the workflow is incomplete. Do not print runtime config, dispatch ledgers or worker identities unless asked for an audit log.

- `Incomplete`: a snapshot, scope, coverage, quorum or required validator gap.
- `Degraded`: incomplete workflow explicitly accepted by the user; never `Approve`.
- `Request changes`: completed review with a critical/high blocking issue.
- `Comment`: completed review with other concrete issues.
- `Approve`: no findings and all required gates satisfied.

An empty findings array is meaningful only after these gates. Reviewers do not modify files, run mutating checks or provide unit-test-only advice. Only the coordinator persists review evidence in the separate store under the shared protocol; the reviewed checkout remains unchanged.
