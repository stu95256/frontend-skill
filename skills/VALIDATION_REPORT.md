# VS Code Chat Catalog Validation Report

Generated: 2026-10-28

## Result

**PASS — source catalog, format checks and focused executable verification.**

- 61 Agent Skills: 30 core and 31 on demand.
- 14 custom agents: five coordinators and nine protected workers.
- Two instruction files.
- Four stable Skill names now use different primary sources: TDD, RHF, i18n and frontend design.
- Excluded specialist packages and their selection rules are absent. Dedicated supporting checklists were removed; ordinary native controls, labels and component states remain in general frontend examples.

## Catalog and format

The current repository validator reports:

```text
VS Code Chat catalog validation passed: 61 skills, 14 custom agents, 2 instruction files, no legacy runtime artifacts
```

All 61 packages passed the official Agent Skills reference validator from agentskills/agentskills commit `69ef37e9424c0a7ea9dd2293b559e43ec8176379`, using strictyaml 1.7.3. All 61 passed the native skill-creator quick validator.

Windows checks used Python 3.11.15 with UTF-8 mode; upstream validators default to the platform encoding otherwise. Real Markdown links outside fenced examples were checked throughout the Skills tree: zero missing local targets.

Primary and retained sources, fixed SHAs and licenses are recorded in [the manifest](SKILLS_MANIFEST.md). New upstream licenses are included beside the adapted Skills.

## Regression tests

```bash
python -m unittest -v tests/test_vscode_conversion.py
```

**Seven tests passed; none skipped** in the final run, using Python 3.11.15 and Git Bash with its path explicitly configured.

Coverage includes:

- Catalog consistency and rejected references to excluded specialist Skills.
- Installing exactly 61 Skills, 14 agents and two instructions, pruning excluded legacy directories and preserving an unrelated customization.
- Ordered staged commit-message candidates.
- Resumable Skill Creator evaluation and holdout isolation.
- Tracked/untracked review packages and rejected empty/unrelated committed ranges.
- Same-basename plan isolation, normalized plan identity and preserved ignore rules.

Installer and Bash filesystem checks ran outside the host sandbox because sandboxed Git Bash path operations are denied. All installation destinations were isolated temporary folders; the actual personal catalog was not modified.

## Actual form template

The [server-backed form](react-hook-form-zod/templates/server-backed-form.tsx) compiled with strict TypeScript 5.9.3, React/React DOM 19.2.0, RHF 7.84.0, Zod 4.3.6, resolvers 5.2.2 and React types 19.0.0.

A jsdom 26.1.0 harness exercised that compiled template and verified:

- Dirty edits survive a same-record background refresh while untouched fields update.
- Empty and malformed numeric input cannot submit.
- Parsed output carries a number rather than the input string.
- Submission stays pending until saving finishes.
- The persisted server response becomes the clean baseline.
- Cancel restores that baseline.
- A keyed record change does not keep the previous record's edits.

The initial harness exposed inherited keepDirtyValues behavior on save/Cancel resets. The template explicitly overrides preservation in those resets; the same checks then passed. This correction is documented in [form lifecycle](react-hook-form-zod/references/form-lifecycle.md).

## i18next CLI

The fixed upstream package identifies i18next-cli **1.80.5**, requiring Node 22+. The isolated fixture used that CLI on Node 22.23.2.

Verified the version-matched prompt command, dry-run source SHA preservation, instrumentation, extraction and lint. Status rejected two untranslated keys; after supplying the two local fixture translations, lint and status passed with 2/2 complete.

SWC's native loader requires a protected user cache. These commands ran outside the sandbox using the normal cache, without weakening its checks. No translation service, credentials or external project were used. This is a CLI fixture check, not validation of an entire application runtime or translation quality.

## Other focused checks

- The static Skill scanner processed all 61 packages. Pattern hits remained in dummy test passwords, the scanner's own detection examples and the source-retrieval warning example. The four newly adapted packages had no findings. Static patterns do not establish blanket security.
- The unchanged shadcn coverage helper rejected missing coverage and accepted complete coverage.
- Source Python syntax and installer/bundle Bash syntax were checked; changed files have no whitespace errors.
- TDD and design instructions were reviewed for self-contained references, user scope and retained workflow contracts. No model A/B or visual behavior result is claimed.

## Transport packages

The portable tar.gz and 7z are rebuilt from canonical source. Export checks require exactly 61 Skill entrypoints, no excluded directories, successful validation of the extracted catalog, a valid 7z integrity test and a matching Base64 decode/SHA-256 round trip.

The transfer archive and adjacent checksum represent this 61-Skill release.

## Remaining limits

VS Code discovery, handoff UI and real BYOK worker invocation still require verification in the target Ubuntu profile. Formatting, CLI fixtures and DOM tests do not establish model selection quality or prove rendered visual appearance.

See [the update report](../docs/SKILL_REPLACEMENT_RESEARCH.zh-TW.md) and [Ubuntu setup](../docs/VS_CODE_CHAT_SETUP.zh-TW.md).
