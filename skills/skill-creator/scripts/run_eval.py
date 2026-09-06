#!/usr/bin/env python3
"""Score VS Code Chat Agent Skill routing observations.

The model calls happen inside VS Code through stateless Skill Trigger Evaluator
subagents. This helper only validates and scores their recorded JSON results, so
it never bypasses the selected BYOK provider.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

try:
    from .utils import parse_skill_md
except ImportError:
    from utils import parse_skill_md


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def score_observations(
    eval_set: list[dict],
    observations: list[dict],
    skill_name: str,
    description: str,
    trigger_threshold: float = 0.5,
) -> dict:
    for item in eval_set:
        if not isinstance(item, dict) or not isinstance(item.get("query"), str) or not item["query"].strip():
            raise ValueError("each eval item requires a non-empty string query")
        if not isinstance(item.get("should_trigger"), bool):
            raise ValueError("each eval item requires boolean should_trigger")
    expected = {item["query"]: item["should_trigger"] for item in eval_set}
    if len(expected) != len(eval_set):
        raise ValueError("eval queries must be unique")

    grouped: dict[str, list[bool]] = defaultdict(list)
    for item in observations:
        query = item.get("query")
        if query not in expected:
            raise ValueError(f"observation has unknown query: {query!r}")
        selected = item.get("selected_skill")
        if selected is not None and not isinstance(selected, str):
            raise ValueError("selected_skill must be a string or null")
        grouped[query].append(selected == skill_name)

    missing = [query for query in expected if not grouped[query]]
    if missing:
        raise ValueError(f"missing observations for {len(missing)} query(s): {missing}")

    results = []
    for query, should_trigger in expected.items():
        triggers = grouped[query]
        trigger_rate = sum(triggers) / len(triggers)
        passed = trigger_rate >= trigger_threshold if should_trigger else trigger_rate < trigger_threshold
        results.append(
            {
                "query": query,
                "should_trigger": should_trigger,
                "trigger_rate": trigger_rate,
                "triggers": sum(triggers),
                "runs": len(triggers),
                "pass": passed,
            }
        )

    passed = sum(item["pass"] for item in results)
    return {
        "skill_name": skill_name,
        "description": description,
        "results": results,
        "summary": {"total": len(results), "passed": passed, "failed": len(results) - passed},
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Score VS Code Skill Trigger Evaluator observations")
    parser.add_argument("--eval-set", required=True, type=Path)
    parser.add_argument("--observations", required=True, type=Path)
    parser.add_argument("--skill-path", required=True, type=Path)
    parser.add_argument("--description", help="description under evaluation; defaults to SKILL.md")
    parser.add_argument("--trigger-threshold", type=float, default=0.5)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    if not 0 <= args.trigger_threshold <= 1:
        parser.error("--trigger-threshold must be between 0 and 1")
    if not (args.skill_path / "SKILL.md").is_file():
        parser.error(f"no SKILL.md at {args.skill_path}")

    name, original_description, _ = parse_skill_md(args.skill_path)
    try:
        result = score_observations(
            load_json(args.eval_set),
            load_json(args.observations),
            name,
            args.description or original_description,
            args.trigger_threshold,
        )
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc

    rendered = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
