---
name: Frontend Staged Commit Message
description: Generate one commit subject from only the staged frontend diff.
target: vscode
tools: [read, search, execute]
---

# Frontend Staged Commit Message

Follow [frontend-staged-commit-message](../skills/frontend-staged-commit-message/SKILL.md).

1. Use only read-only Git commands.
2. Define scope exclusively as `git diff --cached`; stop if it is empty.
3. Infer one Conventional Commit subject from the staged behavior change, not filenames alone.
4. Return exactly one concise English subject line, with no code fence, explanation, body, or trailing period.
5. Never edit, stage, commit, push, checkout, reset, merge, or rebase.
