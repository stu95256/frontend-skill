# Frontend Heavy Staged Review Rule

For heavyweight frontend code review tasks where the user asks to review already staged changes with many sub-agents, use the `frontend-heavy-staged-review-workflow` skill.

Applies to:
- Review of `git add` / staged changes.
- `git diff --cached` review.
- Requests for heavy review, many sub-agents, 5 reviewers per review skill, configurable reviewer counts, or failure-tolerant reviewer replacement.
- React, TypeScript, Tailwind, AG Grid React, Ant Design, react-i18next, react-router-dom, react-hook-form, accessibility, responsive, UI, form, table, routing, i18n, and browser-visible frontend changes.

Rules:
1. Review target is only `git diff --cached`.
2. Do not review unstaged changes; mention them as out of scope if present.
3. Do not modify files, stage files, run auto-fixes, or commit.
4. Before dispatching reviewers, run and summarize:
   - `git rev-parse --show-toplevel`
   - `git status --short --branch`
   - `git diff --cached --name-only`
   - `git diff --cached --stat`
   - `git diff --cached`
5. If there are no staged files, stop and tell the user there is nothing staged to review.
6. Build a runtime config and dispatch plan before spawning reviewer sub-agents.
7. Default to `reviewers_per_skill: 5`; allow explicit user overrides.
8. Use exact local skill names only; do not use generic labels such as "React skill".
9. Every selected review skill must reach the configured valid reviewer quorum.
10. Failed, timed-out, invalid, missing, or non-skill-grounded reviewers do not count toward quorum.
11. Use replacement reviewer waves until quorum is reached or replacement budget is exhausted.
12. Primary reviewers must stay independent; do not feed H01-H05 each other's findings.
13. A counted reviewer must either read `skills/<skill-name>/SKILL.md` or receive coordinator-injected skill criteria.
14. Run aggregation validator sub-agents before finalizing the report.
15. Always exclude unit-test-only suggestions; do not recommend unit tests or test coverage changes.
16. Final report must include runtime config, dispatch plan, reviewer health ledger, skill quorum status, aggregation validation, consolidated findings, path, severity, evidence, recommended fix, out-of-scope notes, and verdict.
17. Do not claim Complete or Approve if required quorum or aggregation validation failed.

Full workflow after global move:
`~/.kilo/workflows/FRONTEND_HEAVY_STAGED_REVIEW_WORKFLOW.md`

Staging source in this repository:
`.kilo/workflows/FRONTEND_HEAVY_STAGED_REVIEW_WORKFLOW.md`
