---
description: Coordination and verification rules for VS Code Chat agents.
applyTo: "**"
---

# VS Code Chat Coordination

- Use Agent Skills for reusable procedures and custom agents for tool restrictions, handoffs, and named subagent roles.
- This catalog's coordinator configuration targets VS Code Local, including BYOK. Confirm the selected harness; `target: vscode` does not switch the running session. Native Copilot requires compatible native agent configuration and its `task` tool schema.
- Before delegating in Local, verify that `agent/runSubagent` is enabled and required named workers are discovered/allowed. Invoke it with explicit `agentName`, `description`, and a complete `prompt`. Omitting the name inherits the current agent's instructions/tools; it does not create a neutral role. Never simulate independent reviewers or evaluators when the workflow requires them.
- Give every subagent a self-contained goal, relevant context, constraints, expected output, and completion criteria. Local invocations are stateless and cannot receive follow-up questions. Require needed evidence in the returned final text or verified shared artifacts; intermediate worker tool outputs are not automatically delivered to the parent.
- Run independent read-only tasks in parallel. Keep dependent work and overlapping file edits sequential.
- Run catalog coordinators only at the top level and keep their skills inline. Workers do not dispatch workers; this catalog does not require enabling nested subagents.
- Do not hard-code a worker model unless the route has been tested. By default, let custom agents inherit the currently selected BYOK model.
- Do not claim a file change, command result, browser behavior, or external side effect without direct verification.
- Never commit, push, merge, publish, or rewrite history unless the user explicitly requests it.
