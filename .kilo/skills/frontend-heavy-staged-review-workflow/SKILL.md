---
name: frontend-heavy-staged-review-workflow
description: Use when reviewing git-staged frontend changes with a heavy real-sub-agent process. Reviews only `git diff --cached`, defaults to five valid sub-agent reviewers per selected review skill, supports configurable reviewer counts and replacement reviewers, validates quorum, runs aggregation validators, forbids unit-test-only suggestions, and returns a concise findings-only report.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [frontend, code-review, staged-diff, subagent, heavy-review, quorum, workflow, react, typescript, no-unit-tests, kilo]
    related_skills: [frontend-staged-review-workflow, audit-code-reviewer, code-review-excellence, typescript-code-reviewer, code-review-and-quality, secpriv-code-review, react-dev, react-useeffect, vercel-react-best-practices, web-design-guidelines, accessibility-compliance, tailwind-design-system, tailwind-v4-shadcn, ant-design, ag-grid, react-hook-form-zod, internationalization-i18n, react-router-declarative-mode, react-router-data-mode, react-router-framework-mode, playwright-best-practices, webapp-testing]
---

# Frontend Heavy Staged Review Workflow

Use this skill when the user wants a heavier version of the frontend staged review workflow with many real independent reviewer sub-agents, replacement reviewers, quorum rules, and aggregation validators.

## Core contract

1. Review target is only `git diff --cached`.
2. Do not review unstaged changes; record them internally as out of scope if present.
3. This is review-only: do not modify files, stage files, auto-fix, or commit.
4. Build runtime config and an internal dispatch plan before reviewer waves; do not show them unless the user asks for the audit log.
5. Reviewer passes must come from actual Kilo sub-agents/custom agents or equivalent sub-agent tooling.
6. The coordinator/main agent must not simulate multiple reviewers or count its own analysis as a reviewer pass.
7. If no real sub-agent mechanism is available, return `Incomplete` and stop.
8. Every selected review skill defaults to five valid reviewer sub-agent outputs.
9. User may override `reviewers_per_skill`, `min_valid_reviewers_per_skill`, `replacement_budget_per_skill`, `max_selected_skills`, `wave_size`, and `allow_degraded_report`.
10. Failed, timed-out, invalid, missing, simulated, or non-skill-grounded outputs do not count toward quorum.
11. Use replacement reviewer waves until quorum is reached or replacement budget is exhausted.
12. Primary reviewers must be independent; do not show H01-H05 each other's findings.
13. Counted reviewers must either read `skills/<skill-name>/SKILL.md` or receive coordinator-injected skill criteria.
14. Run aggregation validator sub-agents internally before finalizing when configured.
15. Exclude unit-test-only suggestions.
16. Final user-facing report must be findings-only.
17. Final user-facing report must be written in Chinese.

## When to use

Use when the user says any of:

- 「用重型 review workflow」
- 「用大量 sub-agent review staged changes」
- 「每個 review skill 跑 5 個 sub-agent」
- 「幫我做 heavy staged review」
- 「我要更保險的前端 staged review」
- 「review git add 的內容，但多跑幾個 reviewer」

Do not use for:

- Unstaged-only review.
- Quick/light review where `frontend-staged-review-workflow` is enough.
- Auto-fix loops.
- Implementation planning; use `frontend-task-preflight` for that.

## Default runtime config

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
  max_total_reviewer_passes: auto_from_selected_skills
  max_selected_skills: auto_or_user_override
  skill_priority_order: evidence_strength_then_core_then_user_request
  aggregation_validator_count: 2
  require_strict_json: true
  no_unit_test_suggestions: true
  review_only_no_file_edits: true
  primary_reviewer_isolation: true
  final_report: findings_only
```

## Required pre-flight commands

Run and capture internally:

```bash
git rev-parse --show-toplevel
git status --short --branch
git diff --cached --name-only
git diff --cached --stat
git diff --cached
```

Stop if `git diff --cached --name-only` is empty.

## Skill selection

Select the smallest exact local skill set that matches the staged diff. Baseline skill: `code-review-excellence` for any frontend staged diff.

Add conditional skills only when staged paths or diff evidence support them:

- `code-review-and-quality` for complex multi-file, architecture/API boundary, or broad maintainability risk.
- `typescript-code-reviewer` for TypeScript/TSX type changes, `any`/`unknown`, assertions, async/error handling, React hooks or props.
- `secpriv-code-review` for auth, permissions, user data, persistence, XSS/HTML injection, secrets, third-party scripts, analytics, privacy, or dangerous browser APIs.
- Stack-specific skills when directly triggered: `react-dev`, `react-useeffect`, `vercel-react-best-practices`, `web-design-guidelines`, `accessibility-compliance`, `tailwind-design-system`, `tailwind-v4-shadcn`, `ant-design`, `ag-grid`, `react-hook-form-zod`, `internationalization-i18n`, `react-router-declarative-mode`, `react-router-data-mode`, `react-router-framework-mode`, `playwright-best-practices`, `webapp-testing`.

If too many skills match, rank by direct staged evidence, core quality/security/type safety, explicit user request, then weak inference. Keep dropped/deferred skill decisions internal unless they affect verdict/confidence.

## Reviewer waves

Default reviewer angles per selected skill:

- H01: correctness, likely runtime bugs, broken assumptions.
- H02: edge cases, null/undefined/empty states, async failure paths.
- H03: maintainability, architecture fit, readability, local project conventions.
- H04: performance, rendering cost, bundle/runtime risk.
- H05: skill-specific deep pass using the assigned skill checklist.

Replacement reviewers inherit the missing reviewer angle unless the run needs a consensus-check replacement.

## Sub-agent prompt template

Use `templates/subagent-prompt.md` for reviewer prompts and the strict JSON output contract. A counted reviewer pass must follow that template's staged-diff-only, no-unit-test, no-file-edit, and real-sub-agent constraints.

## Output validation and quorum

A reviewer output counts only when:

- it came from an actual sub-agent/custom-agent/tool invocation;
- strict JSON parses;
- reviewer id matches the internal dispatch plan;
- skill slug and skill path match;
- `skill_read=true` or `skill_criteria_injected=true`;
- findings contain path, severity, evidence, why it matters, recommended fix, confidence, and blocking status;
- no unit-test-only advice remains;
- no unstaged changes are used as evidence.

Failed, timed-out, invalid, missing, simulated, or non-skill-grounded outputs must be recorded in the internal reviewer health ledger and replaced if budget remains.

## Aggregation validation

After drafting consolidated findings, run aggregation validator sub-agents internally. They check missed high/critical findings, duplicate merges, quorum math, overclaimed Complete/Approve status, unit-test suggestion leaks, and report-field completeness.

Aggregation validators do not count toward selected skill quorum. Validator results stay internal unless they change verdict/confidence or the user asks for audit log.

## Final user-facing report

Return findings only in Chinese. Use:

`templates/final-report.md`

The final report title should be `# 前端重型已暫存變更審查結果`.

Do not include runtime config, dispatch plan, deferred/dropped skill table, reviewer health ledger, skill quorum status, aggregation validation table, aggregation decision log, reviewer IDs, sub-agent names, skill provenance, or `Found by` unless the user asks for audit log.

## Full workflow reference

Read the full workflow for detailed matrices, schemas, failover rules, aggregation validator instructions, and final report template:

`references/FRONTEND_HEAVY_STAGED_REVIEW_WORKFLOW.md`

If the skill is moved to the planned global folder, the same full workflow should also exist at:

`~/.kilo/workflows/FRONTEND_HEAVY_STAGED_REVIEW_WORKFLOW.md`
