---
name: frontend-staged-review-workflow
description: Use when reviewing git-staged frontend changes with real independent sub-agents. Reviews only `git diff --cached`, builds an internal dispatch plan, runs at least two sub-agents for every selected review skill, forbids unit-test suggestions, validates reviewer outputs, and returns a concise findings-only report.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [frontend, code-review, staged-diff, subagent, workflow, react, typescript, no-unit-tests]
    related_skills: [audit-code-reviewer, code-review-excellence, typescript-code-reviewer, code-review-and-quality, secpriv-code-review, react-dev, react-useeffect, vercel-react-best-practices, web-design-guidelines, accessibility-compliance, tailwind-design-system, tailwind-v4-shadcn, ant-design, ag-grid, react-hook-form-zod, internationalization-i18n, react-router-declarative-mode, react-router-data-mode, react-router-framework-mode, playwright-best-practices, webapp-testing]
---

# Frontend Staged Review Workflow

## Overview

This workflow reviews only the code that is already staged with `git add`. It is designed for frontend projects where the user wants real independent reviewer sub-agents to inspect the same staged diff, while the user receives a concise findings-only report.

Core contract:

1. Review target is **only** `git diff --cached`.
2. Use real independent sub-agents or Kilo custom agents for reviewer passes.
3. The coordinator / main agent must **not** perform reviewer passes itself and must **not** simulate multiple reviewers with internal personas.
4. Every selected review skill must be executed by **at least two independent sub-agents**.
5. Every sub-agent must load or be given the exact local review skill it is assigned.
6. If the runtime cannot actually launch sub-agents/custom agents, stop and return `Incomplete`; do not continue with a main-agent-only review.
7. Do **not** suggest unit tests, test coverage changes, or "add a unit test" follow-ups.
8. Final output must list: path, severity, and recommended fix.
9. Final user-facing report must be written in Chinese.

This is a review-only workflow. Do not modify files, do not stage additional files, and do not commit.

## When to Use

Use when the user says any of:

- "review git add 的內容"
- "review staged changes"
- "前端 review workflow"
- "用 sub-agent review 我的 code"
- "幫我 review 已 staged 的前端修改"

Do not use for:

- Unstaged work (`git diff`) unless the user first stages it.
- Backend-only review with no frontend impact.
- Unit test planning or test coverage review.
- Auto-fix loops; this workflow reports findings only.

## Research Basis

Detailed rationale lives in `references/research-notes.md`. At runtime, keep only the operational rule: independent reviewer passes reduce blind spots, and `audit-code-reviewer` is a coordinator pattern, not a default reviewer skill. If the user explicitly selects `audit-code-reviewer` as a reviewer, it must receive two independent reviewer passes like every other selected skill.

## Gate 1 — Pre-flight: staged diff only

Run and capture these commands internally before launching reviewers:

```bash
git rev-parse --show-toplevel
git status --short --branch
git diff --cached --name-only
git diff --cached --stat
git diff --cached
```

Rules:

- If `git diff --cached --name-only` is empty, stop and tell the user there is nothing staged to review.
- Do not use unstaged changes as review input.
- If `git status --short` shows unstaged changes, mention them as out-of-scope but do not review them.
- Capture the repository root, branch/status, staged file list, diff stat, unstaged file list, and the cached diff as the shared review packet.
- If the cached diff is large, split it by file while preserving the same selected skill list and internal reviewer ledger.

## Review Skill Selection Matrix

Select the smallest set of exact local skills that matches the staged diff. Every selected skill still requires at least two real sub-agent reviewer passes. Do not run a broad skill set just because the workflow is available.

Baseline skill:

| Trigger evidence in staged files / diff | Exact skill | Minimum sub-agents | Focus |
|---|---|---:|---|
| Any frontend staged diff | `code-review-excellence` | 2 | General correctness, maintainability, architecture, performance, constructive review quality. |

Conditional skills:

| Trigger evidence in staged files / diff | Exact skill | Minimum sub-agents | Focus |
|---|---|---:|---|
| Complex multi-file change, architecture/API boundary, or broad maintainability risk | `code-review-and-quality` | 2 | Five-axis quality gate: correctness, readability, architecture, security, performance. |
| TypeScript/TSX type changes, `any`/`unknown`, assertions, async/error handling, React hooks or props | `typescript-code-reviewer` | 2 | TypeScript/TSX type safety, unsafe assertions, async/error handling, React hooks and props. |
| Auth, permissions, user data, persistence, XSS/HTML injection, secrets, third-party scripts, analytics, privacy, or dangerous browser APIs | `secpriv-code-review` | 2 | Security + privacy findings, CWE/GDPR-style classification, false-positive suppression. |
| `.tsx`, React components, hooks, state, props | `react-dev` | 2 | Component boundaries, hook correctness, state ownership, React idioms. |
| `useEffect`, subscriptions, browser APIs, timers, derived state, async side effects | `react-useeffect` | 2 | Avoid unnecessary effects, stale closures, cleanup, synchronization bugs. |
| React performance, memoization, expensive renders, server/client boundary, bundle/runtime concerns | `vercel-react-best-practices` | 2 | React/Next/Vite performance patterns and avoidable re-renders. |
| UI, layout, visual hierarchy, copy, UX, interaction states, responsive behavior | `web-design-guidelines` | 2 | UI quality, affordance, polish, responsive behavior. |
| Accessibility, keyboard interaction, ARIA, semantic HTML, focus management | `accessibility-compliance` | 2 | WCAG/accessibility risks and concrete remediation. |
| Tailwind design tokens, theme scales, variants, reusable utility composition | `tailwind-design-system` | 2 | Token consistency, class composition, design-system maintainability. |
| Tailwind v4 config, shadcn-style components, CSS variables, design tokens in shadcn patterns | `tailwind-v4-shadcn` | 2 | Tailwind v4 / shadcn compatibility, token usage, component styling. |
| Ant Design components, ProComponents, Table/Form/Modal APIs, theme tokens | `ant-design` | 2 | antd component API, theme/token usage, accessibility/performance. |
| AG Grid files, column defs, cell renderers, row models, grid performance | `ag-grid` | 2 | Grid config, rendering performance, typed row data, accessibility. |
| forms, validation schemas, React Hook Form, Zod, field errors | `react-hook-form-zod` | 2 | Form state, schema validation, error UX, controlled/uncontrolled issues. |
| i18n files, translation keys, interpolation, locale formatting, react-i18next usage | `internationalization-i18n` | 2 | Missing translations, interpolation safety, date/number formatting. |
| React Router declarative routes, `<Routes>`, `<Route>`, `useNavigate`, route elements | `react-router-declarative-mode` | 2 | Declarative routing correctness and navigation behavior. |
| React Router data APIs, loaders/actions, `defer`, `useLoaderData`, fetchers | `react-router-data-mode` | 2 | Data-router correctness, loader/action boundaries, error states. |
| React Router framework-mode conventions, file routes, framework config | `react-router-framework-mode` | 2 | Framework-mode route conventions and integration. |
| Playwright config/specs/selectors/fixtures were staged or the diff changes E2E-visible selectors | `playwright-best-practices` | 2 | E2E selector stability and browser automation risk. Do not ask for unit tests. |
| Browser-visible runtime behavior changed but no Playwright-specific files were staged | `webapp-testing` | 2 | Runtime/browser behavior risk and manual/browser verification ideas. Do not ask for unit tests. |

Do not select a skill unless `skills/<skill-name>/SKILL.md` exists. Do not write generic labels like "React skill" or ambiguous rows like "A or B" in the dispatch plan. If two skills both match, select both and run two sub-agents for each.

## Gate 2 — Dispatch Plan

Before spawning sub-agents, the coordinator must write an internal dispatch plan. The workflow must not start reviewer waves until this plan is complete. Do not show the dispatch plan to the user unless they ask for the audit log.

Hard gate: before reviewing, confirm that the current runtime can actually launch independent sub-agents or Kilo custom agents. If no real sub-agent mechanism is available, stop here and return `Incomplete` with a concise note. Do not let the coordinator/main agent review the diff itself, and do not emulate sub-agents by writing multiple reviewer personas in one context.

Dispatch plan fields:

| Field | Requirement |
|---|---|
| `selected_skill` | Exact local skill slug. |
| `skill_path` | `skills/<selected_skill>/SKILL.md`. Must exist. |
| `trigger_evidence` | File path, extension, code pattern, or diff evidence that selected the skill. |
| `reviewer_ids` | At least two IDs per selected skill, e.g. `typescript-code-reviewer-A`, `typescript-code-reviewer-B`. |
| `angles` | Distinct angle for each reviewer. |
| `wave` | Dispatch wave number, respecting the environment's parallelism limit. |
| `input_scope` | Full staged diff or file/chunk subset assigned to the reviewer. |
| `expected_outputs` | Usually `2`; higher if the user asks for extra redundancy. |

Example:

| Skill | Skill path | Trigger evidence | Reviewer IDs | Angles | Wave | Input scope |
|---|---|---|---|---|---:|---|
| `typescript-code-reviewer` | `skills/typescript-code-reviewer/SKILL.md` | `src/UserTable.tsx` staged | `typescript-code-reviewer-A`, `typescript-code-reviewer-B` | type-safety; edge cases | 1 | full cached diff |
| `ag-grid` | `skills/ag-grid/SKILL.md` | `columnDefs` changed | `ag-grid-A`, `ag-grid-B` | grid API; rendering performance | 2 | AG Grid-related files |

## Shared Review Packet

Every reviewer must receive the same shared packet unless the dispatch plan explicitly assigns a file/chunk subset:

- Repository root.
- Branch/status from `git status --short --branch`.
- Review target: `git diff --cached` only.
- Staged file list.
- Diff stat.
- Cached diff or assigned cached-diff chunk.
- Unstaged files list marked as out of scope.
- Selected skill list and dispatch plan row for that reviewer.
- Relevant project excerpts when available: `package.json`, `tsconfig.json`, route config, UI library config.
- No-unit-test rule.
- Required strict JSON schema.

For large diffs, record coverage in the dispatch plan and internal reviewer ledger:

- `input_scope = full cached diff` when every reviewer sees the whole diff.
- `input_scope = path subset: ...` when reviewers are sharded.
- Record any file/chunk coverage limitations internally; expose them only if they affect the findings or the verdict.

## Sub-agent Dispatch Rules

Hard requirements:

- A valid reviewer pass must come from an actual sub-agent/custom-agent/tool invocation.
- The coordinator/main agent may prepare context, dispatch reviewers, validate outputs, and aggregate findings, but it must not count its own analysis as a reviewer pass.
- Do not simulate reviewers with headings like "Reviewer A" / "Reviewer B" inside the coordinator response. Those are not valid sub-agent outputs.
- If sub-agent dispatch fails, is unavailable, or is blocked by the environment, mark the affected passes as `missing` or `failed` and return `Incomplete` unless the user explicitly accepts a degraded report.

For each selected review skill:

1. Launch at least two independent sub-agents.
2. Give both agents the shared review packet and their dispatch plan row.
3. Give each a different angle so they do not simply duplicate each other:
   - Reviewer A: correctness / architecture / likely runtime bugs.
   - Reviewer B: edge cases / maintainability / integration / false positives.
   - Additional reviewers, if any: performance, accessibility, security/privacy, framework integration, or UI polish as appropriate.
4. Require every sub-agent to read `skills/<selected_skill>/SKILL.md` before reviewing when file tools are available.
5. If a sub-agent cannot read the skill file, the coordinator must paste the skill's key review criteria into the prompt or mark that reviewer output as degraded.
6. Tell every sub-agent: **do not suggest unit tests**.
7. Ask every sub-agent to return strict JSON only.

When using `delegate_task`, Kilo custom agents, or any equivalent sub-agent mechanism, batch in groups of up to the system concurrency limit. If the environment allows only three parallel children, run several waves until every selected skill has at least two valid reviewer outputs. If no equivalent mechanism is available, stop rather than doing a main-agent-only review.

## Sub-agent Output Contract

Every sub-agent must return strict JSON only: no markdown, no prose outside JSON, no comments. Use `templates/subagent-prompt.md` for the exact reviewer prompt and JSON schema.

Required fields: `reviewer_id`, `skill_used`, `skill_path`, `skill_read`, `status`, `angle`, `input_scope`, `verdict`, `findings`, and `notes`. Each finding must include path, line or line range when available, severity, category, summary, evidence, recommended fix, confidence, and blocking status. If the sub-agent has no findings, it must return an empty `findings` array and `verdict: "approve"` or `verdict: "comment"` with notes.

## Gate 3 — Reviewer Output Validation and Failure Policy

Validate every reviewer output before aggregation.

A reviewer output is valid only if:

- It came from an actual sub-agent/custom-agent/tool invocation, not from coordinator self-review or simulated personas.
- It is parseable strict JSON.
- It includes `reviewer_id`, `skill_used`, `skill_path`, `skill_read`, `status`, `angle`, `input_scope`, `verdict`, `findings`, and `notes`.
- `skill_used` matches the dispatch plan row.
- `skill_path` points to an existing local `skills/<skill-name>/SKILL.md`.
- `findings[*]` include path, severity, summary, evidence, recommended fix, confidence, and blocking status.
- It does not include unit-test-only advice.

Failure handling:

1. If JSON is invalid, required fields are missing, or the output suggests unit tests, retry that reviewer once with a stricter prompt.
2. If the retry is still invalid, mark the reviewer as `invalid` in the ledger. Invalid reviewers do not count toward the two-pass minimum.
3. If a reviewer fails or times out, mark it as `failed` in the ledger. Failed reviewers do not count toward the two-pass minimum.
4. If any selected skill has fewer than two valid reviewer outputs, the workflow is **incomplete** and must not claim full completion.
5. The user may accept a degraded report, but the coordinator must keep missing reviewer passes in the internal audit log. The user-facing final report should stay concise: show `Incomplete` or degraded status without exposing reviewer/sub-agent/skill provenance unless the user asks for the audit log.

## Aggregation Workflow

After all valid sub-agents finish:

1. Create an expanded internal reviewer ledger:
   - reviewer id
   - skill used
   - skill path
   - angle
   - status: `completed`, `degraded`, `failed`, `invalid`, `missing`
   - verdict
   - number of findings
   - trigger evidence
   - input scope
   - retry count
   - invalid / failure reason, if any
2. Normalize severities:
   - `critical`: definite runtime breakage, data loss, exploitable security/privacy issue, inaccessible critical flow.
   - `high`: likely user-facing bug, serious type-safety hole, auth/privacy/accessibility problem, major regression risk.
   - `medium`: maintainability or edge-case issue likely to matter soon.
   - `low`: clarity, polish, non-blocking UI/UX or performance improvement.
3. Deduplicate findings by `(path, nearby line, category, issue type)`.
4. Keep the highest severity when reviewers disagree.
5. Preserve cross-reviewer support internally for confidence and deduplication, but do not expose reviewer IDs, sub-agent names, or skill provenance in the user-facing findings report.
6. Drop any finding that only says to add unit tests or improve unit test coverage.
7. If a suggested fix is vague, rewrite it into an actionable recommendation or mark it as `needs clarification`.
8. Record dropped, merged, or severity-adjusted findings in the internal audit log only.

Verdict rule:

- Any valid `critical` or `high` blocking finding -> `Request changes`.
- Only `medium` / `low` findings -> `Comment`.
- No findings and all expected reviewer passes completed -> `Approve`.
- Any missing/failed/invalid reviewer pass that leaves a selected skill with fewer than two valid outputs -> `Incomplete`.

## Final User Report Format

The final user-facing report must be findings-only and written in Chinese. Keep dispatch plans, reviewer ledgers, skill names, reviewer IDs, aggregation logs, retry details, and sub-agent provenance internal unless the user explicitly asks for the audit log.

Use `templates/final-report.md` for the exact concise format. The final report must contain only:

- Chinese verdict line (`結論: ...`).
- Findings grouped by Chinese severity headings: `嚴重`, `高`, `中`, `低`.
- For each finding: path, line when available, issue, evidence, why it matters, and recommended fix, written in Chinese.
- Chinese suggested fix order when there is more than one finding.

If there are no findings, say `結論: Approve` and `已暫存 diff 中沒有發現問題。` If the workflow is incomplete or degraded, say `結論: Incomplete` with a concise Chinese note and no reviewer/skill provenance.

## Completion Checklist

The workflow is complete only when:

- [ ] `git diff --cached` was the only review target and is non-empty.
- [ ] Internal dispatch plan was written before sub-agent dispatch.
- [ ] Selected skill list uses exact local skill slugs only, and every selected skill path exists.
- [ ] Every selected skill has at least two valid real sub-agent/custom-agent reviewer outputs.
- [ ] No reviewer output was simulated by the coordinator/main agent.
- [ ] Reviewer outputs were validated as strict JSON or marked failed/invalid/missing in the internal audit log.
- [ ] Findings were deduplicated and severity-normalized.
- [ ] Unit-test-only suggestions were removed.
- [ ] The final user-facing report is findings-only and includes path, severity, evidence, why it matters, and recommended fix for every finding.
- [ ] Unstaged files, if any, were not reviewed.

## Common Pitfalls

1. Reviewing unstaged changes. This violates the workflow. Only `git diff --cached` is in scope.
2. Running only one sub-agent for a selected skill. Every selected skill needs at least two valid independent passes.
3. Simulating multiple reviewers in the main/coordinator context. This does not count; use real sub-agents/custom agents or return `Incomplete`.
4. Treating `audit-code-reviewer` as a reviewer replacement. It is the coordinator pattern by default, not a substitute for the two-pass rule.
5. Letting reviewers recommend unit tests. Remove those findings and remind reviewer prompts that unit-test advice is forbidden.
6. Listing generic skill labels. Use exact local names such as `typescript-code-reviewer`, not "TypeScript skill".
7. Using ambiguous `or` routing. If two skills match, select both; otherwise use deterministic trigger evidence.
8. Accepting JSON-like prose. Reviewer outputs must be strict JSON or marked invalid.
9. Reporting vague advice. Every finding needs a concrete path, severity, evidence, and recommended fix.
