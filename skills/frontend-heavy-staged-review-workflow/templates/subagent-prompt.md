# Heavy staged worker scope adapter

Populate and send the complete [shared reviewer prompt](../../frontend-staged-review-workflow/templates/subagent-prompt.md), including actual contract and criteria text. This adapter is coordinator input, not a path-only worker assignment.

Set `MODE_SCOPE_AND_GIT_IDENTITIES` to:

```text
Mode: heavy staged
Base HEAD/unborn marker: {BASE_ID}
Captured index identity: {INDEX_ID}
Captured blob/old-to-new path map: {BLOB_AND_PATH_MAP}
Review only the supplied cached diff or assigned complete hunk group.
Full-file/package/config context is from captured index blobs, read with
git cat-file blob <captured_sha>; removed/pre-change context is from the pinned base.
Do not re-run a live cached diff or read current worktree files as staged truth.
```

Use the missing independent angle for replacements. The coordinator owns run/attempt/replacement metadata, recovery lineage and raw/normalized references; the worker need not reproduce those fields. Retries and normalization replace attempts and never add independent votes. The configured heavy quorum applies to every required cell, including split groups. Keep other reviewers' findings and validator conclusions out of the packet.
