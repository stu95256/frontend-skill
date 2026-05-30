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
skills/      Kilo-readable Agent Skills, including frontend-task-preflight, frontend-debug-workflow, frontend-staged-review-workflow, and frontend-heavy-staged-review-workflow.
workflows/   Full workflow reference documents.
rules/       Kilo global instructions/rules for preflight, debug, staged review, and heavy staged review.
docs/        User-facing Traditional Chinese usage guides and prompt templates.
manifests/   Source manifest and validation notes copied from the project skill catalog, plus Kilo staging manifest.
kilo.jsonc   Example global Kilo config to copy/merge manually.
```

User guides:

```text
docs/FRONTEND_TASK_PREFLIGHT_USAGE.zh-TW.md
docs/FRONTEND_STAGED_REVIEW_WORKFLOW_USAGE.zh-TW.md
docs/FRONTEND_HEAVY_STAGED_REVIEW_WORKFLOW_USAGE.zh-TW.md
docs/FRONTEND_DEBUG_WORKFLOW_USAGE.zh-TW.md
```

Important:

- This repository folder is staging only. It does not change your actual Kilo global configuration until you manually move/copy it.
- The current `skills/` set was copied from this project's reviewed skill catalog, then Kilo-facing workflow skills were added for frontend task preflight, debug, staged review, and heavy staged review.
- Debug workflow support includes `frontend-debug-workflow`, `systematic-debugging`, `react-dev`, `react-useeffect`, `typescript-advanced-types`, `browser-testing-with-devtools`, `webapp-testing`, and stack-specific frontend skills.
- Review workflow support includes `frontend-staged-review-workflow`, `frontend-heavy-staged-review-workflow`, `audit-code-reviewer`, and `secpriv-code-review`.
- Heavy staged review defaults to five valid reviewer sub-agents per selected review skill, supports replacement reviewers for failed/invalid/timed-out outputs, and runs aggregation validator sub-agents before finalizing.
- On Linux, move/copy this staged `.kilo` folder to `~/.kilo` first; avoid symlinks unless you have verified Kilo Code follows them correctly.

Review workflow rules:

```text
rules/frontend-staged-review.md
rules/frontend-heavy-staged-review.md
rules/frontend-debug.md
```
