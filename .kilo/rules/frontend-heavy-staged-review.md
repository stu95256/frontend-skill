# Frontend Heavy Staged Review Rule

For heavyweight frontend code review tasks where the user asks to review already staged changes with many sub-agents, use the `frontend-heavy-staged-review-workflow` skill.

Applies to:
- Review of `git add` / staged changes.
- `git diff --cached` review.
- Requests for heavy review, many sub-agents, 5 reviewers per review skill, configurable reviewer counts, or failure-tolerant reviewer replacement.
- React, TypeScript, Tailwind, AG Grid React, Ant Design, react-i18next, react-router-dom, react-hook-form, accessibility, responsive, UI, form, table, routing, i18n, and browser-visible frontend changes.

Rules:
1. Review target is only `git diff --cached`.
2. Do not review unstaged changes; record them internally as out of scope if present.
3. Do not modify files, stage files, run auto-fixes, or commit.
4. Before dispatching reviewers, run and capture internally:
   - `git rev-parse --show-toplevel`
   - `git status --short --branch`
   - `git diff --cached --name-only`
   - `git diff --cached --stat`
   - `git diff --cached`
5. If there are no staged files, stop and tell the user there is nothing staged to review.
6. Build runtime config and an internal dispatch plan before spawning reviewer sub-agents; do not show them unless the user asks for the audit log.
7. Reviewer passes must come from actual Kilo sub-agents/custom agents or equivalent sub-agent tooling; the coordinator/main agent must not simulate multiple reviewers.
8. If no real sub-agent mechanism is available, stop and return `Incomplete`; do not perform a main-agent-only review.
9. Default to `reviewers_per_skill: 5`; allow explicit user overrides.
10. Use exact local skill names only; do not use generic labels such as "React skill".
11. Every selected review skill must reach the configured valid reviewer quorum.
12. Failed, timed-out, invalid, missing, simulated, or non-skill-grounded reviewers do not count toward quorum.
13. Use replacement reviewer waves until quorum is reached or replacement budget is exhausted.
14. Primary reviewers must stay independent; do not feed H01-H05 each other's findings.
15. A counted reviewer must either read `skills/<skill-name>/SKILL.md` or receive coordinator-injected skill criteria.
16. Run aggregation validator sub-agents internally before finalizing the findings.
17. Always exclude unit-test-only suggestions; do not recommend unit tests or test coverage changes.
18. Final report must be findings-only and written in Chinese unless the user explicitly asks for the audit log; include path, severity, evidence, recommended fix, and verdict, but omit runtime config, dispatch plan, reviewer ledgers, quorum tables, reviewer/sub-agent/skill provenance, and `Found by` from the user-facing output.
19. Final user-facing report must be written in Chinese; keep code identifiers, paths, commands, enum values, and quoted source text unchanged when appropriate.
20. Do not claim Complete or Approve if required quorum or aggregation validation failed.

Full workflow after global move:
`~/.kilo/workflows/FRONTEND_HEAVY_STAGED_REVIEW_WORKFLOW.md`

Staging source in this repository:
`.kilo/workflows/FRONTEND_HEAVY_STAGED_REVIEW_WORKFLOW.md`
