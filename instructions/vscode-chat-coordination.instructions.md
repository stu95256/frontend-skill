---
description: Coordination and verification rules for VS Code Chat agents.
applyTo: "**"
---

# VS Code Chat Coordination

- Use Agent Skills for reusable procedures and custom agents for tool restrictions, handoffs, and named subagent roles.
- Before delegating, verify that `agent/runSubagent` is enabled. Never simulate multiple reviewers in one context when a workflow requires independent subagents.
- Give every subagent a self-contained goal, relevant context, constraints, expected output, and completion criteria. Subagent invocations are stateless and cannot receive follow-up questions.
- Run independent read-only tasks in parallel. Keep dependent work and overlapping file edits sequential.
- Leave nested subagents disabled unless a specific bounded recursive workflow requires them.
- Do not hard-code a worker model unless the route has been tested. By default, let custom agents inherit the currently selected BYOK model.
- Do not claim a file change, command result, browser behavior, or external side effect without direct verification.
- Never commit, push, merge, publish, or rewrite history unless the user explicitly requests it.
