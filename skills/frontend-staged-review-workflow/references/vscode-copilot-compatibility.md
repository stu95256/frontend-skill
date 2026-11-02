# VS Code review delegation compatibility

Checked against official documentation and upstream implementation on 2026-11-02. This catalog's custom agents use `target: vscode`: their authored configuration targets **VS Code Local**. The selected session harness still determines execution; this frontmatter does not switch a Copilot session to Local. Do not infer the harness from a model/provider name or from the fact that the editor is VS Code.

## Harness boundary

| Concern | VS Code Local, this catalog's configured target | Native Copilot harness |
|---|---|---|
| Delegation | `agent/runSubagent` | Native `task`; inspect the exposed schema |
| Named worker selection | `agentName`, exact case-sensitive custom-agent name | Native agent selection; do not copy Local argument names |
| Coordinator roster | `agents` allowlist plus the `agent` tool set | Local `agents` frontmatter is unsupported; requires an adapted policy/configuration |
| Worker no-delegation rule | `agents: []`, no agent tool, and explicit instructions | Verify native controls; do not assume the Local field is enforced |
| Repeated work | Fresh self-contained invocations; no follow-up to the same Local invocation | Native capabilities may differ; this review still uses fresh independent assignments |

For these installed agents, select Local in a new Chat session and choose Frontend Review at the top level. A user asking for native Copilot support needs both agent configuration and tool-call adaptation; changing `target` or renaming `runSubagent` alone is insufficient. Keep the current Local configuration until an adapted version has been verified in the destination harness.

## Actual Local call

Read the exposed tool schema. In the checked upstream implementation, `prompt` and `description` are required; `agentName` and `model` are optional. For strict staged/branch/heavy review, always supply `agentName` for a discovered, allowed worker. `#tool:agent/runSubagent` is a prompt reference: printing this text or a JSON example does not execute a tool.

Example arguments, populated before an actual tool invocation:

```json
{
  "agentName": "Frontend Reviewer",
  "description": "Review query mutation correctness",
  "prompt": "{COMPLETE_FROZEN_ASSIGNMENT_AND_POPULATED_REVIEWER_PROMPT}"
}
```

Use `Frontend Security Reviewer` or `Frontend Review Validator` for those roles. Reviewer IDs, evidence manifests, snapshot/scope IDs, criteria and requested result schema belong **inside `prompt`**, not additional tool arguments. The worker name is not a reviewer/seat ID. Omit `model` unless explicitly selecting a supported model; do not invent a model ID.

Omitting `agentName` uses the current agent's configuration. It does not select a neutral general-purpose reviewer. In particular, do not omit it to bypass a missing/disallowed worker or copy Frontend Review into an alleged independent reviewer. Missing required named workers means `Incomplete` in these three workflows. A generic single-task review may use an inherited-role invocation only when the parent instructions/tools are compatible, with that limitation disclosed; it cannot fill strict review quorum.

The checked schema has no `maxTokens`, `max_output_tokens`, `response_format`, `output_schema`, `tools`, `resume`, `session_id` or `run_in_background` argument. Do not pass those fields from another host. Recheck the actual schema if a future version exposes new capabilities. Use the named worker's frontmatter to configure tools. Token targets, JSON fields, end markers, retry caps and quorum are **workflow instructions**, not VS Code runtime settings or enforced structured output.

## Result and scheduling semantics

Local returns the worker's final text as a tool result; the checked implementation clears accumulated text after worker tool calls. The parent must not assume it receives all worker tool outputs or a conversation transcript. Require the final result to include the actual decisive excerpts needed by a read/search-only validator. In this workflow, “raw worker output” means the returned final result exactly as received, not inaccessible internal activity or logs.

Parse/validate that returned text against the requested workflow schema. A tool error or the fallback text `Agent completed with no output` is a failed attempt, never a zero-finding review. Markdown instructions cannot force JSON, prevent truncation or configure the model's output limit. The delivery tail detects some incomplete responses; it does not prove complete reasoning or transport correctness.

Local normally completes the invocation before returning its result. Do not invent a native wait/resume/session API. If the actual host exposes a deferred operation, use only that host's documented completion mechanism. Further review or repair uses a new call with a complete prompt. Concurrent independent calls may be scheduled within actual tool/model limits; `max_parallel_subagents` in the heavy-mode plan is not a VS Code setting or a guarantee of parallel execution.

## Configuration checks

- Coordinator: `tools` contains `agent`, `agents` names resolve to installed/enabled workers, and `disable-model-invocation: true` discourages accidental coordinator nesting. Another coordinator's explicit allowlist can override that guard, so keep the runtime top-level check.
- Workers: `user-invocable: false` hides them from the picker without disabling normal delegation. `agents: []` and no agent tool prevent recursive work in Local. A custom worker's tool list can override the parent's selected list; do not assume an anonymous invocation has the same restrictions.
- Skills: these review Skills load inline by default. Do not add `context: fork` to a coordinator Skill: that would place its delegation workflow in a subagent and conflict with the single-level plan. Reading a Skill supplies criteria, not a new agent/tool registration.
- MCP: `<server name>/*` is valid only for actually configured and enabled tools. It does not connect/authenticate a server. Prompt-file tool lists can override custom-agent lists in Local; inspect effective tools if Azure or delegation is unexpectedly absent.
- Discovery: repository-root `skills/` and `agents/` are packaging directories, not default discovery locations. Use the catalog installer or configured supported locations, then check Open Customizations and Chat Diagnostics. Confirm actual named worker calls in a disposable Local session before claiming runtime verification.

## Official sources

- [VS Code subagents](https://code.visualstudio.com/docs/agents/run/subagents): separate Local/native harness behavior, self-contained stateless calls, model selection and default nesting restriction.
- [Custom agent file reference](https://code.visualstudio.com/docs/agents/reference/custom-agent-file-reference): `target` interpretation, tool lists, agent roster/visibility and MCP namespaces.
- [Copilot migration FAQ](https://code.visualstudio.com/docs/agent-customization/migrate-customizations#why-does-my-coordinators-subagent-invocation-stop-working): `runSubagent` and native `task` require different invocation/configuration checks.
- [Agent Skills](https://code.visualstudio.com/docs/agent-customization/agent-skills): supported discovery locations and experimental forked Skill execution.
- [Microsoft's Local runSubagent implementation](https://github.com/microsoft/vscode/blob/main/src/vs/workbench/contrib/chat/common/tools/builtinTools/runSubagentTool.ts): `IRunSubagentToolInputParams`, `getToolData`, inherited current-agent configuration, returned text and error handling. This is checked upstream source, not proof of the installed build's implementation; the exposed session schema remains authoritative.
