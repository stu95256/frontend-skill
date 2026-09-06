# frontend-skill

A curated VS Code Chat / GitHub Copilot BYOK customization catalog for React and TypeScript frontend work. The repository root mirrors the runtime directories installed under `~/.copilot`.

## Catalog at a glance

- **67** Agent Skills under `skills/`
- **17** custom agents under `agents/`: eight user-facing workflow agents and nine hidden subagent workers
- **2** cross-project instruction files under `instructions/`
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

These workflows combine an Agent Skill for reusable policy with a VS Code custom coordinator agent for tools, handoffs, and named subagents:

- [`frontend-staged-review-workflow`](./skills/frontend-staged-review-workflow/) — reviews `git diff --cached` only, dispatches at least two real sub-agents per selected skill, and excludes unit-test-only suggestions.
- [`frontend-branch-review-workflow`](./skills/frontend-branch-review-workflow/) — pins source, target, and merge-base SHAs and reviews only committed merge-base-to-source changes.
- [`frontend-debug-workflow`](./skills/frontend-debug-workflow/) — evidence-first root-cause workflow with stack-aware skill routing and explicit verification.
- [`frontend-staged-commit-message`](./skills/frontend-staged-commit-message/) — reads only staged changes and returns one concise English commit subject without staging, editing, committing, or pushing.
- [`frontend-task-preflight`](./skills/frontend-task-preflight/) + **Frontend Task Preflight** — read-only research and an implementation-plan handoff.
- [`frontend-heavy-staged-review-workflow`](./skills/frontend-heavy-staged-review-workflow/) + **Frontend Heavy Staged Review** — five independent reviewer seats per selected skill plus validator subagents.

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

The installer merges `skills/`, `agents/`, and `instructions/` into `~/.copilot` without deleting unrelated personal customizations or changing VS Code/BYOK settings. See the [Ubuntu setup and diagnostics guide](./docs/VS_CODE_CHAT_SETUP.zh-TW.md).

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
- [Ubuntu VS Code Chat setup](./docs/VS_CODE_CHAT_SETUP.zh-TW.md)
- [Ubuntu VM copy-and-install guide](./docs/VM_COPY_GUIDE.zh-TW.md)
- [Frontend task preflight workflow](./skills/frontend-task-preflight/references/FRONTEND_TASK_PREFLIGHT_WORKFLOW.md)
- [Branch review workflow](./skills/frontend-branch-review-workflow/references/FRONTEND_BRANCH_REVIEW_WORKFLOW.md)
- [Debug workflow](./skills/frontend-debug-workflow/references/FRONTEND_DEBUG_WORKFLOW.md)
- [Heavy staged review workflow](./skills/frontend-heavy-staged-review-workflow/references/FRONTEND_HEAVY_STAGED_REVIEW_WORKFLOW.md)


Do not store API keys, access tokens, cookies, passwords, or other credentials in skills, manifests, examples, or validation output.
