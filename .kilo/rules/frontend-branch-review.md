# Frontend Branch Review Rule

When the user asks to review what a frontend source branch will contribute before merging into `master` or another target branch, use `frontend-branch-review-workflow`.

Applies to:

- “review this branch before merging to master” requests;
- local or remote branch refs;
- React, TypeScript, Tailwind, AG Grid React, Ant Design, react-i18next, react-router-dom, react-hook-form, accessibility, responsive, UI, form, table, routing, i18n, and browser-visible frontend changes;
- requests for multiple independent reviewer sub-agents before merge.

Rules:

1. Default `target_ref` to `master`; use the user-provided `source_ref`, or the current branch only when source is omitted and HEAD is attached.
2. Prefer a freshly fetched `origin/master` when `origin` and network access are available; otherwise record target freshness internally.
3. Resolve source, effective target, and merge base to immutable SHAs before dispatch.
4. Review only `git diff --find-renames <merge_base_sha> <source_sha>`.
5. Do not use current working-tree, staged, untracked, or target-only changes as source-branch findings.
6. For branch-specific file context, use `git show <source_sha>:<path>` or `git show <target_sha>:<path>`; do not trust the current worktree when it represents another ref.
7. Do not checkout, switch, merge, rebase, reset, modify, stage, auto-fix, or commit.
8. Stop if refs cannot resolve, there is no merge base, the branch contribution is empty, or source is ambiguous in detached HEAD.
9. Build an internal dispatch plan before spawning reviewers; do not show it unless the user asks for the audit log.
10. Reviewer passes must come from actual Kilo sub-agents/custom agents or equivalent tooling. The coordinator must not simulate reviewers.
11. If no real sub-agent mechanism is available, return `Incomplete`; do not perform main-agent-only review.
12. Use exact local skill names. Every selected review skill requires at least two independent valid reviewers.
13. Require reviewer outputs to match the pinned source, target, and merge-base SHAs.
14. Exclude unit-test-only suggestions and test-coverage follow-ups.
15. Final report must be findings-only and written in Chinese. Include the source/target snapshot, verdict, path, severity, evidence, impact, and recommended fix; omit reviewer/sub-agent/skill provenance.

Full workflow after global move:
`~/.kilo/workflows/FRONTEND_BRANCH_REVIEW_WORKFLOW.md`

Staging source:
`.kilo/workflows/FRONTEND_BRANCH_REVIEW_WORKFLOW.md`
