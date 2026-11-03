# VS Code Chat Catalog Validation Report

Updated: 2026-11-03

## Review evidence and recovery pass — 2026-11-03

The three review modes and their agents now use protocol v3: semantic acceptance, lossless presentation normalization, persisted raw/source artifacts outside the checkout, inspected-artifact receipts and class-specific bounded recovery. The [runtime protocol](./frontend-staged-review-workflow/references/runtime-and-evidence.md) defines the handoff and recovery rules; the [evidence helper](./frontend-staged-review-workflow/scripts/review_evidence.py) preserves actual bytes and provenance.

- Catalog validation passed for 60 Skills, 10 agents and two instructions. All 60 Skills passed the official Agent Skills reference validator; the three modified review Skills also passed the system skill-creator quick validator.
- In UTF-8 mode, unittest discovery ran 26 tests in 47.137 seconds: 23 passed and three existing Bash-dependent tests were skipped because Bash was unavailable. All 17 new evidence tests passed, including raw bytes/NUL/CRLF, Chinese paths, corruption refusal, linked Git directories, junction escapes, clean-filter avoidance and partial-clone reads without object writes.
- Five independent tabletop scenarios checked normalization, transient failure followed by evidence repair, raw artifact retransmission, inherited split exhaustion and changed-bundle revalidation. Changed Markdown links and whitespace checks passed; editor diagnostics reported no Python errors.
- Actual VS Code Local worker execution, BYOK discovery and Azure MCP were not exercised. Distribution archives were not rebuilt.

## Local / BYOK compatibility pass — 2026-11-02

The [catalog-wide audit](../docs/VS_CODE_BYOK_COMPATIBILITY_AUDIT.zh-TW.md) records the current Local target, official references, corrected delegation/discovery assumptions, and runtime limits. It covers implementation and Skill Creator as well as the existing review workflows.

- Catalog validation passed for 60 Skills, 10 agents and two instructions. All 60 packages also passed the cached official reference validator (`69ef37e` checkout) and bundled Local quick validator.
- All **nine** regression tests passed, with no skips, in 55.972 seconds. New cases verify supported Local frontmatter, rejected invalid fields/types, UTF-8 content and packaging from an unrelated working directory; existing installer and SDD cases ran with Git Bash.
- The installer fixture initially failed to create its isolated target under the host sandbox; the suite passed outside the sandbox, without modifying the real personal catalog. Bash syntax checks passed for installer and bundle builder.
- An independent read-only tabletop pass checked missing named workers and accidentally delegated coordinators. Real VS Code discovery, BYOK worker execution and Azure MCP were not tested. Existing distribution archives were not rebuilt for this pass.

The adoption and earlier validation records below describe their own runs and retain their original results.

## Current adoption — 2026-11-02

The [Azure DevOps PR Skill](./azure-devops-create-pr/SKILL.md) and its [bundled PR template](./azure-devops-create-pr/assets/pr-description.md) were moved from the proposal directory into the canonical catalog. Both files retain their original content. The manifest, routing documentation, source policy, catalog count checks and installation fixture now include the new Skill.

- Catalog validator passed: **60 Skills, 10 custom agents, two instruction files**. The manifest contains 30 core and 30 on-demand entries.
- All 60 packages passed the official Agent Skills reference validator at commit `69ef37e9424c0a7ea9dd2293b559e43ec8176379`, using the cached offline package and UTF-8 mode. The moved PR Skill also passed the native skill-creator quick validator.
- All seven conversion/migration regression tests passed, none skipped, in 32.277 seconds. The installer test verifies that the bundled PR template is copied byte-for-byte into an isolated installation target.
- Relative links in the moved Skill and its research document resolve at the new locations.
- Installation tests ran with Git Bash outside the host sandbox because Git Bash could not create its isolated temporary target inside the sandbox. The actual personal catalog was not modified.

Existing distribution archives were not rebuilt for this move; rebuild them from the current canonical source before distributing the 60-Skill catalog. This change does not verify live Azure DevOps PR creation or work item association.

## Historical validation record — 2026-10-29

The sections below record the earlier 59-Skill catalog and its checks; their counts and transport results are historical.

### Result

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
