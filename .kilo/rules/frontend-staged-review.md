# Frontend Staged Review Rule

For frontend code review tasks where the user asks to review already staged changes, use the `frontend-staged-review-workflow` skill.

Applies to:
- Review of `git add` / staged changes.
- `git diff --cached` review.
- React, TypeScript, Tailwind, AG Grid React, Ant Design, react-i18next, react-router-dom, react-hook-form, accessibility, responsive, UI, form, table, routing, i18n, and browser-visible frontend changes.
- Requests to use multiple reviewer sub-agents for frontend code review.

Rules:
1. Review target is only `git diff --cached`.
2. Do not review unstaged changes; mention them as out of scope if present.
3. Do not modify files, stage files, run auto-fixes, or commit.
4. Before dispatching reviewers, run and capture internally:
   - `git status --short --branch`
   - `git diff --cached --name-only`
   - `git diff --cached --stat`
   - `git diff --cached`
5. If there are no staged files, stop and tell the user there is nothing staged to review.
6. Build an internal dispatch plan before spawning reviewer sub-agents; do not show it unless the user asks for the audit log.
7. Reviewer passes must come from actual Kilo sub-agents/custom agents or equivalent sub-agent tooling; the coordinator/main agent must not simulate multiple reviewers.
8. If no real sub-agent mechanism is available, stop and return `Incomplete`; do not perform a main-agent-only review.
9. Use exact local skill names only; do not use generic labels such as "React skill".
10. Every selected review skill must have at least two independent valid reviewer passes.
11. Always exclude unit-test-only suggestions; do not recommend unit tests or test coverage changes.
12. Validate reviewer outputs before aggregation.
13. Final report must be findings-only and written in Chinese unless the user explicitly asks for the audit log; include path, severity, evidence, recommended fix, and verdict, but omit reviewer/sub-agent/skill provenance from the user-facing output.
14. Final user-facing report must be written in Chinese; keep code identifiers, paths, commands, enum values, and quoted source text unchanged when appropriate.

Full workflow after global move:
`~/.kilo/workflows/FRONTEND_STAGED_REVIEW_WORKFLOW.md`

Staging source in this repository:
`.kilo/workflows/FRONTEND_STAGED_REVIEW_WORKFLOW.md`
