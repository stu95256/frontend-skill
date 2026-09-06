---
name: using-agent-skills
description: Use when choosing which installed frontend engineering skills apply to a task.
license: MIT
---

# Using Agent Skills

Use Copilot's skill discovery instead of loading the entire catalog. Read only the smallest set whose descriptions match the current task.

## Routing

- Clarify a new feature or design: `brainstorming`, then `frontend-task-preflight`.
- Plan work: `planning-and-task-breakdown` or `writing-plans`.
- Execute an approved plan: `executing-plans`; add `subagent-driven-development` when `agent/runSubagent` is enabled.
- Debug a frontend defect: `frontend-debug-workflow` and `systematic-debugging`.
- Implement frontend UI: `frontend-ui-engineering` plus only the detected framework/library skills.
- Test: `test-driven-development`; use `vitest`, `playwright-cli`, `playwright-best-practices`, or `webapp-testing` when their tooling is present.
- Review staged work: `frontend-staged-review-workflow` or `frontend-heavy-staged-review-workflow`.
- Review a branch contribution: `frontend-branch-review-workflow`.
- Generate a staged commit subject: `frontend-staged-commit-message`.
- Finish a branch: `finishing-a-development-branch` and `verification-before-completion`.

## Selection Rules

1. Inspect manifests and nearby code before selecting technology-specific skills.
2. Prefer exact skills such as `react-router`, `ag-dev`, `ant-design`, `react-hook-form-zod`, or `internationalization-i18n` over generic assumptions.
3. Load process skills before implementation skills because they define sequencing and verification.
4. Do not cite or depend on a skill unless Copilot diagnostics shows it loaded or `~/.copilot/skills/<name>/SKILL.md` exists.
5. A skill supplies procedures and resources; it is not itself a custom agent. Use custom agents under `~/.copilot/agents` for tool restrictions, handoffs, and named subagent roles.

## Verification

Before acting, ensure each selected skill directly matches observed task evidence and that no required linked resource is missing.
