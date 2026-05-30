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
4. Before dispatching reviewers, run and summarize:
   - `git status --short --branch`
   - `git diff --cached --name-only`
   - `git diff --cached --stat`
   - `git diff --cached`
5. If there are no staged files, stop and tell the user there is nothing staged to review.
6. Build a dispatch plan before spawning reviewer sub-agents.
7. Use exact local skill names only; do not use generic labels such as "React skill".
8. Every selected review skill must have at least two independent valid reviewer passes.
9. Always exclude unit-test-only suggestions; do not recommend unit tests or test coverage changes.
10. Validate reviewer outputs before aggregation.
11. Final report must include dispatch plan, reviewer ledger, consolidated findings, path, severity, evidence, recommended fix, out-of-scope notes, and verdict.

Full workflow after global move:
`~/.kilo/workflows/FRONTEND_STAGED_REVIEW_WORKFLOW.md`

Staging source in this repository:
`.kilo/workflows/FRONTEND_STAGED_REVIEW_WORKFLOW.md`
