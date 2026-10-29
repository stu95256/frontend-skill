# VS Code Chat Catalog Validation Report

Generated: 2026-10-29

## Current result

**PASS — catalog, Skill format and migration regression checks.**

- 59 Agent Skills: 30 core and 29 on demand.
- 10 custom agents: three coordinators and seven protected workers.
- Two instruction files.
- User-facing agents: Frontend Implementation, Frontend Review and VS Code Skill Creator.
- The two retired workflow packages, their full references and four dedicated agent definitions were removed. Routing, usage examples, VM setup and manifests match the remaining catalog.

The repository validator reports:

```text
VS Code Chat catalog validation passed: 59 skills, 10 custom agents, 2 instruction files, no legacy runtime artifacts
```

## Current format and regression checks

All 59 packages passed the official Agent Skills reference validator from agentskills/agentskills commit `69ef37e9424c0a7ea9dd2293b559e43ec8176379`. All 59 also passed the native skill-creator quick validator. Windows runs used Python 3.11.15 with UTF-8 mode.

All seven existing regression tests passed, none skipped, in 17.745 seconds:

```bash
python -m unittest -v tests/test_vscode_conversion.py
```

The migration fixture starts with ten retired Skill directories, four retired Agent files and unrelated personal customizations. Installation removes the retired entries, installs the current 59 Skills / 10 catalog Agents / two instructions, and preserves the personal Skill content and additional personal Agent.

The negative-reference fixture rejects retired workflow/agent routes as well as excluded specialist routes. Existing tests also cover ordered commit subjects, resumable Skill Creator evaluation, holdout isolation, uncommitted review packages, rejected empty/unrelated ranges and same-basename plan isolation.

Installer Bash syntax, editor diagnostics for the changed Python files and usage guide, local Markdown links and whitespace checks passed. Git Bash migration tests ran outside the host sandbox, only against isolated temporary targets. The actual personal catalog was not modified.

## Review workflow retained

The three review modes retain the [shared contract](frontend-staged-review-workflow/references/review-contract.md): immutable evidence, conditional upgraded Skill routing, independent per-hunk coverage and required aggregation validation. Staged/branch use at least two seats per selected risk scope; heavy defaults to five seats and two validators.

The shared reviewer retains Implementation's separate single-task contract. The [usage guide](../docs/AGENT_USAGE_GUIDE.zh-TW.md) now documents only the three current user-facing agents.

The prior isolated Git fixture verified unborn-HEAD cached diffs, worktree/index separation, restaging identity changes, immutable old blobs and pinned branch context. That fixture was run during the review update; it was not repeated for this catalog deletion.

## Retained specialist verification record

The four cross-source replacements remain unchanged. Their earlier focused checks were completed on 2026-10-28:

- The actual server-backed form template compiled with strict TypeScript and passed DOM checks for dirty refresh, numeric parsing, awaited submission, saved baselines, Cancel and keyed record changes. Those checks exposed and verified the explicit reset preservation overrides.
- The fixed i18next-cli 1.80.5 fixture verified prompt output, dry-run preservation, instrumentation, extraction, lint and translation status on Node 22.
- The shadcn coverage helper's missing/complete cases passed.
- Static scanning and source syntax checks were performed during the earlier upgrade; no new scanner result or model-quality comparison is claimed for this deletion.

See [the cross-source update record](../docs/SKILL_REPLACEMENT_RESEARCH.zh-TW.md) and [source manifest](SKILLS_MANIFEST.md).

## Transport packages and limits

The portable tar.gz and a fresh 7z are rebuilt from canonical source. Export checks require 59 Skill entrypoints, 10 agent definitions, two instructions, no retired directories/agent files, successful extracted-catalog validation, exact archive inventory, 7z integrity and Base64/SHA-256 round-trip agreement.

Actual VS Code discovery and BYOK worker execution still need verification in the target Ubuntu profile. Format/migration checks do not prove reviewer coverage behavior, rendered visual quality or model performance. See [Ubuntu setup](../docs/VS_CODE_CHAT_SETUP.zh-TW.md).
