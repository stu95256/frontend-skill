#!/usr/bin/env python3
"""Build and parse VS Code Skill Description Optimizer task packets.

The optimizer itself runs as a VS Code custom subagent so it inherits the active
BYOK model. This helper keeps prompt construction and response parsing
deterministic and testable.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    from .utils import parse_skill_md
except ImportError:
    from utils import parse_skill_md


def build_improvement_prompt(
    skill_name: str,
    skill_content: str,
    current_description: str,
    eval_results: dict,
    history: list[dict],
) -> str:
    failed_positive = [
        item for item in eval_results["results"] if item["should_trigger"] and not item["pass"]
    ]
    false_positive = [
        item for item in eval_results["results"] if not item["should_trigger"] and not item["pass"]
    ]
    failures = {
        "missed_relevant_queries": failed_positive,
        "incorrect_triggers": false_positive,
    }
    return f"""Improve the description for VS Code Agent Skill `{skill_name}`.

Current description:
<current_description>{current_description}</current_description>

Training failures (holdout results are intentionally absent):
<failures>{json.dumps(failures, indent=2, ensure_ascii=False)}</failures>

Prior attempts; do not repeat them mechanically:
<history>{json.dumps(history, indent=2, ensure_ascii=False)}</history>

Skill content:
<skill_content>{skill_content}</skill_content>

Generalize the user's intent rather than enumerating the test queries. Make the
trigger distinctive from neighboring skills, factual, and no more than 1024
characters. Return only `<new_description>...</new_description>`.
"""


def parse_description(response: str) -> str:
    match = re.search(r"<new_description>(.*?)</new_description>", response, re.DOTALL)
    if not match:
        raise ValueError("optimizer response is missing <new_description> tags")
    description = match.group(1).strip().strip('"')
    if not description:
        raise ValueError("optimizer returned an empty description")
    if len(description) > 1024:
        raise ValueError(f"optimizer description is {len(description)} characters; limit is 1024")
    return description


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare or parse a VS Code description-optimizer task")
    parser.add_argument("--eval-results", required=True, type=Path)
    parser.add_argument("--skill-path", required=True, type=Path)
    parser.add_argument("--history", type=Path)
    parser.add_argument("--prompt-output", required=True, type=Path)
    parser.add_argument("--response", type=Path, help="optional optimizer response to parse")
    parser.add_argument("--result-output", type=Path)
    args = parser.parse_args()

    try:
        eval_results = json.loads(args.eval_results.read_text(encoding="utf-8"))
        history = json.loads(args.history.read_text(encoding="utf-8")) if args.history else []
        name, description, content = parse_skill_md(args.skill_path)
        prompt = build_improvement_prompt(name, content, description, eval_results, history)
        args.prompt_output.write_text(prompt, encoding="utf-8")

        if args.response:
            improved = parse_description(args.response.read_text(encoding="utf-8"))
            output = {
                "description": improved,
                "history": history
                + [
                    {
                        "description": description,
                        "passed": eval_results["summary"]["passed"],
                        "total": eval_results["summary"]["total"],
                    }
                ],
            }
            rendered = json.dumps(output, indent=2, ensure_ascii=False) + "\n"
            if args.result_output:
                args.result_output.write_text(rendered, encoding="utf-8")
            print(rendered, end="")
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc


if __name__ == "__main__":
    main()
