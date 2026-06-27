# Frontend Preflight Rule

For frontend implementation tasks, use the `frontend-task-preflight` skill before coding.

Applies to:
- React
- TypeScript
- Tailwind
- AG Grid React
- Ant Design
- react-i18next
- react-router-dom
- react-hook-form
- Figma/design-to-code tasks
- UI layout, responsive, accessibility, form, table, routing, or i18n changes

Rules:
1. Do not edit source files during preflight.
2. First summarize the user's goal, known files, design/Figma references, constraints, and assumptions.
3. Read relevant code and nearby patterns before asking questions.
4. Treat Figma as input, not the only truth.
5. If Figma and current code differ, create a gap matrix.
6. Identify applicable skills before planning.
7. Check official docs when library behavior matters.
8. Ask only blocking questions after checking what can be checked from code or docs; user-facing questions must be written in Chinese, while code identifiers, paths, commands, enum values, API fields, and quoted source text may remain unchanged.
9. Present approach options and tradeoffs when there is more than one reasonable path.
10. Write an implementation plan with exact files, task order, verification commands, expected results, risks, and assumptions.
11. Include a naming plan for generated code: variable and function names should be descriptive and domain-specific, avoid abbreviations, and preserve important qualifiers from existing code or business concepts. For example, do not shorten `isSpcTableEmptyVal` to `isEmptyVal`.
12. Do not start implementation until the user explicitly approves.

Full workflow after global move:
`~/.kilo/workflows/FRONTEND_TASK_PREFLIGHT_WORKFLOW.md`

Staging source in this repository:
`.kilo/workflows/FRONTEND_TASK_PREFLIGHT_WORKFLOW.md`
