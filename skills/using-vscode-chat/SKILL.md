---
name: using-vscode-chat
description: Use when starting VS Code Chat work that should follow installed personal skills and agents.
license: MIT
---

# Using VS Code Chat

Apply VS Code Chat's native customization model instead of runtime-specific command names.

## Discovery

- Personal Agent Skills: `~/.copilot/skills/<skill-name>/SKILL.md`.
- Personal custom agents: `~/.copilot/agents/*.agent.md`.
- Personal instructions: `~/.copilot/instructions/*.instructions.md`.
- Personal hooks: `~/.copilot/hooks/*.json`.
- BYOK model configuration remains in the active VS Code profile, not in `~/.copilot`.

Use **Chat: Open Customizations** and Chat Diagnostics to confirm that VS Code loaded each artifact. Do not assume the repository's root `skills/` or `agents/` folders are discovered until they are installed into `~/.copilot`.

## Operating Rules

1. Let Copilot load relevant skills from their descriptions; do not paste every skill into context.
2. Use a custom agent when a workflow needs a constrained tool set, a handoff, or named worker roles.
3. Enable `agent/runSubagent` for coordinators. Every subagent invocation receives a self-contained prompt and returns one final result.
4. Treat subagent calls as stateless: no follow-up questions, shared todo state, or inherited parent-chat assumptions.
5. Run independent read-only workers in parallel. Keep overlapping edits and dependent work sequential.
6. Leave nested subagents disabled unless a specific bounded recursive workflow requires them.
7. Do not hard-code a model in shared agents by default; let workers inherit the currently selected BYOK model unless a tested model route is intentional.
8. Verify changes with actual tools and report real outputs rather than plausible results.

## Related Skill

Use `using-agent-skills` to choose the smallest exact set of engineering skills for the current task.

## Verification

A setup is ready only when Chat Diagnostics shows the intended skills and agents without load errors and a coordinator can visibly invoke an allowed worker through `agent/runSubagent`.
