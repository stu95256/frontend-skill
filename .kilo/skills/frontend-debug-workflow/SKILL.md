---
name: frontend-debug-workflow
description: Use when the user gives frontend code paths plus a bug, runtime symptom, console error, TypeScript error, failing test, or broken UI behavior and wants the agent to debug and fix the code. The workflow reads the specified files and nearby usage, gathers evidence, forms a root-cause hypothesis, selects exact local frontend skills, applies a minimal fix, verifies it, and reports a replayable debug record.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [frontend, debugging, root-cause, workflow, react, typescript, browser, verification, kilo]
    related_skills: [systematic-debugging, incremental-implementation, verification-before-completion, source-driven-development, react-dev, react-useeffect, react-state-management, typescript-advanced-types, typescript-code-reviewer, react-router-declarative-mode, react-router-data-mode, react-router-framework-mode, ant-design, antd, ag-grid, react-hook-form-zod, internationalization-i18n, tailwind-design-system, tailwind-v4-shadcn, responsive-design, accessibility-compliance, browser-testing-with-devtools, webapp-testing, playwright-best-practices, performance-optimization, vercel-react-best-practices, security-and-hardening, secpriv-code-review]
---

# Frontend Debug Workflow

Use this skill when the user provides one or more frontend code locations and a problem, then asks you to debug and fix their code.

## Core contract

1. Treat the provided paths and symptoms as a debug packet.
2. Read the specified files and nearby usage before fixing.
3. Gather evidence: error messages, reproduction, stack trace, browser console/network/DOM, tests, typecheck, git diff, or source lines.
4. Trace data/control/render flow until you can explain why the problem happens.
5. Select exact local skills from `skills/<skill-name>/SKILL.md` based on the root cause area.
6. Write a minimal fix plan before edits.
7. Fix the root cause, not only the symptom.
8. Verify with commands or browser/manual reproduction that match the original problem.
9. Return a debug report with inspected files, evidence, root cause, skills used, changes, verification, and remaining risks.

## When to use

Use when the user says any of:

- 「debug 我的 code」
- 「這些檔案有問題，幫我修」
- 「這段前端 code 為什麼壞掉」
- 「console error / TypeScript error / UI bug / route bug / form bug / table bug」
- 「我會給你一段或多段程式碼位置和問題，請查原因並修正」

Do not use for:

- Review-only staged diff tasks; use `frontend-staged-review-workflow` or `frontend-heavy-staged-review-workflow`.
- Pure planning before implementation; use frontend task preflight patterns instead.
- Backend-only debugging with no frontend behavior.

## Required workflow

### 0. Intake

Record:

- Problem statement.
- User-provided files / symbols / routes.
- Error messages, stack traces, screenshots, reproduction steps.
- Constraints and assumptions.

If the user gives a path but not all details, inspect first; ask only when blocked.

### 1. Read code and nearby usage

Must inspect:

- The provided files and relevant line ranges.
- Imports/exports.
- Call sites and parent/child components.
- Similar working examples in the codebase.
- Route, form, grid, i18n, style, API, or state files touched by the flow.

### 2. Gather evidence

Use the narrowest reliable evidence source:

- TypeScript: targeted typecheck or relevant compiler error.
- Tests: original failing command.
- Browser: console/network/DOM/reproduction steps.
- Source: exact path/line evidence and nearby working pattern.
- Git: recent diffs/log when regression timing matters.

### 3. Trace flow and state root cause

Before editing, write a hypothesis:

```markdown
I think the root cause is ... because ...
Evidence:
- E1 ...
- E2 ...
Disconfirming check:
- ...
```

No fixes are allowed before this root-cause gate.

### 4. Select local skills

Always include `systematic-debugging` conceptually for bugs. Add exact local skills as needed:

| Evidence / problem area | Use exact local skills |
|---|---|
| Minimal root-cause fix and verification | `incremental-implementation`, `verification-before-completion` |
| Need official/source docs | `source-driven-development` |
| React component/state | `react-dev`, `react-state-management` |
| `useEffect`, stale closure, cleanup, async sync | `react-useeffect` |
| TypeScript / TSX / generics / unsafe assertions | `typescript-advanced-types`, `typescript-code-reviewer` |
| Routing/navigation/loaders/actions | `react-router-declarative-mode`, `react-router-data-mode`, `react-router-framework-mode` |
| Ant Design | `ant-design`, `antd` |
| AG Grid | `ag-grid` |
| React Hook Form / Zod | `react-hook-form-zod` |
| i18n | `internationalization-i18n` |
| Tailwind / responsive / tokens | `tailwind-design-system`, `tailwind-v4-shadcn`, `responsive-design` |
| A11y/focus/keyboard | `accessibility-compliance` |
| Browser-visible behavior | `browser-testing-with-devtools`, `webapp-testing` |
| Playwright trace/E2E | `playwright-best-practices` |
| Performance/rendering | `performance-optimization`, `vercel-react-best-practices` |
| Security/privacy | `security-and-hardening`, `secpriv-code-review` |

Do not cite a skill unless `skills/<skill-name>/SKILL.md` exists.

### 5. Minimal fix plan

Before editing, record:

- Root cause to fix.
- Exact files to change.
- Exact intended changes.
- Verification commands / manual steps.
- Out-of-scope items.

### 6. Implement

Rules:

- Prefer precise patches.
- Do not hide errors with `as any`, eslint disables, empty catch, or arbitrary `setTimeout` unless evidence proves that is the correct API pattern.
- Do not bundle unrelated refactors.
- If the fix fails, return to evidence/hypothesis instead of stacking guesses.

### 7. Verify

Run verification that matches the original bug. Examples:

- `npm run typecheck`
- `npm run lint`
- targeted test command
- Playwright / browser reproduction
- manual checklist when no automated route exists

### 8. Final report

Return:

- Problem summary.
- Files inspected.
- Evidence log.
- Root cause.
- Skills used and why.
- Changes made.
- Verification results.
- Remaining risks / skipped checks.

## Full reference

See `references/FRONTEND_DEBUG_WORKFLOW.md` for the full workflow, evidence templates, skill matrix, gates, and completion criteria.
