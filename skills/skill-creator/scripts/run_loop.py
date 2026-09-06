#!/usr/bin/env python3
"""Maintain a resumable VS Code Agent Skill evaluation loop.

Model calls are deliberately external: the VS Code Skill Creator coordinator
invokes protected BYOK subagents and records their JSON. This script owns the
train/holdout split, scoring state, history, and best-description selection.
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

try:
    from .improve_description import build_improvement_prompt, parse_description
    from .run_eval import score_observations
    from .utils import parse_skill_md
except ImportError:
    from improve_description import build_improvement_prompt, parse_description
    from run_eval import score_observations
    from utils import parse_skill_md


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def stratified_split(eval_set: list[dict], holdout: float, seed: int) -> tuple[list[str], list[str]]:
    rng = random.Random(seed)
    groups = {
        True: [item["query"] for item in eval_set if item["should_trigger"]],
        False: [item["query"] for item in eval_set if not item["should_trigger"]],
    }
    train: list[str] = []
    test: list[str] = []
    for queries in groups.values():
        rng.shuffle(queries)
        count = int(len(queries) * holdout)
        if holdout > 0 and len(queries) > 1:
            count = max(1, min(count, len(queries) - 1))
        elif len(queries) <= 1:
            count = 0
        test.extend(queries[:count])
        train.extend(queries[count:])
    return train, test


def subset(state: dict, split: str) -> list[dict]:
    selected = set(state[f"{split}_queries"])
    return [item for item in state["eval_set"] if item["query"] in selected]


def cmd_init(args) -> None:
    eval_set = read_json(args.eval_set)
    if not isinstance(eval_set, list) or not eval_set:
        raise ValueError("eval set must be a non-empty JSON array")
    for item in eval_set:
        if not isinstance(item, dict) or not isinstance(item.get("query"), str) or not item["query"].strip():
            raise ValueError("each eval item requires a non-empty string query")
        if not isinstance(item.get("should_trigger"), bool):
            raise ValueError("each eval item requires boolean should_trigger")
    if len({item["query"] for item in eval_set}) != len(eval_set):
        raise ValueError("eval queries must be unique")
    name, description, _ = parse_skill_md(args.skill_path)
    train, test = stratified_split(eval_set, args.holdout, args.seed)
    state = {
        "skill_name": name,
        "skill_path": str(args.skill_path),
        "original_description": description,
        "current_description": description,
        "iteration": 1,
        "max_iterations": args.max_iterations,
        "trigger_threshold": args.trigger_threshold,
        "eval_set": eval_set,
        "train_queries": train,
        "test_queries": test,
        "current_results": {},
        "history": [],
    }
    write_json(args.state, state)
    print(f"initialized {args.state}: train={len(train)} holdout={len(test)}")


def cmd_score(args) -> None:
    state = read_json(args.state)
    eval_subset = subset(state, args.split)
    if not eval_subset:
        raise ValueError(f"{args.split} split is empty")
    result = score_observations(
        eval_subset,
        read_json(args.observations),
        state["skill_name"],
        state["current_description"],
        state["trigger_threshold"],
    )
    state["current_results"][args.split] = result
    write_json(args.state, state)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_prompt(args) -> None:
    state = read_json(args.state)
    train = state["current_results"].get("train")
    if not train:
        raise ValueError("score the train split before building an optimizer prompt")
    _, _, content = parse_skill_md(Path(state["skill_path"]))
    blinded_history = [
        {key: value for key, value in record.items() if not key.startswith("test_")}
        for record in state["history"]
    ]
    prompt = build_improvement_prompt(
        state["skill_name"],
        content,
        state["current_description"],
        train,
        blinded_history,
    )
    args.output.write_text(prompt, encoding="utf-8")
    print(args.output)


def current_record(state: dict) -> dict:
    train = state["current_results"].get("train")
    test = state["current_results"].get("test")
    if not train:
        raise ValueError("train results are missing")
    return {
        "iteration": state["iteration"],
        "description": state["current_description"],
        "train_passed": train["summary"]["passed"],
        "train_total": train["summary"]["total"],
        "train_results": train["results"],
        "test_passed": test["summary"]["passed"] if test else None,
        "test_total": test["summary"]["total"] if test else None,
        "test_results": test["results"] if test else None,
    }


def cmd_apply(args) -> None:
    state = read_json(args.state)
    if state["iteration"] >= state["max_iterations"]:
        raise ValueError("maximum iterations reached")
    if state.get("test_queries") and "test" not in state.get("current_results", {}):
        raise ValueError("score the holdout split before advancing the iteration")
    description = parse_description(args.response.read_text(encoding="utf-8"))
    state["history"].append(current_record(state))
    state["current_description"] = description
    state["iteration"] += 1
    state["current_results"] = {}
    write_json(args.state, state)
    print(description)


def cmd_best(args) -> None:
    state = read_json(args.state)
    records = list(state["history"])
    if state.get("current_results", {}).get("train"):
        records.append(current_record(state))
    if not records:
        print(state["current_description"])
        return

    def score(item: dict) -> tuple[float, float]:
        if item.get("test_total"):
            primary = item["test_passed"] / item["test_total"]
        else:
            primary = item["train_passed"] / item["train_total"]
        secondary = item["train_passed"] / item["train_total"]
        return primary, secondary

    best = max(records, key=score)
    print(best["description"])


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init")
    init.add_argument("--eval-set", required=True, type=Path)
    init.add_argument("--skill-path", required=True, type=Path)
    init.add_argument("--state", required=True, type=Path)
    init.add_argument("--holdout", type=float, default=0.4)
    init.add_argument("--seed", type=int, default=42)
    init.add_argument("--max-iterations", type=int, default=5)
    init.add_argument("--trigger-threshold", type=float, default=0.5)
    init.set_defaults(func=cmd_init)

    score = sub.add_parser("score")
    score.add_argument("--state", required=True, type=Path)
    score.add_argument("--split", required=True, choices=["train", "test"])
    score.add_argument("--observations", required=True, type=Path)
    score.set_defaults(func=cmd_score)

    prompt = sub.add_parser("prompt")
    prompt.add_argument("--state", required=True, type=Path)
    prompt.add_argument("--output", required=True, type=Path)
    prompt.set_defaults(func=cmd_prompt)

    apply = sub.add_parser("apply")
    apply.add_argument("--state", required=True, type=Path)
    apply.add_argument("--response", required=True, type=Path)
    apply.set_defaults(func=cmd_apply)

    best = sub.add_parser("best")
    best.add_argument("--state", required=True, type=Path)
    best.set_defaults(func=cmd_best)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    try:
        if hasattr(args, "holdout") and not 0 <= args.holdout < 1:
            parser.error("--holdout must be in [0, 1)")
        if hasattr(args, "trigger_threshold") and not 0 <= args.trigger_threshold <= 1:
            parser.error("--trigger-threshold must be in [0, 1]")
        args.func(args)
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc


if __name__ == "__main__":
    main()
