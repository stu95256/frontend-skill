---
name: skill-creator
description: Create, evaluate, and improve VS Code Agent Skills with isolated test contexts.
license: Apache-2.0
---

# VS Code Agent Skill Creator

Create or improve Agent Skills that VS Code Chat can discover from `~/.copilot/skills/<name>/SKILL.md`. Optimize for predictable model behavior, progressive disclosure, and evaluation in fresh subagent contexts.

This workflow targets VS Code Local, including BYOK, and runs in the top-level **VS Code Skill Creator** agent. Keep it inline. If already delegated, return `needs_parent_dispatch` instead of creating nested workers. Native Copilot requires adapted agent configuration and its actual `task` schema; see [harness compatibility](../frontend-staged-review-workflow/references/vscode-copilot-compatibility.md).

## Required structure

```text
<skill-name>/
├── SKILL.md
├── scripts/       # deterministic helpers only
├── references/    # details loaded when needed
├── templates/     # files copied into output
└── assets/        # non-context resources
```

`SKILL.md` must start at byte zero with YAML frontmatter containing:

```yaml
---
name: lowercase-hyphenated-name
description: What the skill does and when Copilot should load it.
---
```

The directory name must equal `name`, use lowercase letters, digits, and hyphens, and be at most 64 characters. Keep the description under 1,024 characters. Use `argument-hint`, `user-invocable`, `disable-model-invocation`, or `context: fork` only when their behavior is intentional.

## Procedure

1. Clarify the capability, trigger examples, non-trigger examples, output contract, and constraints.
2. Search installed skills before creating a duplicate. Extend an existing skill when it owns the same trigger.
3. Draft the smallest sufficient `SKILL.md`. Move bulky details and deterministic logic to supporting files.
4. Validate frontmatter, links, scripts, and directory naming.
5. Create 8–12 realistic routing queries:
   - positive prompts that should load the skill;
   - near-miss negatives that should not load it;
   - ambiguous prompts that compete with adjacent skills.
6. Start a resumable evaluation ledger with `scripts/run_loop.py` `init`. It creates a stratified training/holdout split; keep holdout results out of optimizer prompts.
7. Invoke `agent/runSubagent` with `agentName="Skill Trigger Evaluator"`, a short `description`, and a complete `prompt` once per query and repetition. Give it only the query, candidate names/descriptions, and expected output schema—not the expected answer. Each invocation is independent and stateless. If the named role is missing/disallowed, report evaluation `BLOCKED`; an anonymous call inherits the coordinator and is not a blind routing evaluator.
8. Record each returned `{query, selected_skill, reason}` object and score the split with `scripts/run_loop.py` `score`.
9. Build a blinded optimizer packet with `scripts/run_loop.py` `prompt`, invoke `Skill Description Optimizer`, and apply its tagged response with `scripts/run_loop.py` `apply`.
10. Repeat with fresh evaluator invocations. Stop on full training success, no holdout improvement, or the configured iteration limit; use `scripts/run_loop.py` `best` to select the best holdout result.
11. After routing succeeds, evaluate actual procedure/output behavior separately. Independent execution, grading, or blind revision comparison requires discovered, allowed roles with compatible tools/instructions; the current routing-only roster does not provide those roles. Otherwise record that evaluation as blocked or parent-only, with observed evidence and limits; do not claim an independent pass. Use randomized A/B labels when a compatible independent comparison is available.
12. Present the final skill, evaluation matrix, unresolved limitations, and installation path.

Use the same explicit invocation arguments with `agentName="Skill Description Optimizer"` for optimization. Local invocations are stateless. Never instruct the parent to resume a previous evaluator; create a new invocation with the complete task package. Only the final returned result and verified shared artifacts are evidence; do not assume the parent receives the worker's intermediate tool outputs. JSON formats are prompt contracts, not runtime-enforced output schemas.

## Evaluation commands

```bash
SC=~/.copilot/skills/skill-creator/scripts
python3 "$SC/run_loop.py" init --eval-set eval.json --skill-path ./my-skill --state loop.json
python3 "$SC/run_loop.py" score --state loop.json --split train --observations train-observations.json
python3 "$SC/run_loop.py" prompt --state loop.json --output optimizer-prompt.md
python3 "$SC/run_loop.py" score --state loop.json --split test --observations holdout-observations.json
python3 "$SC/run_loop.py" apply --state loop.json --response optimizer-response.txt
python3 "$SC/run_loop.py" best --state loop.json
python3 "$SC/generate_report.py" loop.json --output report.html
```

## VS Code-specific rules

- Write procedures in terms of capabilities rather than another agent runtime's tool names.
- For parallel evaluation, the selected parent agent must have the `agent` tool enabled.
- `context: fork` is experimental and requires `github.copilot.chat.skillTool.enabled`. It runs the entire skill in a subagent. Use it only for self-contained work that needs neither user questions nor further delegation; never fork this skill or the implementation/review coordinator skills.
- Skill frontmatter, including portable `allowed-tools` metadata, does not grant the selected Local agent tools or install workers. Put effective tool/roster controls in discovered custom agents; see [discovery](../using-vscode-chat/SKILL.md).
- Do not hardcode a model name. BYOK agents inherit the selected Chat model unless an installed custom agent deliberately specifies another available model.
- This catalog uses one delegation level. Workers do not dispatch workers; keep `chat.subagents.allowInvocationsFromSubagents` disabled.

## Evaluation record

For every test case record:

```json
{
  "query": "realistic user request",
  "should_trigger": true,
  "selected_skill": "candidate-skill",
  "reason": "short routing rationale"
}
```

Treat an unparseable or incomplete evaluation as a failure. Do not infer a pass from fluent prose.

## Progressive disclosure

Keep the main file focused on decisions and the ordered procedure. Link supporting material with relative paths and state when to read it. Do not duplicate the same rule in the main file and a reference.

Useful retained helpers:

- `scripts/quick_validate.py` — basic package validation.
- `scripts/package_skill.py` — optional ZIP-based `.skill` export, not a VS Code installer. For VS Code, extract/copy the complete skill folder into a supported discovery location.
- `scripts/run_eval.py` — deterministically score recorded VS Code evaluator observations.
- `scripts/improve_description.py` — build optimizer packets and validate tagged responses without calling another provider.
- `scripts/run_loop.py` — persist train/holdout splits, iteration history, and best-description selection across stateless subagents.
- `scripts/generate_report.py` — render the resumable loop state as an HTML comparison report.
- `eval-viewer/generate_review.py` and `assets/eval_review.html` — optional human review UI.
- `agents/grader.md`, `agents/comparator.md`, and `agents/analyzer.md` — retained behavioral-evaluation prompt resources, not registered VS Code custom agents. The current evaluator/optimizer roles cannot impersonate them. Use a separately configured, discovered and allowed compatible named role, or perform the optional analysis in the parent and disclose the lack of independent evaluation. A read-only worker returns the JSON; the parent writes it. Supply actual saved final results/artifacts and label any missing transcript; Local does not automatically deliver a full worker transcript.
- `references/schemas.md` — evaluation data schemas.

## Verification

Before completion:

- run this repository's `python scripts/validate_skill_catalog.py` when editing this catalog;
- run `uvx --from skills-ref agentskills validate <skill-directory>` when available;
- confirm every local Markdown link resolves;
- run each bundled script's help or validation path;
- report actual commands and results;
- do not commit or install the skill unless the user requested it.
