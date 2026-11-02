---
name: using-agent-skills
description: Use when choosing which installed frontend engineering skills apply to a task.
license: MIT
---

# Using Agent Skills

Use Copilot's skill discovery instead of loading the entire catalog. Read only the smallest set whose descriptions match the current task.

## Routing

- Clarify a new feature or design: `brainstorming`.
- Plan work: `planning-and-task-breakdown` or `writing-plans`.
- Execute an approved plan: `executing-plans`; add `subagent-driven-development` when `agent/runSubagent` is enabled.
- Debug a frontend defect: `systematic-debugging`.
- Implement frontend UI: `frontend-ui-engineering` plus only the detected framework/library skills.
- Unit/integration tests: `test-driven-development`, `vitest`, and `javascript-testing-patterns`, according to the installed versions and test environment.
- Review staged work: `frontend-staged-review-workflow` or `frontend-heavy-staged-review-workflow`.
- Review a branch contribution: `frontend-branch-review-workflow`.
- Generate a staged commit subject: `frontend-staged-commit-message`.
- Finish a branch: `finishing-a-development-branch` and `verification-before-completion`.

## Selection Rules

1. Inspect manifests and nearby code before selecting technology-specific skills.
2. Prefer exact skills such as `react-router`, `ag-dev`, `ant-design`, `react-hook-form-zod`, or `internationalization-i18n` over generic assumptions.
3. Load process skills before implementation skills because they define sequencing and verification.
4. Resolve a skill through diagnostics or an actual supported/configured location, then read its real `SKILL.md` and required resources. `~/.copilot/skills` is one personal location; project `.github/skills` and supported plugin contributions can also supply skills. File existence alone is not proof of automatic discovery.
5. A skill supplies procedures and resources; it is not itself a custom agent and does not grant tools. Use discovered custom agents for tool restrictions, handoffs, and named subagent roles; catalog files are installed under `~/.copilot/agents`, while Local UI-created agents may use Profile storage. Check [using-vscode-chat](../using-vscode-chat/SKILL.md) for discovery and harness boundaries.

## Verification

Before acting, ensure each selected skill directly matches observed task evidence and that no required linked resource is missing.
