# frontend-skill

A curated VS Code Chat / GitHub Copilot BYOK customization catalog for React and TypeScript frontend work. The repository root mirrors the runtime directories installed under `~/.copilot`.

## Catalog at a glance

- **59** Agent Skills under `skills/`
- **10** custom agents under `agents/`: three user-facing agents and seven hidden subagent workers
- **2** cross-project instruction files under `instructions/`
- Upstream source, pinned commit, path, and license tracked in [`skills/SKILLS_MANIFEST.md`](./skills/SKILLS_MANIFEST.md)
- Update families and safe migration procedure tracked in [`SKILL_SOURCES.md`](./SKILL_SOURCES.md)
- Machine-checkable catalog validation in [`scripts/validate_skill_catalog.py`](./scripts/validate_skill_catalog.py)

The catalog targets React, TypeScript, Tailwind/shadcn, AG Grid React, Ant Design, react-i18next, React Router, React Hook Form/Zod, and Vitest.

## Default routing

| Task evidence | Preferred skill(s) |
|---|---|
| React Router | `react-router` — detects installed mode/version and reads the matching official docs |
| AG Grid feature work | `ag-dev`; use `ag-update` only for dependency upgrades |
| shadcn/Tailwind v4 components | `shadcn`; use `tailwind-design-system` for general tokens/utilities |
| React Hook Form lifecycle | `react-hook-form-zod` — subscription scope, reset and parsed input/output |
| Localization automation | `internationalization-i18n` — project-pinned i18next CLI and retained runtime patterns |
| Design direction and UI polish | `frontend-design` — surface modes adapted from Impeccable |
| Unit/integration tests | `vitest`, optionally `javascript-testing-patterns` |
| OpenAPI-generated types | `openapi-typescript` deterministic CLI pipeline |
| React completion diagnostics | `react-doctor` after root-cause work, never as a debugging substitute |
| Third-party skill intake | `skill-scanner` before installation or update |

## Project-specific workflows

These workflows combine an Agent Skill for reusable policy with a VS Code custom coordinator agent for tools, handoffs, and named subagents:

- [`frontend-staged-review-workflow`](./skills/frontend-staged-review-workflow/) — reviews `git diff --cached` only, dispatches at least two real sub-agents per selected skill, and excludes unit-test-only suggestions.
- [`frontend-branch-review-workflow`](./skills/frontend-branch-review-workflow/) — pins source, target, and merge-base SHAs and reviews only committed merge-base-to-source changes.
- [`frontend-staged-commit-message`](./skills/frontend-staged-commit-message/) — explains the staged intent and type choice, then returns at least five one-line English subjects ordered from simple to detailed, without staging, editing, committing, or pushing.
- [`frontend-staged-review-workflow`](./skills/frontend-staged-review-workflow/), [`frontend-heavy-staged-review-workflow`](./skills/frontend-heavy-staged-review-workflow/), and [`frontend-branch-review-workflow`](./skills/frontend-branch-review-workflow/) share the **Frontend Review** coordinator while retaining separate scope and quorum policies.
- Their [shared review contract](./skills/frontend-staged-review-workflow/references/review-contract.md) pins evidence, routes the upgraded design/form/i18n/TDD Skills and requires independent coverage per changed scope plus aggregation validation.

All coordinator and worker definitions live in [`agents/`](./agents/). Worker agents are hidden from the picker and explicitly allowlisted by coordinators. Subagent invocations are treated as stateless; retries receive a complete task packet instead of relying on follow-up messages.

## Validation

Run from the repository root:

```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate_skill_catalog.py
python3 -m unittest -v tests/test_vscode_conversion.py
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

Preview and install the complete personal customization set on Ubuntu:

```bash
bash scripts/install-vscode-chat.sh --dry-run
bash scripts/install-vscode-chat.sh
```

The installer merges `skills/`, `agents/`, and `instructions/` into `~/.copilot`, retires excluded specialist entries and the workflow/agent entries removed in the 2026-10-29 migration, and preserves unrelated personal customizations and VS Code/BYOK settings. See the [Ubuntu setup and diagnostics guide](./docs/VS_CODE_CHAT_SETUP.zh-TW.md).

To move the catalog into a VM as one file, build the portable archive:

```bash
bash scripts/build-vscode-chat-bundle.sh
```

Copy `dist/frontend-skill-vscode-chat-bundle.tar.gz` to the Ubuntu VM, extract it, and run the bundled installer. See the [VM copy-and-install guide](./docs/VM_COPY_GUIDE.zh-TW.md) for Git, `scp`, shared-folder, and direct-copy options.

Repository folders are canonical source only; VS Code does not discover this root layout automatically. Install it under `~/.copilot`, reload VS Code, then use **Chat: Open Customizations** and Chat Diagnostics to verify discovery.

## Repository documents

- [Source and update policy](./SKILL_SOURCES.md)
- [Per-skill manifest](./skills/SKILLS_MANIFEST.md)
- [Validation report](./skills/VALIDATION_REPORT.md)
- [2026-10-28 catalog update report](./docs/SKILL_REPLACEMENT_RESEARCH.zh-TW.md)
- [Ubuntu VS Code Chat setup](./docs/VS_CODE_CHAT_SETUP.zh-TW.md)
- [Ubuntu VM copy-and-install guide](./docs/VM_COPY_GUIDE.zh-TW.md)
- [Custom Agents 中文使用與輸入格式](./docs/AGENT_USAGE_GUIDE.zh-TW.md)
- [Branch review workflow](./skills/frontend-branch-review-workflow/references/FRONTEND_BRANCH_REVIEW_WORKFLOW.md)
- [Heavy staged review workflow](./skills/frontend-heavy-staged-review-workflow/references/FRONTEND_HEAVY_STAGED_REVIEW_WORKFLOW.md)


Do not store API keys, access tokens, cookies, passwords, or other credentials in skills, manifests, examples, or validation output.
