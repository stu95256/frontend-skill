# VS Code Chat Custom Agents

## User-facing workflow agents

- `Frontend Task Preflight`
- `Frontend Implementation`
- `Frontend Debug`
- `Frontend Staged Review`
- `Frontend Heavy Staged Review`
- `Frontend Branch Review`
- `Frontend Staged Commit Message`
- `VS Code Skill Creator`

## Protected workers

- `Frontend Researcher`
- `Frontend Plan Reviewer`
- `Frontend Implementer`
- `Frontend Verifier`
- `Frontend Reviewer`
- `Frontend Security Reviewer`
- `Frontend Review Validator`
- `Skill Trigger Evaluator`
- `Skill Description Optimizer`

Workers use `user-invocable: false`, which is VS Code's documented pattern for agents that are hidden from the picker but available for subagent invocation. They intentionally do not set `disable-model-invocation: true`, because that field blocks general model-initiated subagent use. Coordinators still restrict their own worker roster with explicit `agents` allowlists.

Coordinators invoke fresh stateless workers through `#tool:agent/runSubagent`. They do not require nested subagents and do not hard-code a model, so the current BYOK model is inherited when no invocation-specific model is chosen.
