# VS Code Chat Custom Agents

These agent files target **VS Code Local** (`target: vscode`). Native Copilot is a different harness with different delegation and supported frontmatter. The target field does not select the running harness. See [compatibility and actual invocation arguments](../skills/frontend-staged-review-workflow/references/vscode-copilot-compatibility.md).

## User-facing agents

- `Frontend Implementation`
- `Frontend Review` — selects staged, heavy staged, or branch review mode
- `VS Code Skill Creator`

## Protected workers

- `Frontend Implementer`
- `Frontend Verifier`
- `Frontend Reviewer`
- `Frontend Security Reviewer`
- `Frontend Review Validator`
- `Skill Trigger Evaluator`
- `Skill Description Optimizer`

Workers use `user-invocable: false`, which is VS Code's documented pattern for agents that are hidden from the picker but available for subagent invocation. They intentionally do not set `disable-model-invocation: true`, because that field blocks general model-initiated subagent use. Coordinators still restrict their own worker roster with explicit `agents` allowlists.

Local coordinators invoke fresh stateless workers through `#tool:agent/runSubagent`, explicitly selecting a worker with `agentName` and providing `description` and the complete assignment in `prompt`. Omitting `agentName` inherits the current agent; catalog coordinators do not use that fallback. All three coordinators guard top-level invocation and keep their orchestration skills inline; all seven workers explicitly set `agents: []`. They do not require nested subagents and do not hard-code a model; BYOK workers continue with the selected model unless another is explicitly configured.

The installer stores these files under `~/.copilot/agents`; Local UI-created user agents can instead live in Profile storage. Check actual discovery before dispatch, especially with a custom install target. See [setup and BYOK configuration](../docs/VS_CODE_CHAT_SETUP.zh-TW.md).

Select `Frontend Review` at the top level; it sets `disable-model-invocation: true` to discourage accidental nested orchestration. Direct use of a review Skill in another top-level agent is supported. The review coordinator directly dispatches primary reviewers, an optional Azure description check using `Frontend Reviewer`, and bounded validator batches. It retries recoverable failed calls once with full immutable evidence. See the [runtime/evidence protocol](../skills/frontend-staged-review-workflow/references/runtime-and-evidence.md).

The review coordinator's `ado/*` and `ado-remote-mcp/*` tool namespaces support common Azure DevOps MCP server names when connected. A custom MCP server name must be enabled under its actual namespace in the coordinator tool selection and the catalog validator's tool allowlist; discovery never assumes tools exist. Azure text is captured read-only by the coordinator and supplied to the auxiliary worker. Missing MCP is a disclosed optional skip. No Azure write operation is part of review.

Deterministic single-pass procedures, such as generating a staged commit subject, remain Agent Skills instead of occupying the agent picker. Closely related review scopes share the parameterized `Frontend Review` coordinator while retaining their separate policy Skills.
