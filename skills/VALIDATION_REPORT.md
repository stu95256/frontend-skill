# Skills Validation Report

Generated: 2026-09-05

## Result

**PASS**

| Check | Scope | Result |
|---|---:|---|
| Project catalog validator | 65 portable skills + workflow mirrors | PASS |
| Agent Skills reference validator | 65 `skills/` + 67 `.kilo/skills/` = 132 validations | 132 passed, 0 failed |
| Replacement directory gate | 7 required replacement directories | PASS |
| Obsolete active workflow references | `skills/` and `.kilo/` workflow roots | 0 |
| `related_skills` resolution | Portable catalog | PASS |
| Relative skill links/assets | Portable and Kilo catalogs | PASS |
| Pinned updated provenance | 46 manifest rows compared with cloned upstream HEAD and `SKILL.md` path | PASS |
| License provenance | all 65 manifest rows | explicit identifiers; no `See upstream` placeholders |
| Commit-pin durability | all GitHub-backed manifest rows | full 40-character SHAs |
| Skill security scanner | 9 newly adopted external targets; scanner's own threat-signature fixtures excluded | 0 critical/high findings after remediation |
| Workflow smoke requirements | staged, branch, debug, commit-message, preflight | PASS |
| Workflow mirror byte equality | project, root docs, and Kilo workflow copies | PASS |
| Bash syntax | 8 scripts | 8 passed, 0 failed |
| Python syntax | 15 scripts | 15 passed, 0 failed |
| Node syntax | 3 JavaScript/CommonJS scripts | 3 passed, 0 failed |
| OpenAPI deterministic generation smoke test | `openapi-typescript@7.13.0`, same schema generated twice | PASS; identical SHA-256 |

## Baseline and remediation

The 2026-09-01 baseline passed 56 of 67 portable skill frontmatters and failed 11. The failures came from unsupported top-level fields, flow-style YAML metadata, and one unquoted description containing a colon.

The current catalog:

- moves project version/author/trigger fields under `metadata`;
- emits block-style YAML for project-curated review/workflow metadata;
- quotes descriptions when YAML requires it;
- verifies directory name equals frontmatter `name`;
- validates both the portable and Kilo staging catalogs.

## Workflow migration checks

The validator confirms that active workflow routing now uses:

- `react-router` with runtime mode/version detection;
- `ag-dev` for feature work and `ag-update` for upgrades;
- `shadcn` for shadcn/Tailwind v4 component workflows;
- `vitest` for Vitest-specific testing;
- `playwright-cli` for repeatable browser interaction;
- `playwright-best-practices` for Playwright test authoring/review;
- `openapi-typescript` for deterministic CLI generation;
- `accessibility` for evidence-led audits alongside `accessibility-compliance`;
- `react-doctor` only as a post-fix diagnostic;
- `skill-scanner` as the third-party skill intake gate.

The staged review still requires at least two independent sub-agents per selected skill and reads only `git diff --cached`. The branch review still pins source, target, and merge-base SHAs. The commit-message workflow remains message-only and does not stage, edit, commit, or push.

## Commands executed

```bash
python scripts/validate_skill_catalog.py
```

Result:

```text
catalog validation passed: 65 skills, 7 replacements present, no obsolete workflow references
```

The Agent Skills reference implementation was pinned from:

```text
https://github.com/agentskills/agentskills.git
commit 69ef37e9424c0a7ea9dd2293b559e43ec8176379
subdirectory skills-ref
```

Result:

```text
skills_ref_total=132 failed=0
```

Syntax checks:

```text
bash_syntax_total=8 failed=0
python_syntax_total=15 failed=0
node_syntax_total=3 failed=0
```

OpenAPI generation smoke test:

```text
openapi-typescript 7.13.0
first =91b58363e0dec407a19298c5cfaab8dbf9a8989749d2482577c3deb26235619f
second=91b58363e0dec407a19298c5cfaab8dbf9a8989749d2482577c3deb26235619f
generated lines=57
```

## Independent review

A read-only workflow reviewer found six medium-severity routing/policy inconsistencies and one low-severity duplicate after the first migration pass. All seven were corrected: baseline reviewer wording, shadcn preflight routing, conditional browser research, Playwright-to-DevTools fallback evidence, heavy-review routing, minimum two-reviewer clamping, and duplicate research-note references. Catalog, mirror, and reference validation were rerun after the fixes.

A second read-only provenance reviewer found three medium-severity issues: 12 license placeholders, 11 abbreviated commit pins, and an ambiguous `openapi-typescript` upstream-path claim. These were corrected with explicit licenses, full SHAs, source-backed attribution for `qa-test-planner` and `react-dev`, vendored Softaworks MIT license files, and separate local-skill versus pinned CLI documentation provenance for `openapi-typescript`. The catalog validator now enforces explicit licenses and full GitHub commit SHAs.

## Security and provenance notes

- Upstream repositories and pinned revisions are recorded in `SKILLS_MANIFEST.md` and `SKILL_SOURCES.md`.
- Direct replacement skills vendor their upstream license file where available.
- Documentation and reports contain no credentials.
- `skill-scanner` was run against nine newly adopted external targets. The shadcn pre-prompt command and PNG metadata findings were remediated; the rerun reported zero critical/high findings. The scanner's own threat-signature fixtures are intentionally excluded from self-scan totals.
- This report applies to the current working tree only; rerun validation after any skill or workflow change.
