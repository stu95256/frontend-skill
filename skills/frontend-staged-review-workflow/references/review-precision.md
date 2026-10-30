# Review precision references

Consult when maintaining the evidence gate or evaluating false positives. These are design references, not additional runtime instructions. Checked 2026-10-30; linked upstream prompts may change.

## Sources and adopted principles

- [OpenAI review rubric](https://github.com/openai/codex/blob/main/codex-rs/prompts/templates/review/rubric.md) and [review-agent sample](https://github.com/openai/codex/blob/main/codex-rs/skills/src/assets/samples/review-agent/SKILL.md): require an actionable introduced defect, demonstrably affected code and no unstated assumptions. Inspect callers and tests; accept zero findings. Match the rigor of the project.
- [Anthropic code-review command](https://github.com/anthropics/claude-plugins-official/blob/main/plugins/code-review/commands/code-review.md): validate individual candidate bugs before publishing and remove unvalidated claims. Adopt focused claim verification within the existing validator passes. Do not copy its model assignments, PR posting permissions, tool assumptions, or restrictions that would suppress genuine bugs with reachable input/state preconditions.
- [A Practical Approach to Verifying Code at Scale](https://alignment.openai.com/scaling-code-verification/): prioritize useful, accurate findings; repository context and execution evidence can improve precision. Multiple reviewers or extra comments alone do not establish quality.
- [Are LLMs Reliable Code Reviewers?](https://arxiv.org/html/2603.00539v1), arXiv preprint: richer explanation/fix prompts increased rejection of correct implementations in the studied settings. Compare original and proposed behavior when permitted, rather than trusting persuasive rationales. The study uses small Python benchmark tasks and specific model snapshots; its rates do not establish performance on frontend repositories. Passing a limited test suite cannot prove correctness.
- [GitHub ReviewBench](https://github.blog/ai-and-ml/reviewbench-an-open-benchmark-for-ai-code-review/): evaluate precision and recall separately and judge new findings on their evidence instead of assuming the known issue list is exhaustive.

## Behavioral evaluation

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

Record the model/version, packets, selected criteria, raw candidates, validator decisions and final findings. Human-adjudicate disputed and newly discovered claims. Compare final precision (valid findings / all findings), recall of known valid defects, false alarms on clean changes, unresolved review rate and review cost. Track rejected genuine defects as well as removed noise; filtering everything is not success. Repeat across comparable runs before claiming reduced false positives. Format checks and catalog tests do not measure reviewer accuracy.
