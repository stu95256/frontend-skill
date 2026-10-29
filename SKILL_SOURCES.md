# Skill Sources and Update Policy

Updated: 2026-10-28

`skills/SKILLS_MANIFEST.md` is the per-skill source of truth. This file groups actively synchronized upstream families and records the update policy.

## Synchronized upstream families

| Family | Local skills | Repository | Pinned revision | License |
|---|---|---|---|---|
| Superpowers | `brainstorming`, `dispatching-parallel-agents`, `executing-plans`, `finishing-a-development-branch`, `receiving-code-review`, `requesting-code-review`, `subagent-driven-development`, `systematic-debugging`, `using-git-worktrees`, `using-vscode-chat`, `verification-before-completion`, `writing-plans`, `writing-skills` | https://github.com/obra/superpowers | `2ce8aa15d05bd57213e6f746f953aafb7ded7a8b` | MIT |
| Addy Osmani engineering | `code-review-and-quality`, `context-engineering`, `documentation-and-adrs`, `frontend-ui-engineering`, `incremental-implementation`, `performance-optimization`, `planning-and-task-breakdown`, `security-and-hardening`, `source-driven-development`, `spec-driven-development`, `using-agent-skills` | https://github.com/addyosmani/agent-skills | `aeac41d4d005999432bb7312f7ff06383a91d59d` | MIT |
| Anthropic official and retained design guidance | `frontend-design`, `skill-creator`, `web-artifacts-builder` | https://github.com/anthropics/skills | `dbd4588f9e1033efb41dad4bef2f7947c8993d44` | per-skill notice |
| Vercel Labs | `vercel-composition-patterns`, `vercel-react-best-practices`, `vercel-react-view-transitions`, `web-design-guidelines` | https://github.com/vercel-labs/agent-skills | `1a2c79d4e6c4a2283dc2c614b6538cbe1ed5ca62` | MIT |
| React Router official | `react-router` | https://github.com/remix-run/react-router | `959182edd6fe3556cec3b52ec83178d99da29ceb` | MIT |
| AG Grid official | `ag-dev`, `ag-update` | https://github.com/ag-grid/skills | `ef483f7f9e8cc9e5f359144d11317cd4094d5b8e` | MIT |
| shadcn official | `shadcn` | https://github.com/shadcn-ui/ui | `96da9cc7f1aa10580a3741664e2a77c721206c00` | MIT |
| Vitest maintainer | `vitest` | https://github.com/antfu/skills | `8886fe2d385d3644cbb47e46ae9cb1cf09307d3b` | MIT |
| React Doctor | `react-doctor` | https://github.com/millionco/react-doctor | `84ad0c8d0df7a3ab7d26946367fae3bc39c100d0` | Modified MIT |
| Sentry skill scanner | `skill-scanner` | https://github.com/getsentry/skills | `d12f250460ffd961f549dbebf7eeb0cf4afd4c2e` | Apache-2.0 |
| SecondSky retained form/i18n references | `internationalization-i18n`, `react-hook-form-zod` | https://github.com/secondsky/claude-skills | `88378361314f558fb719aec0af9fd898ab36f0b2` | MIT |
| Wshobson retained frontend skills | `design-system-patterns`, `javascript-testing-patterns`, `react-state-management`, `responsive-design`, `tailwind-design-system`, `typescript-advanced-types` | https://github.com/wshobson/agents | `0874a27b17a22e2b7c2e2bcd725768e0803cad06` | MIT |
| Ant Design official | `ant-design`, `antd` | https://github.com/ant-design/antd-skill | `e65d2d3da9a2a129885131f5aeffe2c9037f83cb` | MIT |
| Softaworks retained frontend skills | `qa-test-planner`, `react-dev`, `react-useeffect` | https://github.com/softaworks/agent-toolkit | `3027f20f3181758385a1bb8c022d4041dfb4de84` | MIT |
| Meta SecPriv | `secpriv-code-review` | https://github.com/facebookresearch/secpriv-skill | `70e1269a988cb401ac838164b3db9434ffa9f4ea` | MIT |
| OpenAPI TypeScript CLI source | tool used by project-curated `openapi-typescript` | https://github.com/openapi-ts/openapi-typescript | `d46a319ae2efab30e135ba9b223a3cffd1a67eab` | MIT |
| Matt Pocock TDD | `test-driven-development` | https://github.com/mattpocock/skills | `59db609eb1e18aaf59b63284d0e52255aff0c63c` | MIT |
| Supabase RHF lifecycle | `react-hook-form-zod` (primary entrypoint/lifecycle) | https://github.com/supabase/supabase | `167c633ed06da4da7b545f083b999fd7d8c669c5` | Apache-2.0 |
| i18next official CLI workflow | `internationalization-i18n` (primary workflow) | https://github.com/i18next/i18next-cli | `740a925c2a2b93e37c427bfd1a798708e68b7431` | MIT |
| Impeccable design playbooks | `frontend-design` (primary entrypoint/modes) | https://github.com/pbakaus/impeccable | `8409a564d1baee90b2dde4f7a8f06288838e3921` | Apache-2.0 |

## Local adaptation notes

- Vercel source names are preserved under the stable local slugs `vercel-react-best-practices`, `vercel-composition-patterns`, and `vercel-react-view-transitions`; only frontmatter `name` is adapted to match the local directory.
- `shadcn` moves the upstream invocation hint under standards-compliant `metadata`, removes pre-prompt command execution, requires a project-resolved or explicitly pinned CLI rather than `@latest`, and strips nonessential PNG XMP metadata without changing pixels.
- `react-doctor` moves its version under `metadata`, pins the validated CLI to `0.9.18`, and treats its moving web playbook as optional untrusted reference text rather than fetching or executing it implicitly.
- `internationalization-i18n` adds i18next JSON v4 plural rules, namespace/lazy-loading guidance, typed-selector notes, and per-request SSR guidance.
- `react-hook-form-zod` removes stale fixed dependency-version claims and requires lockfile/runtime inspection.
- `qa-test-planner` moves the upstream explicit trigger under standards-compliant `metadata`; `react-dev` moves the upstream version field under `metadata`. Their content and MIT license remain sourced from the pinned Softaworks revision.
- `openapi-typescript` is project-curated rather than an upstream Agent Skill. Its CLI behavior is grounded in pinned upstream `docs/cli.md` and `docs/advanced.md`, and its tool-source commit is tracked separately from the local catalog revision.
- Project workflow frontmatter uses block-style YAML because the Agent Skills reference parser intentionally rejects JSON-like flow sequences.

## Project-curated and retained skills

- The staged-review, heavy-staged-review, branch-review, and staged-commit-message workflows are project-curated because their pinned-SHA, staged-only, real-sub-agent, quorum, findings-only, and commit-output guarantees are more specific than generic upstream workflows.
- `typescript-code-reviewer` remains project-curated; `secpriv-code-review`, `react-dev`, and `qa-test-planner` remain source-backed specialist skills with local portability adaptations recorded above.
- `performance-optimization` keeps database/cache/query-plan coverage while frontend workflows also route React/runtime concerns to Vercel and source, build, and unit/integration evidence.

## Current catalog adaptation — 2026-10-29

- Retained catalog: 59 Skills, 10 custom agents, 2 instruction files.
- Shared upstream checklists are vendored inside their owning Skill so installation is self-contained.
- Superpowers updates preserve stateless VS Code workers and local uncommitted review support; helper scripts adopt plan ownership, range guards, and explicit interpreter invocation.
- Vitest references cover the installed major and Node/DOM unit/integration scope; beta examples require an explicit version check.
- Only source, type, build, unit/integration, and supplied diagnostic evidence are routed by the catalog.

## Cross-source replacements

- TDD now follows Matt Pocock's focused public-interface tests and vertical slices; preserves authorized task boundaries and green refactoring, with no destructive restart rule.
- RHF entrypoint and lifecycle guidance now follow Supabase; Studio-only components, lint policies and dependencies are excluded. Existing SecondSky schema, array and wizard references remain.
- i18n workflow now follows the official i18next CLI skill with project-pinned commands and local files by default. Runtime, Intl, RTL and alternative framework guidance remains from SecondSky.
- Design entrypoint now follows Impeccable's surface modes and selected document playbooks. No launcher, hooks, extra agents, specialist audit workflow or live-page dependency is imported; retained Anthropic guidance keeps its license.
- Dedicated audit/implementation packages excluded by the user are absent; the installer removes their obsolete installed copies. No animation-performance package is included.
- Existing component labels, native controls, UI states and component-library behavior remain normal frontend examples; they do not select a specialist audit.
- The manifest records primary and retained sources separately. Skill names remain stable so existing coordinators continue to resolve them.

## Safe update procedure

1. Fetch the upstream revision and inspect its license and supporting files.
2. Add the replacement before changing or removing the installed skill.
3. Build a reference graph over `skills/`, `agents/`, `instructions/`, workflow documents, manifests, rules, and `related_skills`.
4. Update workflow selection matrices, examples, reviewer IDs, fallback rules, and mirrors.
5. Run `python scripts/validate_skill_catalog.py` and the official Agent Skills reference validator.
6. Run workflow smoke tests, then remove superseded directories only after no active reference remains.
7. Regenerate manifests and validation reports; never store credentials in documentation.
