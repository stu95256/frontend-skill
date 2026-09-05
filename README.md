# frontend-skill

A curated, pinned, and validated Agent Skills catalog for React/TypeScript frontend work. The repository keeps portable skills under `skills/` and a synchronized Kilo Code staging tree under `.kilo/`.

## Catalog at a glance

- **65** portable skills
- **33** default-core skills and **32** on-demand specialists
- **67** Kilo skills after adding two Kilo-only workflow wrappers
- Upstream source, pinned commit, path, and license tracked in [`skills/SKILLS_MANIFEST.md`](./skills/SKILLS_MANIFEST.md)
- Update families and safe migration procedure tracked in [`SKILL_SOURCES.md`](./SKILL_SOURCES.md)
- Machine-checkable catalog validation in [`scripts/validate_skill_catalog.py`](./scripts/validate_skill_catalog.py)

The catalog targets React, TypeScript, Tailwind/shadcn, AG Grid React, Ant Design, react-i18next, React Router, React Hook Form/Zod, Vitest, and Playwright.

## Default routing

| Task evidence | Preferred skill(s) |
|---|---|
| React Router | `react-router` — detects installed mode/version and reads the matching official docs |
| AG Grid feature work | `ag-dev`; use `ag-update` only for dependency upgrades |
| shadcn/Tailwind v4 components | `shadcn`; use `tailwind-design-system` for general tokens/utilities |
| Unit/integration tests | `vitest`, optionally `javascript-testing-patterns` |
| Browser interaction/evidence | `playwright-cli`; use `browser-testing-with-devtools` for DevTools-specific diagnosis |
| Playwright test authoring/review | `playwright-best-practices` |
| Accessibility implementation | `accessibility-compliance`; use `accessibility` for evidence-led WCAG 2.2 audits |
| OpenAPI-generated types | `openapi-typescript` deterministic CLI pipeline |
| React completion diagnostics | `react-doctor` after root-cause work, never as a debugging substitute |
| Third-party skill intake | `skill-scanner` before installation or update |

## Project-specific workflows

These workflows intentionally remain project-curated because generic upstream skills do not preserve all local guarantees:

- [`frontend-staged-review-workflow`](./skills/frontend-staged-review-workflow/) — reviews `git diff --cached` only, dispatches at least two real sub-agents per selected skill, and excludes unit-test-only suggestions.
- [`frontend-branch-review-workflow`](./skills/frontend-branch-review-workflow/) — pins source, target, and merge-base SHAs and reviews only committed merge-base-to-source changes.
- [`frontend-debug-workflow`](./skills/frontend-debug-workflow/) — evidence-first root-cause workflow with stack-aware skill routing and explicit verification.
- [`frontend-staged-commit-message`](./skills/frontend-staged-commit-message/) — reads only staged changes and returns one concise English commit subject without staging, editing, committing, or pushing.
- `.kilo/skills/frontend-task-preflight/` — Kilo-only task planning wrapper.
- `.kilo/skills/frontend-heavy-staged-review-workflow/` — Kilo-only high-quorum staged review wrapper.

Workflow copies under root documents, `.kilo/skills/`, and `.kilo/workflows/` are synchronized by the catalog validator.

## Validation

Run from the repository root:

```bash
python scripts/validate_skill_catalog.py
```

Then validate each skill against the official Agent Skills reference implementation:

```bash
for skill in skills/*/; do
  [ -f "$skill/SKILL.md" ] || continue
  uvx --from 'git+https://github.com/agentskills/agentskills.git#subdirectory=skills-ref' \
    skills-ref validate "$skill" || exit 1
done
```

The committed validation result is recorded in [`skills/VALIDATION_REPORT.md`](./skills/VALIDATION_REPORT.md). Never claim the catalog is green without running both checks on the current working tree.

## Installation

Copy only the required skill directories into a supported agent skill root, for example:

```text
.claude/skills/<skill-name>/
.opencode/skills/<skill-name>/
~/.copilot/skills/<skill-name>/
```

For Kilo Code, review [`.kilo/README.md`](./.kilo/README.md), validate the staging tree, then copy or merge it into `~/.kilo/`.

## Repository documents

- [Source and update policy](./SKILL_SOURCES.md)
- [Per-skill manifest](./skills/SKILLS_MANIFEST.md)
- [Validation report](./skills/VALIDATION_REPORT.md)
- [Frontend task preflight workflow](./FRONTEND_TASK_PREFLIGHT_WORKFLOW.md)
- [Branch review workflow](./FRONTEND_BRANCH_REVIEW_WORKFLOW.md)
- [Debug workflow](./FRONTEND_DEBUG_WORKFLOW.md)
- [Heavy staged review workflow](./FRONTEND_HEAVY_STAGED_REVIEW_WORKFLOW.md)
- [Agent skill layout research](./AGENT_SKILL_LAYOUTS_RESEARCH.md)

Do not store API keys, access tokens, cookies, passwords, or other credentials in skills, manifests, examples, or validation output.
