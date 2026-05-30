# Frontend Debug Rule

For frontend debugging tasks where the user provides code paths, symbols, routes, components, errors, symptoms, or reproduction steps and wants the agent to debug and fix the code, use the `frontend-debug-workflow` skill.

Applies to:
- React, TypeScript, TSX, Tailwind, AG Grid React, Ant Design, react-i18next, react-router-dom, react-hook-form.
- Browser-visible frontend runtime bugs.
- Console errors, TypeScript errors, failing frontend tests, broken UI interactions, route/form/table/i18n/style bugs.
- Requests like 「debug 我的 code」, 「查為什麼壞掉並修」, 「我會給檔案位置和問題」.

Rules:
1. Treat user-provided paths as starting points, not the full investigation scope.
2. Read specified files and nearby usage before edits.
3. Gather evidence and record it: error messages, stack traces, commands, browser console/network/DOM, source lines, or working examples.
4. Do not fix before stating a root-cause hypothesis.
5. Select exact local skills based on the problem area; do not cite generic or nonexistent skills.
6. Write a minimal fix plan before editing.
7. Fix the root cause, not merely the symptom.
8. Do not hide errors with `as any`, eslint disables, empty catch, arbitrary timeout, or blanket optional chaining unless evidence proves that is the correct API pattern.
9. Verify with commands or browser/manual reproduction that match the original bug.
10. Final response must include files inspected, evidence, root cause, skills used, changes made, verification, and remaining risks.

Full workflow after global move:
`~/.kilo/workflows/FRONTEND_DEBUG_WORKFLOW.md`

Staging source in this repository:
`.kilo/workflows/FRONTEND_DEBUG_WORKFLOW.md`
