# Review precision references

Consult when maintaining the evidence gate or evaluating false positives. These are design references, not additional runtime instructions. Checked 2026-10-30; linked upstream prompts may change.

## Sources and adopted principles

- [OpenAI review rubric](https://github.com/openai/codex/blob/main/codex-rs/prompts/templates/review/rubric.md) and [review-agent sample](https://github.com/openai/codex/blob/main/codex-rs/skills/src/assets/samples/review-agent/SKILL.md): require an actionable introduced defect, demonstrably affected code and no unstated assumptions. Inspect callers and tests; accept zero findings. Match the rigor of the project.
- [Anthropic code-review command](https://github.com/anthropics/claude-plugins-official/blob/main/plugins/code-review/commands/code-review.md): validate individual candidate bugs before publishing and remove unvalidated claims. Adopt focused claim verification within the existing validator passes. Do not copy its model assignments, PR posting permissions, tool assumptions, or restrictions that would suppress genuine bugs with reachable input/state preconditions.
- [A Practical Approach to Verifying Code at Scale](https://alignment.openai.com/scaling-code-verification/): prioritize useful, accurate findings; repository context and execution evidence can improve precision. Multiple reviewers or extra comments alone do not establish quality.
- [Are LLMs Reliable Code Reviewers?](https://arxiv.org/html/2603.00539v1), arXiv preprint: richer explanation/fix prompts increased rejection of correct implementations in the studied settings. Compare original and proposed behavior when permitted, rather than trusting persuasive rationales. The study uses small Python benchmark tasks and specific model snapshots; its rates do not establish performance on frontend repositories. Passing a limited test suite cannot prove correctness.
- [GitHub ReviewBench](https://github.blog/ai-and-ml/reviewbench-an-open-benchmark-for-ai-code-review/): evaluate precision and recall separately and judge new findings on their evidence instead of assuming the known issue list is exhaustive.

## Runtime and dependency sources

Checked 2026-11-02. These sources support mechanics; retry budgets, Low/nit policy and batch sizes are this catalog's design choices, not claimed platform defaults.

For the checked Local call schema, native Copilot differences, inherited-role fallback risk and result-delivery limits, see [VS Code/Copilot compatibility](vscode-copilot-compatibility.md). It links the official migration guide and Microsoft's implementation, rather than treating another product's subagent API as a VS Code API.

- [VS Code subagents](https://code.visualstudio.com/docs/agents/run/subagents): Local invocations have separate, stateless context; nested delegation is disabled by default. Use direct top-level orchestration and complete fresh assignments.
- [VS Code custom agent reference](https://code.visualstudio.com/docs/agents/reference/custom-agent-file-reference): `agents: []` prevents delegation; `disable-model-invocation` guards coordinator invocation; MCP tool namespaces use the configured server name. An explicit coordinator allowlist can override the invocation guard, so retain the runtime depth check.
- [OpenAI multi-agent guidance](https://developers.openai.com/api/docs/guides/responses-multi-agent): bounded independent tasks have separate context and require root synthesis. Native host tools differ from VS Code Local; do not assume one tool schema or nesting limit applies everywhere.
- [Azure DevOps MCP overview](https://learn.microsoft.com/en-us/azure/devops/mcp-server/mcp-server-overview?view=azure-devops) and [remote configuration](https://learn.microsoft.com/en-us/azure/devops/mcp-server/remote-mcp-server?view=azure-devops): PR/work-item reads depend on available toolsets and authentication. The optional check does not create a connection or request write access. Documented remote configuration uses `ado-remote-mcp`; local deployments commonly use `ado`, with actual names discovered at runtime.
- [npm lockfile reference](https://docs.npmjs.com/cli/v11/configuring-npm/package-lock-json/): package entries identify exact resolution and integrity. Use the affected importer's equivalent entries for npm, pnpm or Yarn and account for patches/overrides before relying on implementation behavior.

## Behavioral evaluation cases

Evaluate using fixed snapshots and a held-out set of previously adjudicated reviews. Include clean changes as well as genuine defects; keep expected answers out of reviewer packets. Useful paired cases include:

| Context pair | What the evaluation should distinguish |
|---|---|
| Non-null assertion behind a verified caller guard / a new caller bypassing that guard | Syntax alone versus a reachable null failure introduced by the diff |
| Existing upstream validation / validation removed in the reviewed change | Duplicate-validation advice versus a demonstrated trust-boundary regression |
| A long file or repeated branches / the change creates a documented ownership violation or concrete dependency failure | Refactoring preference versus supported maintainability impact |
| A dependency API available in the pinned version / a change calling an unavailable API | Recalled API behavior versus actual version compatibility |
| An intentional return-value change within the approved contract / the same change breaking a documented caller | Invented requirements versus a contract regression |
| Fully inspected clean change / the same diff without essential caller context | Successful zero findings versus incomplete evidence |
| A reachable race or malformed-input failure / an existing guard making the scenario unreachable | Valid conditional defects versus invented preconditions |
| Changed Query wrapper/key factory / an unchanged installed Query dependency | Risk-based `react-state-management` dispatch versus catalog over-selection |
| Existing semantically equivalent helper/key with a new bypass / a merely similar helper in another domain | Evidenced nonblocking convention finding versus a preferred abstraction |
| Installed source matching the lock entry and patch / stale node_modules or latest upstream source | Version-grounded implementation claim versus unresolved decisive evidence |
| Azure MCP unavailable after a bounded attempt / a missing required code validator batch | Optional disclosed skip versus `Incomplete` |
| A complete packet/result / missing excerpt, delivery tail or required batch IDs | Independently inspectable proof versus transport failure; fresh bounded retry without double-counting |

Record the model/version, packets, selected criteria, raw candidates, validator decisions and final findings. Human-adjudicate disputed and newly discovered claims. Compare final precision (valid findings / all findings), recall of known valid defects, false alarms on clean changes, unresolved review rate and review cost. Track rejected genuine defects as well as removed noise; filtering everything is not success. Repeat across comparable runs before claiming reduced false positives. Format checks and catalog tests do not measure reviewer accuracy.
