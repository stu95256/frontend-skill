# Frontend Branch Review Workflow — Research Notes

## Design basis

This workflow adapts the project's `frontend-staged-review-workflow` from index-based review to commit/ref-based pre-merge review.

Key Git semantics used:

- `git merge-base <target> <source>` identifies the common ancestor used to isolate source-branch contribution.
- `git diff <merge-base> <source>` is equivalent in intent to the common `git diff <target>...<source>` review range while making the pinned merge base explicit.
- `git diff <target>..<source>` compares endpoint trees and can include effects from target-only changes when histories diverged, so it is not used as the branch-contribution definition.
- Refs are resolved to immutable commit SHAs before dispatch so moving branches cannot silently change reviewer scope.
- `git show <sha>:<path>` supplies branch-specific file context without checkout.
- `git merge-tree` may provide optional conflict/integration evidence without changing the working tree, but it is not treated as proof that a future merge will succeed.

Workflow/quality sources:

- Existing local `frontend-staged-review-workflow` for skill selection, real-sub-agent quorum, strict JSON, validation, aggregation, no-unit-test policy, and concise Chinese findings-only output.
- Git documentation concepts: revisions, merge-base, diff ranges, diff rename detection, and merge-tree.
- GitHub code-review conventions for reviewing `base...head` changes before merge.
- Local `audit-code-reviewer`, `code-review-excellence`, `typescript-code-reviewer`, and stack-specific frontend skills.

## Deliberate decisions

1. Default target is `master` because that is the user's requested merge destination, while allowing an explicit target override.
2. A freshly fetched `origin/master` is preferred when available; freshness status is recorded when fetch cannot run.
3. Dirty working trees do not block branch review because the review packet is commit-SHA-based, but all uncommitted state is explicitly out of scope.
4. The workflow never checks out the source branch, making it safe to review local or remote refs without disturbing the user's current worktree.
5. Findings must be attributable to the source contribution or its interaction with the pinned target; target-only defects are excluded.
6. The final report includes source and target short SHAs so the user can identify the reviewed snapshot without exposing reviewer internals.
