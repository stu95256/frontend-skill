from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "frontend-staged-review-workflow" / "scripts" / "review_evidence.py"
SPEC = importlib.util.spec_from_file_location("review_evidence", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
evidence = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(evidence)


@unittest.skipUnless(shutil.which("git"), "git is required")
class ReviewEvidenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.repo = self.base / "reviewed"
        self.repo.mkdir()
        self.git("init", "-q")
        self.store = evidence.EvidenceStore(self.repo, self.base / "evidence")

    def git(self, *args: str) -> subprocess.CompletedProcess[bytes]:
        result = subprocess.run(["git", "-C", str(self.repo), *args], capture_output=True, check=False)
        if result.returncode:
            raise AssertionError(result.stderr.decode("utf-8", errors="replace"))
        return result

    def cli(self, *args: str, data: bytes | None = None) -> subprocess.CompletedProcess[bytes]:
        return subprocess.run([sys.executable, str(SCRIPT), *args, "--repo", str(self.repo), "--store", str(self.store.root)], input=data, capture_output=True, check=False)

    def link_directory(self, alias: Path, target: Path) -> None:
        try:
            alias.symlink_to(target, target_is_directory=True)
        except OSError as exc:
            if sys.platform == "win32":
                import _winapi

                create_junction = getattr(_winapi, "CreateJunction", None)
                if create_junction is not None:
                    create_junction(str(target), str(alias))
                    return
            self.skipTest(f"directory links unavailable: {exc}")

    def test_exact_byte_round_trip_and_receipt_provenance(self) -> None:
        raw = b"first\x00second\r\n\xff\xfe" + "中文\n".encode("utf-8")
        result = self.store.put(raw, "index-manifest", {"source": "raw stdout", "unborn_head": True})
        content = result["objects"]["content"]
        self.assertEqual("sha256:" + hashlib.sha256(raw).hexdigest(), content["id"])
        self.assertEqual(raw, Path(content["path"]).read_bytes())
        self.assertEqual(raw, self.store.get(content["id"]))
        frozen = self.store.get(result["receipt"]["id"])
        receipt = json.loads(frozen)
        self.assertEqual({"source": "raw stdout", "unborn_head": True}, receipt["origin"])
        self.assertEqual(result["objects"], receipt["objects"])
        self.assertTrue(self.store.verify(result["receipt"]["id"])["verified"])
        self.assertEqual({"verified": True, "objects": 2, "receipts": 1}, self.store.verify())

    def test_publication_is_deduplicated_and_never_overwrites_corruption(self) -> None:
        first = self.store.put(b"immutable", "blob", {})
        path = Path(first["objects"]["content"]["path"])
        old_stat = path.stat()
        self.assertEqual(first, self.store.put(b"immutable", "blob", {}))
        self.assertEqual(old_stat.st_mtime_ns, path.stat().st_mtime_ns)
        path.write_bytes(b"corrupted")
        with self.assertRaises(evidence.EvidenceError):
            self.store.put(b"immutable", "blob", {})
        self.assertEqual(b"corrupted", path.read_bytes())
        with self.assertRaises(evidence.EvidenceError):
            self.store.verify(first["receipt"]["id"])
        self.assertEqual([], list(path.parent.glob(".pending-*")))

    def test_receipt_corruption_and_missing_references_are_detected(self) -> None:
        result = self.store.put(b"source", "blob", {})
        receipt_sha = result["receipt"]["sha256"]
        record = self.store.root / "receipts" / (receipt_sha + ".json")
        record.write_bytes(b"{}\n")
        with self.assertRaises(evidence.EvidenceError):
            self.store.verify()
        record.write_bytes(Path(result["receipt"]["path"]).read_bytes())
        Path(result["objects"]["content"]["path"]).unlink()
        with self.assertRaises(FileNotFoundError):
            self.store.verify(result["receipt"]["id"])

    def test_rejects_store_inside_checkout_even_when_repo_argument_is_subdirectory(self) -> None:
        nested = self.repo / "src"
        nested.mkdir()
        for repo, store in ((self.repo, self.repo), (nested, self.repo / ".evidence")):
            with self.subTest(store=store), self.assertRaises(evidence.EvidenceError):
                evidence.EvidenceStore(repo, store)
            self.assertFalse((self.repo / ".evidence").exists())

    def test_rejects_resolved_symlink_store_inside_checkout(self) -> None:
        alias = self.base / "alias"
        self.link_directory(alias, self.repo)
        with self.assertRaises(evidence.EvidenceError):
            evidence.EvidenceStore(self.repo, alias / "evidence")

    def test_linked_worktree_rejects_store_in_external_git_and_common_directories(self) -> None:
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "--allow-empty", "-m", "fixture")
        linked = self.base / "linked"
        self.git("worktree", "add", "--detach", str(linked), "HEAD")
        common = self.repo / ".git"
        private = evidence.resolve_git_directory(linked, "--git-dir")
        self.assertFalse(private.is_relative_to(linked))
        for target in (common, common / "evidence", private, private / "evidence"):
            with self.subTest(target=target), self.assertRaises(evidence.EvidenceError):
                evidence.EvidenceStore(linked, target)
        external = evidence.EvidenceStore(linked, self.base / "safe-evidence")
        self.assertEqual(linked.resolve(), external.repo)

    def test_verify_nonexistent_store_fails_cleanly(self) -> None:
        with self.assertRaises(evidence.EvidenceError):
            self.store.verify()
        result = self.cli("verify")
        self.assertEqual(2, result.returncode)
        self.assertIn(b"does not exist", result.stderr)

    def test_scope_document_capture_flags_are_allowed(self) -> None:
        for args in (
            ["rev-parse", "--verify", "--end-of-options", "HEAD"],
            ["log", "--reverse", "--format=%H%x09%s"],
        ):
            with self.subTest(args=args):
                evidence.validate_git_args(args)
        with self.assertRaises(evidence.EvidenceError):
            evidence.validate_git_args(["log", "--format=%(unapproved)"])

    def test_rejects_object_directory_escape(self) -> None:
        outside = self.base / "elsewhere"
        outside.mkdir()
        self.store.root.mkdir()
        self.link_directory(self.store.root / "objects", outside)
        with self.assertRaises(evidence.EvidenceError):
            self.store.put(b"must stay here", "blob", {})
        self.assertEqual([], list(outside.iterdir()))

    def test_ancestor_store_cannot_publish_into_checkout_named_objects(self) -> None:
        checkout = self.base / "objects"
        checkout.mkdir()
        result = subprocess.run(["git", "-C", str(checkout), "init", "-q"], capture_output=True, check=False)
        self.assertEqual(0, result.returncode, result.stderr)
        store = evidence.EvidenceStore(checkout, self.base)
        with self.assertRaises(evidence.EvidenceError):
            store.put(b"must not publish into checkout", "blob", {})
        self.assertEqual({".git"}, {path.name for path in checkout.iterdir()})

    def test_allowlist_denies_writes_and_external_execution_options(self) -> None:
        for args in (
            ["add", "."], ["hash-object", "-w", "--stdin"], ["update-index", "--refresh"],
            ["status", "--short", "--branch"],
            ["diff", "--output=overwrite"], ["diff", "--ext-diff"], ["diff", "--textconv"],
            ["cat-file", "--filters", "HEAD:file"], ["cat-file", "--batch"],
            ["-c", "alias.attack=!touch compromised", "attack"], ["show", "--show-signature"],
        ):
            with self.subTest(args=args), self.assertRaises(evidence.EvidenceError):
                self.store.capture_git(args)
        self.assertFalse(self.store.root.exists())

    def test_worktree_diffs_are_rejected_without_running_configured_clean_filter(self) -> None:
        marker = self.repo / "filter-ran"
        clean_filter = self.base / "clean_filter.py"
        clean_filter.write_text(
            "import pathlib, sys\n"
            "pathlib.Path(sys.argv[1]).write_bytes(b'filter ran')\n"
            "sys.stdout.buffer.write(sys.stdin.buffer.read())\n",
            encoding="utf-8",
        )
        command = '"' + sys.executable.replace("\\", "/") + '" "' + str(clean_filter).replace("\\", "/") + '" "' + str(marker).replace("\\", "/") + '"'
        self.git("config", "filter.review-test.clean", command)
        (self.repo / ".gitattributes").write_text("*.txt filter=review-test\n", encoding="utf-8")
        (self.repo / "example.txt").write_bytes(b"before\n")
        self.git("add", ".gitattributes", "example.txt")
        self.assertTrue(marker.exists(), "fixture must exercise its configured clean filter")
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", "first")
        base = self.git("rev-parse", "HEAD").stdout.strip().decode("ascii")
        (self.repo / "example.txt").write_bytes(b"after\n")
        self.git("add", "example.txt")
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", "second")
        tip = self.git("rev-parse", "HEAD").stdout.strip().decode("ascii")
        marker.unlink(missing_ok=True)
        (self.repo / "example.txt").write_bytes(b"uncommitted\n")
        for args in (["diff"], ["diff", "HEAD"], ["diff", base], ["diff", "--cached", base, tip], ["diff", "HEAD", "HEAD"]):
            with self.subTest(args=args), self.assertRaises(evidence.EvidenceError):
                self.store.capture_git(args)
            self.assertFalse(marker.exists())
        # Status also runs clean filters for same-length worktree changes.
        (self.repo / "example.txt").write_bytes(b"xxxxxx\n")
        with self.assertRaises(evidence.EvidenceError):
            self.store.capture_git(["status", "--short", "--branch"])
        self.assertFalse(marker.exists())
        for args in (["diff", "--cached"], ["diff", "--staged", base], ["diff", base, tip, "--", "example.txt"]):
            with self.subTest(args=args):
                result = self.store.capture_git(args)
                self.assertEqual(0, json.loads(self.store.get(result["receipt"]["id"]))["origin"]["exit_code"])
                self.assertFalse(marker.exists())
        blob = self.git("rev-parse", "HEAD:example.txt").stdout.strip().decode("ascii")
        with self.assertRaises(evidence.EvidenceError):
            self.store.capture_git(["diff", blob, tip])
        self.assertFalse(marker.exists())

    def test_missing_partial_clone_blob_does_not_lazy_fetch_or_write_git_objects(self) -> None:
        (self.repo / "source.txt").write_bytes(b"object deliberately excluded from the partial clone\n")
        self.git("add", "source.txt")
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", "fixture")
        self.git("config", "uploadpack.allowFilter", "true")
        blob = self.git("rev-parse", "HEAD:source.txt").stdout.strip().decode("ascii")
        partial = self.base / "partial"
        cloned = subprocess.run([
            "git", "clone", "--quiet", "--filter=blob:none", "--no-checkout", "--no-local", str(self.repo), str(partial),
        ], capture_output=True, check=False)
        self.assertEqual(0, cloned.returncode, cloned.stderr)
        pack_dir = partial / ".git" / "objects" / "pack"
        before = {path.name: path.read_bytes() for path in pack_dir.iterdir()}
        store = evidence.EvidenceStore(partial, self.base / "partial-evidence")
        result = store.capture_git(["cat-file", "blob", blob])
        receipt = json.loads(store.get(result["receipt"]["id"]))
        self.assertNotEqual(0, receipt["origin"]["exit_code"])
        self.assertEqual(before, {path.name: path.read_bytes() for path in pack_dir.iterdir()})

    def test_capture_preserves_staged_manifest_and_blob_bytes_without_index_write(self) -> None:
        raw = b"staged\r\n\x00binary\xff"
        source = self.repo / "檔案 with spaces.bin"
        source.write_bytes(raw)
        self.git("add", "--", source.name)
        index = self.repo / ".git" / "index"
        before = index.read_bytes(), index.stat().st_mtime_ns
        expected = self.git("ls-files", "--stage", "-z").stdout
        result = self.store.capture_git(["ls-files", "--stage", "-z"])
        receipt = json.loads(self.store.get(result["receipt"]["id"]))
        self.assertEqual(expected, self.store.get(result["objects"]["stdout"]["id"]))
        self.assertEqual(0, receipt["origin"]["exit_code"])
        self.assertTrue(receipt["origin"]["byte_capture"])
        blob = expected.split(b" ")[1].decode("ascii")
        captured = self.store.capture_git(["cat-file", "blob", blob])
        self.assertEqual(raw, self.store.get(captured["objects"]["stdout"]["id"]))
        diff_args = ["diff", "--cached", "--find-renames", "--full-index", "--binary"]
        expected_patch = self.git("diff", "--no-ext-diff", "--no-textconv", *diff_args[1:]).stdout
        patch = self.store.capture_git(diff_args)
        self.assertEqual(expected_patch, self.store.get(patch["objects"]["stdout"]["id"]))
        source.write_bytes(b"worktree changed")
        self.assertEqual(raw, self.store.get(captured["objects"]["stdout"]["id"]))
        self.assertEqual(before, (index.read_bytes(), index.stat().st_mtime_ns))
        self.assertFalse((self.repo / ".git" / "index.lock").exists())

    def test_failed_git_command_captures_stderr_and_exit_code(self) -> None:
        result = self.store.capture_git(["rev-parse", "--verify", "refs/heads/not-present"])
        receipt = json.loads(self.store.get(result["receipt"]["id"]))
        self.assertNotEqual(0, receipt["origin"]["exit_code"])
        self.assertNotEqual(b"", self.store.get(result["objects"]["stderr"]["id"]))
        self.assertTrue(self.store.verify()["verified"])

    def test_cli_put_stdin_and_get_are_binary_and_bad_origin_fails_cleanly(self) -> None:
        raw = b"\x00\xff\r\n"
        result = self.cli("put", "--kind", "blob", data=raw)
        self.assertEqual(0, result.returncode, result.stderr)
        content_id = json.loads(result.stdout)["objects"]["content"]["id"]
        fetched = self.cli("get", "--object", content_id)
        self.assertEqual(0, fetched.returncode, fetched.stderr)
        self.assertEqual(raw, fetched.stdout)
        invalid = self.cli("put", "--kind", "blob", "--origin", "[]", data=raw)
        self.assertEqual(2, invalid.returncode)
        self.assertNotIn(b"Traceback", invalid.stderr)

    def test_cli_capture_command_separator_and_nonzero_git_exit(self) -> None:
        result = subprocess.run([
            sys.executable, str(SCRIPT), "capture-git", "--repo", str(self.repo), "--store", str(self.store.root),
            "--", "rev-parse", "--verify", "refs/heads/not-present",
        ], capture_output=True, check=False)
        self.assertEqual(0, result.returncode, result.stderr)
        receipt = json.loads(self.store.get(json.loads(result.stdout)["receipt"]["id"]))
        self.assertNotEqual(0, receipt["origin"]["exit_code"])


if __name__ == "__main__":
    unittest.main()
