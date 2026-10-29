# Frontend Branch Review Procedure

Read the [shared contract](../../frontend-staged-review-workflow/references/review-contract.md) for conditional Skill selection, independent coverage, output validation and aggregation.

## Resolve and pin refs

Inputs:

- `source_ref`: user-supplied, otherwise the current branch. Detached HEAD without an explicit source requires clarification.
- `target_ref`: user-supplied, otherwise `master`.
- `fetch_target`: permitted non-destructive fetch when origin/network are available; honor explicit opt-outs and pinned commits.

Never interpolate unquoted user refs. Reject leading `-`; resolve commits with `git rev-parse --verify --end-of-options "${REF}^{commit}"`. Subsequent commands use only resolved object IDs.

When the target is a named shared branch, refresh that exact target on its known remote if allowed. For default `master` on origin, use `git fetch --no-tags origin master` then resolve the fetched commit from `FETCH_HEAD`; fetching this way does not guarantee that `origin/master` was updated. For another requested branch, fetch that branch, never hardcode master. Do not guess a remote for a local-only or ambiguous ref. Do not replace an explicit target commit/tag with a moving remote branch.

Pin the fetched commit immediately. Without fetch, resolve the explicit local target and record freshness as unverified, unless the user deliberately pinned a commit. No forced updates, branch changes, unrelated pruning or pushes.

Capture:

```bash
git rev-parse --show-toplevel
git status --short --branch
git branch --show-current
git remote
git rev-parse --verify --end-of-options "${SOURCE_REF}^{commit}"
git rev-parse --verify --end-of-options "${TARGET_REF}^{commit}"
git merge-base --all "$TARGET_SHA" "$SOURCE_SHA"
```

Assign SOURCE_SHA/TARGET_SHA from the verified resolution (effective fetched target when applicable). Require exactly one merge base. Multiple merge bases need an explicit integration strategy; do not choose an arbitrary base and claim merge readiness. Missing refs, no merge base or unresolved ambiguity means `Incomplete`.

If the source is an ancestor of the target, there is no new contribution; report that no reviewable contribution exists. Equal SHAs also have no contribution. Never equate an empty endpoint diff alone with proof that source is already merged.

## Build the immutable packet

Use the pinned IDs only:

```bash
git log --reverse --format='%H%x09%s' "$MERGE_BASE_SHA..$SOURCE_SHA"
git log --reverse --format='%H%x09%s' "$MERGE_BASE_SHA..$TARGET_SHA"
git --no-pager diff --no-ext-diff --no-textconv --find-renames --name-status -z "$MERGE_BASE_SHA" "$SOURCE_SHA"
git --no-pager diff --no-ext-diff --no-textconv --find-renames --stat "$MERGE_BASE_SHA" "$SOURCE_SHA"
git --no-pager diff --no-ext-diff --no-textconv --check "$MERGE_BASE_SHA" "$SOURCE_SHA"
git --no-pager diff --no-ext-diff --no-textconv --find-renames --full-index "$MERGE_BASE_SHA" "$SOURCE_SHA"
```

Packet fields:

- Root; source/effective target refs and SHAs; merge-base SHA; target freshness.
- Snapshot ID derived from those SHAs and captured patch.
- Source commits and target movement; changed paths/name-status; stat and diff-check result.
- Full patch or assigned complete chunks; indexed/worktree/untracked state marked out of scope.
- Pinned package/lock/config and caller context, exact Skills/criteria, dispatch rows and file/hunk coverage cells.
- Optional integration evidence and its limits; strict JSON and no-unit-test-only-advice rule.

Use `git show "$SOURCE_SHA:path/to/file"` for source context, `git show "$TARGET_SHA:path/to/file"` for target context and merge-base content for deleted/pre-change lines. Current checked-out files are never branch truth. Renames keep old and new path mappings. A finding requires contribution evidence or an interaction the contribution introduces/worsens.

Optional supported `git merge-tree "$MERGE_BASE_SHA" "$TARGET_SHA" "$SOURCE_SHA"` provides limited textual integration evidence without altering the checkout; it is not proof that the actual merge or application works. Never run an actual merge or create a worktree as part of this read-only workflow.

A later ref movement does not invalidate the pinned objects. Continue against them and state reviewed SHAs. A new tip requires a new review run.

## Dispatch, validation and report

Use [the prompt](../templates/subagent-prompt.md). Ledger fields include reviewer/attempt IDs, snapshot/scope, all three SHAs, exact Skill/path, actual loaded/injected criteria/resources, trigger question, distinct angles, assigned hunks and context dependencies.

Each required cell needs two independent completed seats. Retry invalid output once, fresh and stateless; no majority/consensus pass fills missing quorum. Workers use read-only pinned evidence and never see other findings.

Invoke **Frontend Review Validator** for one completed valid aggregation pass. Give it raw outputs, attempt ledger, required/actual coverage, candidate findings and all drop/merge/severity decisions. Missing coverage, inconsistent snapshot, missing quorum or unresolved validator failure means `Incomplete`.

Use [the final report](../templates/final-report.md): source/target/merge-base short SHAs, snapshot ID, verdict, concrete findings and material freshness/integration/visual limits. No findings permits `Approve` only after all gates; unverified target freshness limits the review to the pinned target and must be stated. Operational ledgers remain internal unless requested.

No edits, checkout, switching, staging, commits, pushes, auto-fixes, mutating tests, nested delegation or external PR comments.
