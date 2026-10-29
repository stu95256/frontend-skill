# Research Notes: Frontend Staged Review Workflow

Research date: 2026-05-29

Historical source notes; operational rules were revised on 2026-10-29 in the [shared review contract](review-contract.md). The contract is authoritative for snapshot identity, current routing, coverage cells and validation. The external sources below were not re-researched in that follow-up.

## Goal

Create a frontend-focused review workflow for already staged changes (`git diff --cached`) that uses many independent sub-agents, requires at least two sub-agents for every selected review skill, records each reviewer result, and produces a consolidated report with path, severity, and recommended fix.

Unit test recommendations are intentionally excluded by user requirement.

## External Sources Checked

| Source | URL | Relevant workflow idea used |
|---|---|---|
| Anthropic Claude Code subagents docs | https://docs.anthropic.com/en/docs/claude-code/sub-agents | Use specialized sub-agents such as code reviewers with independent context; sub-agents can be configured for code quality/security/best-practice review and used proactively after code changes. |
| GitHub Docs: reviewing proposed changes in a pull request | https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/reviewing-proposed-changes-in-a-pull-request | Understand the purpose of the change, review changed files, track viewed/progress state, then submit a summary with approve/request-changes style verdict. |
| Google Engineering Practices: The Standard of Code Review | https://google.github.io/eng-practices/review/reviewer/standard.html | Prefer approving changes that improve overall code health even if not perfect; review should optimize code health and maintainability. |
| Google Engineering Practices: What to look for in a code review | https://google.github.io/eng-practices/review/reviewer/looking-for.html | Review design, functionality, complexity, naming, comments, style, consistency, and documentation; this workflow intentionally excludes unit-test advice per project requirement. |
| Google Engineering Practices: How to write code review comments | https://google.github.io/eng-practices/review/reviewer/comments.html | Comments should explain why an issue matters and provide guidance without rewriting the solution for the author. |
| SmartBear code review best practices | https://smartbear.com/learn/code-review/best-practices-for-peer-code-review/ | Findings need to be logged/tracked so review defects do not disappear in discussion. This maps to the reviewer ledger and consolidated findings table. |
| Local staged skill: `code-review-and-quality` | `skills/code-review-and-quality/SKILL.md` | Coordinator should gather minimal shared context, launch independent review passes, wait for results, then merge findings by severity and preserve residual risk. |
| Local staged skill: `secpriv-code-review` | `skills/secpriv-code-review/SKILL.md` | Security/privacy review benefits from detector-validator methodology, high-confidence findings, and explicit structured output. |

## Workflow Decisions

1. **Staged diff as source of truth**
   - Use `git diff --cached --name-only`, `git diff --cached --stat`, and `git diff --cached`.
   - Do not review unstaged changes.

2. **Two sub-agents per selected skill**
   - One reviewer pass can miss issues or overfit to a viewpoint.
   - The workflow requires at least two independent passes for every selected skill.
   - The two reviewers get the same diff but different angle prompts.

3. **Frontend-specific conditional routing**
   - Core review skills always run.
   - React, hooks, design, forms, data grid, i18n, routing, Tailwind and Ant Design criteria are selected only for concrete risks in the captured diff. Excluded specialist workflows are not routed.

4. **Structured records**
   - Each sub-agent returns strict JSON with reviewer id, snapshot/scope, skill, actual coverage, verdict, findings, and notes.
   - The coordinator builds a reviewer ledger before summarizing findings.

5. **No unit-test-only advice**
   - Reviewers must not recommend adding unit tests or increasing coverage. Actual defects in changed assertions/mocks that conceal a behavior error remain reviewable.
   - If a reviewer returns a unit-test-only finding, the coordinator drops it.

6. **Final report shape**
   - User receives severity-grouped findings.
   - Each finding includes path, line if available, issue, why it matters, and recommended fix.
