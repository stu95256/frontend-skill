---
name: skill-creator
description: Create, evaluate, and improve VS Code Agent Skills with isolated test contexts.
license: Apache-2.0
---

# VS Code Agent Skill Creator

Create or improve Agent Skills that VS Code Chat can discover from `~/.copilot/skills/<name>/SKILL.md`. Optimize for predictable model behavior, progressive disclosure, and evaluation in fresh subagent contexts.

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
7. Use `#tool:agent/runSubagent` to invoke `Skill Trigger Evaluator` once per query and repetition. If that named worker is not installed, invoke an anonymous subagent with the same evaluator contract. Give it only the query and candidate names/descriptions—not the expected answer. Each invocation is independent and stateless.
8. Record each returned `{query, selected_skill, reason}` object and score the split with `scripts/run_loop.py` `score`.
9. Build a blinded optimizer packet with `scripts/run_loop.py` `prompt`, invoke `Skill Description Optimizer`, and apply its tagged response with `scripts/run_loop.py` `apply`.
10. Repeat with fresh evaluator invocations. Stop on full training success, no holdout improvement, or the configured iteration limit; use `scripts/run_loop.py` `best` to select the best holdout result.
11. Run separate procedure/output evaluations after routing succeeds. If comparing revisions, use blind randomized labels in fresh subagents.
12. Present the final skill, evaluation matrix, unresolved limitations, and installation path.

Subagent invocations are stateless. Never instruct the parent to resume a previous evaluator; create a new invocation with the complete task package.

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
- `context: fork` runs the entire skill in an isolated subagent. Use it only when the skill returns a self-contained result and does not require iterative user questions.
- Skill frontmatter cannot grant tools or restrict a subagent roster. Put those controls in `~/.copilot/agents/*.agent.md`.
- Do not hardcode a model name. BYOK agents inherit the selected Chat model unless an installed custom agent deliberately specifies another available model.
- Do not use nested subagents unless `chat.subagents.allowInvocationsFromSubagents` is enabled and nesting materially improves the task.

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
- `scripts/package_skill.py` — package a skill directory when a distributable archive is needed.
- `scripts/run_eval.py` — deterministically score recorded VS Code evaluator observations.
- `scripts/improve_description.py` — build optimizer packets and validate tagged responses without calling another provider.
- `scripts/run_loop.py` — persist train/holdout splits, iteration history, and best-description selection across stateless subagents.
- `scripts/generate_report.py` — render the resumable loop state as an HTML comparison report.
- `eval-viewer/generate_review.py` and `assets/eval_review.html` — optional human review UI.
- `agents/grader.md`, `agents/comparator.md`, and `agents/analyzer.md` — prompts that can be embedded in `agent/runSubagent` tasks.
- `references/schemas.md` — evaluation data schemas.

## Verification

Before completion:

- run this repository's `python scripts/validate_skill_catalog.py` when editing this catalog;
- run `uvx --from skills-ref agentskills validate <skill-directory>` when available;
- confirm every local Markdown link resolves;
- run each bundled script's help or validation path;
- report actual commands and results;
- do not commit or install the skill unless the user requested it.
