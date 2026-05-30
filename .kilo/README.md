# Kilo Code Global Install Staging

This folder contains files prepared for a future manual move into a global Kilo Code setup.

Planned target location:

```text
~/.kilo/
```

After moving this folder to `~/.kilo`, copy or merge `kilo.jsonc` into the Kilo global config, usually:

```text
~/.kilo/kilo.jsonc
```

Recommended Kilo config:

```jsonc
{
  "skills": {
    "paths": [
      "~/.kilo/skills"
    ]
  },
  "instructions": [
    "~/.kilo/rules/*.md"
  ]
}
```

Contents:

```text
skills/      Kilo-readable Agent Skills, including frontend-task-preflight and frontend-staged-review-workflow.
workflows/   Full workflow reference documents.
rules/       Kilo global instructions/rules for preflight and staged review.
docs/        User-facing Traditional Chinese usage guides and prompt templates.
manifests/   Source manifest and validation notes copied from the project skill catalog.
kilo.jsonc   Example global Kilo config to copy/merge manually.
```

User guides:

```text
docs/FRONTEND_TASK_PREFLIGHT_USAGE.zh-TW.md
docs/FRONTEND_STAGED_REVIEW_WORKFLOW_USAGE.zh-TW.md
```

Important:

- This repository folder is staging only. It does not change your actual Kilo global configuration until you manually move/copy it.
- The current `skills/` set was copied from this project's reviewed skill catalog, then `frontend-task-preflight` was added as a Kilo-facing workflow skill. Review workflow support also includes `frontend-staged-review-workflow`, `audit-code-reviewer`, and `secpriv-code-review`.
- On Linux, move/copy this staged `.kilo` folder to `~/.kilo` first; avoid symlinks unless you have verified Kilo Code follows them correctly.

Review workflow rule:

```text
rules/frontend-staged-review.md
```
