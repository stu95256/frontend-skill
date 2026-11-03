# Branch worker scope adapter

Populate and send the complete [shared reviewer prompt](../../frontend-staged-review-workflow/templates/subagent-prompt.md), including actual contract and criteria text. This adapter is coordinator input, not a path-only worker assignment.

Set `MODE_SCOPE_AND_GIT_IDENTITIES` to:

```text
Mode: branch
Source ref/SHA: {SOURCE_REF} / {SOURCE_SHA}
Target ref/SHA: {TARGET_REF} / {TARGET_SHA}
Merge-base SHA: {MERGE_BASE_SHA}
Pinned file/blob and old-to-new path map: {BLOB_AND_PATH_MAP}
Review only the supplied merge-base-to-source contribution or assigned complete
hunk group. Additional context uses git show <pinned_sha>:<path>.
Target-only changes are integration context; a finding needs an interaction
introduced/worsened by the contribution. Current worktree, index and untracked
files are out of scope. Removed/pre-change evidence comes from the merge base.
```

The coordinator preserves all three SHAs in the packet/ledger and verifies evidence origins against them. Snapshot identity binds those SHAs; the worker need not redundantly echo them. Explicitly conflicting echoes still invalidate integrity. Later ref movement never silently changes the assignment. Two independent completed seats remain required for every selected risk/coverage cell, including split groups.
