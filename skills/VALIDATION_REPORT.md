# VS Code Chat Catalog Validation Report

Generated: 2026-09-06

## Result

**PASS**

Validated repository state:

- 67 Agent Skills under `skills/*/SKILL.md`
- 17 custom agents under `agents/*.agent.md`
- 2 personal instruction files under `instructions/*.instructions.md`
- 8 user-facing workflow agents and 9 protected worker agents
- no legacy runtime tree, legacy tool identifiers, or `.workflow.md` files

## Executed checks

### Repository validator

```bash
python scripts/validate_skill_catalog.py
```

Observed result:

```text
VS Code Chat catalog validation passed: 67 skills, 17 custom agents, 2 instruction files, no legacy runtime artifacts
```

The validator checks Skill names/frontmatter, flat metadata, manifest parity, custom-agent names/tool sets/allowlists/handoffs, worker protection, relative links, instruction frontmatter, expected workflow mappings, and legacy runtime markers.

### Agent Skills reference validator

```bash
uvx --from skills-ref agentskills validate skills/<skill-name>
```

Executed for every Skill directory.

```text
agentskills validated=67 failed=0
```

### Python and shell syntax

```bash
python -m compileall -q scripts skills
bash -n scripts/install-vscode-chat.sh
git diff --check
```

All completed with exit code 0.

### Conversion regression tests

```bash
python -m unittest -v tests/test_vscode_conversion.py
```

Observed result:

```text
Ran 4 tests
OK
```

The suite covers catalog validation, exact installer counts, tracked and untracked SDD review packages, and Skill Creator train/holdout isolation plus report generation.

### Installer smoke test

Installed into a temporary target and counted the copied runtime assets:

```text
installed skills=67 agents=17 instructions=2
```

The temporary target was removed after verification.

### Migration coverage

Compared the former staging catalog directory names from `HEAD` with the current catalog. Every former skill is represented; the only intentional slug migration is:

```text
using-superpowers -> using-vscode-chat
```

The two formerly legacy-runtime-only skills, `frontend-task-preflight` and `frontend-heavy-staged-review-workflow`, are now first-class catalog entries.

### Converted workflow helper tests

The durable subagent workflow helpers were exercised in a temporary Git repository with both tracked and untracked edits:

```text
sdd helpers: tracked and untracked WORKTREE review passed
```

The Skill Creator's resumable train/holdout lifecycle was exercised through `init`, `score`, `prompt`, `apply`, and `best`; its model-facing steps remain inside the VS Code custom agents so they inherit the active BYOK model.

## Independent review disposition

### VS Code Chat subagent re-audit

Rechecked against the current VS Code Subagents and Custom Agents documentation:

- seven coordinator agents declare `tools: [agent, ...]`, use exact `agents` allowlists, and reference `#tool:agent/runSubagent` in their bodies;
- nine workers use `user-invocable: false`, leave model invocation enabled, have no `agent` tool, and cannot create nested subagents;
- all allowlisted names resolve case-sensitively to installed `.agent.md` definitions;
- worker calls are one-shot and stateless; retry/fix instructions require a fresh invocation with the complete packet;
- no orchestration Skill uses `context: fork`, so the workflows do not depend on nested subagents while `chat.subagents.allowInvocationsFromSubagents` remains disabled;
- no worker pins a model, so VS Code follows its documented model priority and inherits the active BYOK model unless the parent explicitly requests another available model.

An independent review identified stale personal-skill paths, obsolete runtime names, stale README totals, missing checklists, nonportable nested metadata, and lost helper behavior in the first conversion pass. These were corrected: the SDD recovery/review helpers were restored and adapted, and Skill Creator evaluation was rebuilt around hidden BYOK subagents plus a resumable local scoring ledger. All validation was then rerun.

The final subagent audit uses VS Code's documented subagent-only worker pattern: `user-invocable: false` with model invocation left enabled. Coordinator `agents` allowlists are validated for exact names and each worker is referenced by at least one coordinator.

## Remaining environment verification

This repository was converted and mechanically exercised on the available Windows development host. The final discovery and live subagent checks must be run in the target Ubuntu VS Code profile after installation:

1. Run **Chat: Open Customizations**.
2. Inspect Chat Diagnostics.
3. Select **Frontend Task Preflight** and verify its handoff.
4. Stage a small test diff and select **Frontend Staged Review**.
5. Confirm that at least two independent `Frontend Reviewer` subagent calls appear.

See [`../docs/VS_CODE_CHAT_SETUP.zh-TW.md`](../docs/VS_CODE_CHAT_SETUP.zh-TW.md).
