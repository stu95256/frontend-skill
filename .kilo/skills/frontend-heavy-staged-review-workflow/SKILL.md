---
name: frontend-heavy-staged-review-workflow
description: Use when reviewing git-staged frontend changes with a heavy multi-sub-agent process. Reviews only `git diff --cached`, defaults to five valid sub-agent reviewers per selected review skill, supports configurable reviewer counts, replaces failed/invalid/timed-out reviewers, validates skill usage, runs aggregation validator sub-agents, forbids unit-test-only suggestions, and returns a quorum-aware consolidated report.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [frontend, code-review, staged-diff, subagent, heavy-review, quorum, workflow, react, typescript, no-unit-tests, kilo]
    related_skills: [frontend-staged-review-workflow, audit-code-reviewer, code-review-excellence, typescript-code-reviewer, code-review-and-quality, secpriv-code-review, react-dev, react-useeffect, vercel-react-best-practices, web-design-guidelines, accessibility-compliance, tailwind-design-system, tailwind-v4-shadcn, ant-design, ag-grid, react-hook-form-zod, internationalization-i18n, react-router-declarative-mode, react-router-data-mode, react-router-framework-mode, playwright-best-practices, webapp-testing]
---

# Frontend Heavy Staged Review Workflow

Use this skill when the user wants a heavier version of the frontend staged review workflow with many independent reviewer sub-agents and failure-tolerant quorum rules.

## Core contract

1. Review target is only `git diff --cached`.
2. Do not review unstaged changes; list them as out of scope if present.
3. This is review-only: do not modify files, stage files, auto-fix, or commit.
4. Build the dispatch plan before launching reviewer waves.
5. Every selected review skill defaults to five valid reviewer sub-agent outputs.
6. The user can override `reviewers_per_skill`, `min_valid_reviewers_per_skill`, `replacement_budget_per_skill`, `max_selected_skills`, `wave_size`, and `allow_degraded_report`.
7. Failed, timed-out, invalid, missing, or non-skill-grounded reviewers do not count toward quorum.
8. Use replacement reviewer waves until quorum is reached or replacement budget is exhausted.
9. Primary reviewers must be independent; do not show H01-H05 each other's findings.
10. Every counted reviewer must either read `skills/<skill-name>/SKILL.md` or receive a coordinator-injected skill checklist.
11. Run aggregation validator sub-agents on the draft final report.
12. Exclude unit-test-only suggestions.
13. Final report must show dispatch plan, reviewer health ledger, skill quorum status, aggregation validation, consolidated findings, out-of-scope notes, and verdict.

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
```

## Required pre-flight commands

```bash
git rev-parse --show-toplevel
git status --short --branch
git diff --cached --name-only
git diff --cached --stat
git diff --cached
```

Stop if `git diff --cached --name-only` is empty.

## Skill selection

Always consider the core review skills when they exist locally:

- `code-review-excellence`
- `typescript-code-reviewer`
- `code-review-and-quality`
- `secpriv-code-review`

Select conditional frontend skills only when staged paths or diff evidence support them, using exact local skill slugs:

- `react-dev`
- `react-useeffect`
- `vercel-react-best-practices`
- `web-design-guidelines`
- `accessibility-compliance`
- `tailwind-design-system`
- `tailwind-v4-shadcn`
- `ant-design`
- `ag-grid`
- `react-hook-form-zod`
- `internationalization-i18n`
- `react-router-declarative-mode`
- `react-router-data-mode`
- `react-router-framework-mode`
- `playwright-best-practices`
- `webapp-testing`

If too many skills match, rank by direct staged evidence, core quality/security/type safety, user request, then weak inference. Record deferred or dropped skills in the final report.

## Reviewer waves

Default reviewer angles per selected skill:

- H01: correctness, likely runtime bugs, broken assumptions.
- H02: edge cases, null/undefined/empty states, async failure paths.
- H03: maintainability, architecture fit, readability, local project conventions.
- H04: performance, rendering cost, bundle/runtime risk.
- H05: skill-specific deep pass using the assigned skill checklist.

Replacement reviewers inherit the missing reviewer angle unless the run needs a consensus-check replacement.

## Output validation and quorum

A reviewer output counts only when:

- strict JSON parses;
- reviewer id matches the dispatch plan;
- skill slug and skill path match;
- `skill_read=true` or `skill_criteria_injected=true`;
- findings contain path, severity, evidence, why it matters, recommended fix, confidence, and blocking status;
- no unit-test-only advice remains;
- no unstaged changes are used as evidence.

Failed, timed-out, invalid, missing, or non-skill-grounded outputs must be recorded in the reviewer health ledger and replaced if budget remains.

## Aggregation validation

After drafting the consolidated report, run aggregation validator sub-agents. They check missed high/critical findings, duplicate merges, quorum math, overclaimed Complete/Approve status, unit-test suggestion leaks, and report-field completeness.

Aggregation validators do not count toward selected skill quorum.

## Required final report sections

- Runtime config
- Dispatch Plan
- Deferred / Dropped Skill Decisions
- Reviewer Health Ledger
- Skill Quorum Status
- Aggregation Validation
- Consolidated Findings
- Aggregation Decision Log
- Out of Scope
- Suggested Fix Order

## Kilo Code usage

If this skill is installed globally for Kilo Code, pair it with the global rule file:

`~/.kilo/rules/frontend-heavy-staged-review.md`

The Kilo global config should point `skills.paths` at:

`~/.kilo/skills`

and `instructions` at:

`~/.kilo/rules/*.md`

## Full workflow reference

Read the full workflow for detailed matrices, schemas, failover rules, aggregation validator instructions, and final report template:

`references/FRONTEND_HEAVY_STAGED_REVIEW_WORKFLOW.md`

If the skill is moved to the planned global folder, the same full workflow should also exist at:

`~/.kilo/workflows/FRONTEND_HEAVY_STAGED_REVIEW_WORKFLOW.md`
