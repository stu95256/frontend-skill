from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_CREATOR = ROOT / "skills" / "skill-creator" / "scripts"
SDD = ROOT / "skills" / "subagent-driven-development" / "scripts"


def run(*args: str, cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=True)


class VSCodeConversionTests(unittest.TestCase):
    def test_catalog_validator(self) -> None:
        result = run(sys.executable, "scripts/validate_skill_catalog.py")
        self.assertIn("67 skills, 17 custom agents, 2 instruction files", result.stdout)

    @unittest.skipUnless(shutil.which("bash"), "bash is required")
    def test_installer_copies_exact_runtime_counts(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / ".copilot"
            run("bash", str(ROOT / "scripts" / "install-vscode-chat.sh"), "--target", target.as_posix())
            skills = sum((path / "SKILL.md").is_file() for path in (target / "skills").iterdir() if path.is_dir())
            agents = len(list((target / "agents").glob("*.agent.md")))
            instructions = len(list((target / "instructions").glob("*.instructions.md")))
            self.assertEqual((67, 17, 2), (skills, agents, instructions))

    def test_skill_creator_resumable_loop_and_holdout_blinding(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            temp_path = Path(temp)
            eval_path = temp_path / "eval.json"
            state_path = temp_path / "state.json"
            eval_path.write_text(
                json.dumps(
                    [
                        {"query": "review staged frontend diff", "should_trigger": True},
                        {"query": "audit branch UI changes", "should_trigger": True},
                        {"query": "write a poem", "should_trigger": False},
                        {"query": "explain DNS", "should_trigger": False},
                    ]
                ),
                encoding="utf-8",
            )
            run(
                sys.executable,
                str(SKILL_CREATOR / "run_loop.py"),
                "init",
                "--eval-set",
                str(eval_path),
                "--skill-path",
                str(ROOT / "skills" / "frontend-staged-review-workflow"),
                "--state",
                str(state_path),
                "--holdout",
                "0.5",
            )
            state = json.loads(state_path.read_text(encoding="utf-8"))
            expected = {item["query"]: item["should_trigger"] for item in state["eval_set"]}

            for split in ("train", "test"):
                observations = [
                    {
                        "query": query,
                        "selected_skill": state["skill_name"] if expected[query] else None,
                        "reason": "fixture",
                    }
                    for query in state[f"{split}_queries"]
                ]
                observations_path = temp_path / f"{split}.json"
                observations_path.write_text(json.dumps(observations), encoding="utf-8")
                run(
                    sys.executable,
                    str(SKILL_CREATOR / "run_loop.py"),
                    "score",
                    "--state",
                    str(state_path),
                    "--split",
                    split,
                    "--observations",
                    str(observations_path),
                )

            prompt_path = temp_path / "optimizer.md"
            run(
                sys.executable,
                str(SKILL_CREATOR / "run_loop.py"),
                "prompt",
                "--state",
                str(state_path),
                "--output",
                str(prompt_path),
            )
            prompt = prompt_path.read_text(encoding="utf-8")
            for query in state["test_queries"]:
                self.assertNotIn(query, prompt)

            report_path = temp_path / "report.html"
            run(
                sys.executable,
                str(SKILL_CREATOR / "generate_report.py"),
                str(state_path),
                "--output",
                str(report_path),
            )
            self.assertIn("Best Score", report_path.read_text(encoding="utf-8"))

    @unittest.skipUnless(shutil.which("bash") and shutil.which("git"), "bash and git are required")
    def test_sdd_helpers_capture_tracked_and_untracked_worktree_changes(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp)
            run("git", "init", "-q", cwd=repo)
            run("git", "config", "user.email", "test@example.invalid", cwd=repo)
            run("git", "config", "user.name", "Test", cwd=repo)
            (repo / "plan.md").write_text("# Plan\n\n## Task 1: change files\n\nEdit app.txt and add new.txt.\n", encoding="utf-8")
            (repo / "app.txt").write_text("before\n", encoding="utf-8")
            run("git", "add", "plan.md", "app.txt", cwd=repo)
            run("git", "commit", "-qm", "initial", cwd=repo)
            base = run("git", "rev-parse", "HEAD", cwd=repo).stdout.strip()
            (repo / "app.txt").write_text("after\n", encoding="utf-8")
            (repo / "new.txt").write_text("new content\n", encoding="utf-8")

            run("bash", str(SDD / "sdd-workspace"), "plan.md", cwd=repo)
            run("bash", str(SDD / "task-brief"), "plan.md", "1", cwd=repo)
            run("bash", str(SDD / "review-package"), "plan.md", base, "WORKTREE", cwd=repo)

            workspace = repo / ".copilot-workflows" / "sdd" / "plan"
            self.assertTrue((workspace / "task-1-brief.md").is_file())
            packages = list(workspace.glob("review-*.diff"))
            self.assertEqual(1, len(packages))
            review = packages[0].read_text(encoding="utf-8")
            self.assertIn("+after", review)
            self.assertIn("+new content", review)


if __name__ == "__main__":
    unittest.main()
