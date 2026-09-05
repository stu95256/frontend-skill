# Kilo Code Staging Manifest

Generated: 2026-09-02

- Staging source: `frontend-skill/.kilo`
- Planned global target: `~/.kilo`
- Skill directories included: **67**
- Portable catalog mirrors: **65**
- Kilo-only workflow wrappers: `frontend-task-preflight`, `frontend-heavy-staged-review-workflow`

## Required Kilo config

```jsonc
{
  "skills": { "paths": ["~/.kilo/skills"] },
  "instructions": ["~/.kilo/rules/*.md"]
}
```

## Workflow documents

- `workflows/FRONTEND_TASK_PREFLIGHT_WORKFLOW.md`
- `workflows/FRONTEND_DEBUG_WORKFLOW.md`
- `workflows/FRONTEND_STAGED_REVIEW_WORKFLOW.md`
- `workflows/FRONTEND_BRANCH_REVIEW_WORKFLOW.md`
- `workflows/FRONTEND_HEAVY_STAGED_REVIEW_WORKFLOW.md`

## Included skills

- `accessibility`
- `accessibility-compliance`
- `ag-dev`
- `ag-update`
- `ant-design`
- `antd`
- `brainstorming`
- `browser-testing-with-devtools`
- `code-review-and-quality`
- `context-engineering`
- `design-system-patterns`
- `dispatching-parallel-agents`
- `documentation-and-adrs`
- `executing-plans`
- `finishing-a-development-branch`
- `frontend-branch-review-workflow`
- `frontend-debug-workflow`
- `frontend-design`
- `frontend-heavy-staged-review-workflow`
- `frontend-staged-commit-message`
- `frontend-staged-review-workflow`
- `frontend-task-preflight`
- `frontend-ui-engineering`
- `incremental-implementation`
- `internationalization-i18n`
- `javascript-testing-patterns`
- `openapi-typescript`
- `performance-optimization`
- `planning-and-task-breakdown`
- `playwright-best-practices`
- `playwright-cli`
- `qa-test-planner`
- `react-dev`
- `react-doctor`
- `react-hook-form-zod`
- `react-router`
- `react-state-management`
- `react-useeffect`
- `receiving-code-review`
- `requesting-code-review`
- `responsive-design`
- `secpriv-code-review`
- `security-and-hardening`
- `shadcn`
- `skill-creator`
- `skill-scanner`
- `source-driven-development`
- `spec-driven-development`
- `subagent-driven-development`
- `systematic-debugging`
- `tailwind-design-system`
- `test-driven-development`
- `typescript-advanced-types`
- `typescript-code-reviewer`
- `using-agent-skills`
- `using-git-worktrees`
- `using-superpowers`
- `vercel-composition-patterns`
- `vercel-react-best-practices`
- `vercel-react-view-transitions`
- `verification-before-completion`
- `vitest`
- `web-artifacts-builder`
- `web-design-guidelines`
- `webapp-testing`
- `writing-plans`
- `writing-skills`

## Verification

Run from the repository root:

```bash
python scripts/validate_skill_catalog.py
```

Do not install this staging directory globally until the validation report is green.
