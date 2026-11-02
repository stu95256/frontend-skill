---
name: using-vscode-chat
description: Use when starting VS Code Chat work that should follow installed personal skills and agents.
license: MIT
---

# Using VS Code Chat

Apply VS Code Chat's native customization model instead of runtime-specific command names.

This catalog's `target: vscode` agents are configured for VS Code **Local**. Confirm the selected harness: this target controls file interpretation and does not switch a session. Native Copilot uses `task` rather than Local's `agent/runSubagent` and does not support the Local `agents` roster unchanged. Read the [review compatibility guide](../frontend-staged-review-workflow/references/vscode-copilot-compatibility.md) before reusing review instructions across harnesses.

## Discovery

- Personal Agent Skills: `~/.copilot/skills/<skill-name>/SKILL.md`.
- Catalog-installed custom agents: `~/.copilot/agents/*.agent.md`; Local's user-creation UI can use Profile storage instead. Confirm discovery in the active Profile, or configure `chat.agentFilesLocations` for the catalog directory.
- Catalog-installed instructions: `~/.copilot/instructions/*.instructions.md`; Local UI-created user instructions can use Profile storage. Confirm discovery or configure `chat.instructionsFilesLocations`.
- Personal hooks: `~/.copilot/hooks/*.json`.
- BYOK model configuration remains in the active VS Code profile, not in `~/.copilot`.

Use **Chat: Open Customizations** and Chat Diagnostics to confirm that VS Code loaded each artifact. Do not assume the repository's root `skills/` or `agents/` folders are discovered until they are installed into `~/.copilot`.

Use **Chat: Manage Language Models** to configure a BYOK provider/endpoint, then select that model in a Local session. It must support tool calling. `chat.agentHost.byokModels.enabled` enables experimental BYOK support for native Copilot Agent Host; it is not required for Local and does not convert this catalog. Provider context/output limits are real configuration; a Skill's token target does not change them. Built-in utility flows have separate `chat.utilityModel` / `chat.utilitySmallModel` selection, and BYOK does not supply Copilot-backed semantic search or inline completions. Use available text search when needed.

## Operating Rules

1. Let Copilot load relevant skills from their descriptions; do not paste every skill into context.
2. Use a custom agent when a workflow needs a constrained tool set, a handoff, or named worker roles.
3. For Local coordinators, enable `agent/runSubagent` and explicitly set `agentName` for a named worker, with `description` and a complete `prompt`. Omitting the name inherits the current agent's configuration. Native harnesses require their actual delegation schema and compatible custom-agent configuration.
4. Local calls are stateless: no follow-up questions, shared todo state, or inherited parent-chat assumptions. Supply decisive evidence in the final result; intermediate tool outputs are not automatically returned to the parent. Workflow JSON/token budgets are prompt instructions, not extra Local tool arguments.
5. Run independent read-only workers in parallel. Keep overlapping edits and dependent work sequential.
6. Leave nested subagents disabled unless a specific bounded recursive workflow requires them.
7. Do not hard-code a model in shared agents by default; let workers inherit the currently selected BYOK model unless a tested model route is intentional.
8. Verify changes with actual tools and report real outputs rather than plausible results.
9. Re-read the specific supporting reference when its step is reached, especially after context compaction. Keep task scope, retry limits, and verification gates in durable artifacts instead of assuming earlier instructions remain in context.

## Related Skill

Use `using-agent-skills` to choose the smallest exact set of engineering skills for the current task.

## Verification

A setup is ready only when Chat Diagnostics shows the intended skills and agents without load errors and a coordinator can visibly invoke an allowed worker through `agent/runSubagent`.
