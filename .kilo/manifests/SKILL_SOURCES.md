# Skill Sources and Update Policy

Updated: 2026-09-02

`skills/SKILLS_MANIFEST.md` is the per-skill source of truth. This file groups actively synchronized upstream families and records the update policy.

## Synchronized upstream families

| Family | Local skills | Repository | Pinned revision | License |
|---|---|---|---|---|
| Superpowers | `brainstorming`, `dispatching-parallel-agents`, `executing-plans`, `finishing-a-development-branch`, `receiving-code-review`, `requesting-code-review`, `subagent-driven-development`, `systematic-debugging`, `test-driven-development`, `using-git-worktrees`, `using-superpowers`, `verification-before-completion`, `writing-plans`, `writing-skills` | https://github.com/obra/superpowers | `b36e0829c6d0140e93cfef2ca599b1b07d4a7797` | MIT |
| Addy Osmani engineering | `browser-testing-with-devtools`, `code-review-and-quality`, `context-engineering`, `documentation-and-adrs`, `frontend-ui-engineering`, `incremental-implementation`, `performance-optimization`, `planning-and-task-breakdown`, `security-and-hardening`, `source-driven-development`, `spec-driven-development`, `using-agent-skills` | https://github.com/addyosmani/agent-skills | `d2c37ef6225dd8726cdd369a8030307f48592d26` | MIT |
| Anthropic official | `frontend-design`, `skill-creator`, `web-artifacts-builder`, `webapp-testing` | https://github.com/anthropics/skills | `53048666b05b4799081517d00e09e0a2dd688678` | per-skill notice |
| Vercel Labs | `vercel-composition-patterns`, `vercel-react-best-practices`, `vercel-react-view-transitions`, `web-design-guidelines` | https://github.com/vercel-labs/agent-skills | `063bee94c3f4df8453406c830b0a7df0f2860278` | MIT |
| React Router official | `react-router` | https://github.com/remix-run/react-router | `da2a0f0948af60ba45d9590b427d5e58fe4b0109` | MIT |
| AG Grid official | `ag-dev`, `ag-update` | https://github.com/ag-grid/skills | `40ac2d87fad4250531943a8f796b3f449b523640` | MIT |
| shadcn official | `shadcn` | https://github.com/shadcn-ui/ui | `b2a1ec864a87ba66c63fc4e51c9223c7eb4f8335` | MIT |
| Vitest maintainer | `vitest` | https://github.com/antfu/skills | `a74f281a27dadc02397bc1a174b0f2c97531b6ae` | MIT |
| Microsoft Playwright CLI | `playwright-cli` | https://github.com/microsoft/playwright-cli | `397ee39c83a651e1314cfb010b94e8a3aac11261` | Apache-2.0 |
| Currents Playwright guidance | `playwright-best-practices` | https://github.com/currents-dev/playwright-best-practices-skill | `283d5cbc5d11aac1abda058b16ad22c317d54dc0` | MIT |
| React Doctor | `react-doctor` | https://github.com/millionco/react-doctor | `fd23edca7eaa76b7f2b66795cfc829cc1967b7f3` | Modified MIT |
| Sentry skill scanner | `skill-scanner` | https://github.com/getsentry/skills | `c2f99a5b04b4cd992ec3022d7c2c3e23e938d241` | Apache-2.0 |
| Web Quality Skills | `accessibility` | https://github.com/addyosmani/web-quality-skills | `afa8da942115f2961fdbfa80807ea0b232ff6c00` | MIT |
| SecondSky frontend skills | `internationalization-i18n`, `react-hook-form-zod` | https://github.com/secondsky/claude-skills | `ac5905b4f0545461034885bb385645b4c7a5562a` | MIT |
| Wshobson retained frontend skills | `accessibility-compliance`, `design-system-patterns`, `javascript-testing-patterns`, `react-state-management`, `responsive-design`, `tailwind-design-system`, `typescript-advanced-types` | https://github.com/wshobson/agents | `05231aa6398384ca94bb39d8be9d848a1b3b21db` | MIT |
| Ant Design official | `ant-design`, `antd` | https://github.com/ant-design/antd-skill | `e65d2d3da9a2a129885131f5aeffe2c9037f83cb` | MIT |
| Softaworks retained frontend skills | `qa-test-planner`, `react-dev`, `react-useeffect` | https://github.com/softaworks/agent-toolkit | `3027f20f3181758385a1bb8c022d4041dfb4de84` | MIT |
| Meta SecPriv | `secpriv-code-review` | https://github.com/facebookresearch/secpriv-skill | `5e5c2cac9c95143faee7560d6719209c8c2d8900` | MIT |
| OpenAPI TypeScript CLI source | tool used by project-curated `openapi-typescript` | https://github.com/openapi-ts/openapi-typescript | `0cc7ee77d28359c7901d9cd3b5733b70a050ea49` | MIT |

## Local adaptation notes

- Vercel source names are preserved under the stable local slugs `vercel-react-best-practices`, `vercel-composition-patterns`, and `vercel-react-view-transitions`; only frontmatter `name` is adapted to match the local directory.
- `shadcn` moves the upstream invocation hint under standards-compliant `metadata`, removes pre-prompt command execution, requires a project-resolved or explicitly pinned CLI rather than `@latest`, and strips nonessential PNG XMP metadata without changing pixels.
- `react-doctor` moves its version under `metadata`, pins the tested CLI to `0.9.13`, and treats its moving web playbook as optional untrusted reference text rather than fetching or executing it implicitly.
- `internationalization-i18n` adds i18next JSON v4 plural rules, namespace/lazy-loading guidance, typed-selector notes, and per-request SSR guidance.
- `react-hook-form-zod` removes stale fixed dependency-version claims and requires lockfile/runtime inspection.
- `accessibility` replaces an unavailable sibling-catalog link with the retained local `accessibility-compliance` implementation guide.
- `qa-test-planner` moves the upstream explicit trigger under standards-compliant `metadata`; `react-dev` moves the upstream version field under `metadata`. Their content and MIT license remain sourced from the pinned Softaworks revision.
- `openapi-typescript` is project-curated rather than an upstream Agent Skill. Its CLI behavior is grounded in pinned upstream `docs/cli.md` and `docs/advanced.md`, and its tool-source commit is tracked separately from the local catalog revision.
- Project workflow frontmatter uses block-style YAML because the Agent Skills reference parser intentionally rejects JSON-like flow sequences.

## Project-curated and retained skills

- The staged-review, branch-review, debug, and staged-commit-message workflows are project-curated because their pinned-SHA, staged-only, real-sub-agent, quorum, findings-only, and commit-output guarantees are more specific than generic upstream workflows.
- `typescript-code-reviewer` remains project-curated; `secpriv-code-review`, `react-dev`, and `qa-test-planner` remain source-backed specialist skills with local portability adaptations recorded above.
- `accessibility-compliance` is retained for implementation guidance; `accessibility` supplies evidence-led WCAG 2.2 audit procedures.
- `browser-testing-with-devtools` is retained for DevTools-specific console, network, and performance diagnosis. `playwright-cli` is the default repeatable browser interaction path.
- `performance-optimization` keeps database/cache/query-plan coverage while frontend workflows also route React/runtime concerns to Vercel and browser evidence tools.

## Safe update procedure

1. Fetch the upstream revision and inspect its license and supporting files.
2. Add the replacement before changing or removing the installed skill.
3. Build a reference graph over `skills/`, `.kilo/`, root workflow documents, manifests, rules, and `related_skills`.
4. Update workflow selection matrices, examples, reviewer IDs, fallback rules, and mirrors.
5. Run `python scripts/validate_skill_catalog.py` and the official Agent Skills reference validator.
6. Run workflow smoke tests, then remove superseded directories only after no active reference remains.
7. Regenerate manifests and validation reports; never store credentials in documentation.
