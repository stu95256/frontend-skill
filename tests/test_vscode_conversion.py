from __future__ import annotations

import json
import importlib.util
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
    result = subprocess.run(args, cwd=cwd, text=True, encoding="utf-8", capture_output=True)
    if result.returncode:
        raise AssertionError(f"{args[0]} exited {result.returncode}:\n{result.stderr}")
    return result


class VSCodeConversionTests(unittest.TestCase):
    def test_validator_rejects_removed_skill_references(self) -> None:
        spec = importlib.util.spec_from_file_location("catalog_validator", ROOT / "scripts" / "validate_skill_catalog.py")
        assert spec is not None and spec.loader is not None
        validator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(validator)
        with tempfile.TemporaryDirectory() as temp:
            validator.ROOT = Path(temp)
            skill = Path(temp) / "skills" / "example"
            skill.mkdir(parents=True)
            for removed in ("playwright-cli", "accessibility", "accessibility-compliance", "fixing-motion-performance", "animation-performance"):
                with self.subTest(removed=removed):
                    (skill / "SKILL.md").write_text(f"Route this task to `{removed}`.\n", encoding="utf-8")
                    errors: list[str] = []
                    validator.validate_runtime_terms(Path(temp) / "skills", errors)
                    self.assertEqual(1, len(errors))

    def test_catalog_validator(self) -> None:
        result = run(sys.executable, "scripts/validate_skill_catalog.py")
        self.assertIn("61 skills, 14 custom agents, 2 instruction files", result.stdout)

    @unittest.skipUnless(shutil.which("bash"), "bash is required")
    def test_installer_copies_exact_runtime_counts(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / ".copilot"
            retired = ("webapp-testing", "playwright-cli", "playwright-best-practices", "browser-testing-with-devtools", "accessibility", "accessibility-compliance", "fixing-motion-performance", "animation-performance")
            for name in retired:
                old = target / "skills" / name
                old.mkdir(parents=True)
                (old / "SKILL.md").write_text("old catalog entry\n", encoding="utf-8")
            custom = target / "skills" / "personal-customization"
            custom.mkdir()
            (custom / "keep.txt").write_text("keep\n", encoding="utf-8")
            run("bash", (ROOT / "scripts" / "install-vscode-chat.sh").as_posix(), "--target", target.as_posix())
            skills = sum((path / "SKILL.md").is_file() for path in (target / "skills").iterdir() if path.is_dir())
            agents = len(list((target / "agents").glob("*.agent.md")))
            instructions = len(list((target / "instructions").glob("*.instructions.md")))
            self.assertEqual((61, 14, 2), (skills, agents, instructions))
            self.assertTrue((custom / "keep.txt").is_file())
            for name in retired:
                self.assertFalse((target / "skills" / name).exists())

    def test_staged_commit_message_returns_ordered_candidates(self) -> None:
        text = (ROOT / "skills" / "frontend-staged-commit-message" / "SKILL.md").read_text(encoding="utf-8")
        for required in (
            "Output at least five English candidates by default",
            "Before the candidates, provide a short explanation in the user's language",
            "Why these candidates",
            "Commit candidates",
            "Keep every candidate to one line and order them from simple to detailed",
            "1. **Simple**",
            "5. **Most detailed**",
        ):
            self.assertIn(required, text)
        self.assertNotIn("Output exactly one English line", text)

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

            run("bash", (SDD / "sdd-workspace").as_posix(), "plan.md", cwd=repo)
            run("bash", (SDD / "task-brief").as_posix(), "plan.md", "1", cwd=repo)
            run("bash", (SDD / "review-package").as_posix(), "plan.md", base, "WORKTREE", cwd=repo)

            workspace = repo / ".copilot-workflows" / "sdd" / "plan"
            self.assertTrue((workspace / "task-1-brief.md").is_file())
            packages = list(workspace.glob("review-*.diff"))
            self.assertEqual(1, len(packages))
            review = packages[0].read_text(encoding="utf-8")
            self.assertIn("+after", review)
            self.assertIn("+new content", review)

            empty_range = subprocess.run(
                ["bash", (SDD / "review-package").as_posix(), "plan.md", base, base],
                cwd=repo, capture_output=True,
            )
            self.assertEqual(3, empty_range.returncode, empty_range.stderr.decode("utf-8"))
            unrelated = run("git", "commit-tree", "HEAD^{tree}", "-m", "unrelated root", cwd=repo).stdout.strip()
            unrelated_range = subprocess.run(
                ["bash", (SDD / "review-package").as_posix(), "plan.md", base, unrelated],
                cwd=repo, capture_output=True,
            )
            self.assertEqual(3, unrelated_range.returncode, unrelated_range.stderr.decode("utf-8"))

    @unittest.skipUnless(shutil.which("bash") and shutil.which("git"), "bash and git are required")
    def test_sdd_workspace_disambiguates_plan_names(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp)
            run("git", "init", "-q", cwd=repo)
            base = repo / ".copilot-workflows" / "sdd"
            base.mkdir(parents=True)
            ignore = base / ".gitignore"
            ignore.write_text("# keep local policy\n*.tmp\n", encoding="utf-8")
            for parent in ("alpha", "beta"):
                (repo / parent).mkdir()
                (repo / parent / "plan.md").write_text("# Plan\n", encoding="utf-8")
            helper = (SDD / "sdd-workspace").as_posix()
            first = run("bash", helper, "alpha/plan.md", cwd=repo).stdout.strip()
            second = run("bash", helper, "beta/plan.md", cwd=repo).stdout.strip()
            self.assertNotEqual(first, second)
            self.assertEqual(first, run("bash", helper, "alpha/../alpha/plan.md", cwd=repo).stdout.strip())
            self.assertEqual("# keep local policy\n*.tmp\n", ignore.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
