#!/usr/bin/env python3
"""Write-once, content-addressed raw review evidence outside a Git checkout.

This helper preserves bytes and verifies integrity; it does not establish that a
set of captures forms a consistent Git snapshot. The coordinator owns that gate.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import uuid


SCHEMA = "frontend-review-evidence/v1"
ID_RE = re.compile(r"sha256:([0-9a-f]{64})\Z")
GIT_OBJECT_RE = re.compile(r"(?:[0-9a-fA-F]{40}|[0-9a-fA-F]{64})\Z")
FLAGS = {
    "rev-parse": {"--verify", "--quiet", "--end-of-options", "--show-toplevel", "--git-dir", "--git-common-dir", "--is-inside-work-tree", "--show-object-format"},
    "ls-files": {"--stage", "-s", "-z", "--cached", "--full-name", "--error-unmatch"},
    "diff": {"--cached", "--staged", "--find-renames", "--full-index", "--raw", "--name-status", "--numstat", "--stat", "--check", "-z", "--binary", "--no-ext-diff", "--no-textconv", "--no-color", "--no-renames"},
    "show": {"--no-patch", "--format=", "--format=raw", "--format=fuller", "--format=oneline", "--name-status", "--stat", "--full-index", "--binary", "--no-ext-diff", "--no-textconv", "--no-color"},
    "log": {"--oneline", "--reverse", "--no-patch", "--format=raw", "--format=fuller", "--format=oneline", "--format=%H%x09%s", "--name-status", "--stat", "--no-ext-diff", "--no-textconv", "--no-color"},
    "merge-base": {"--all", "--is-ancestor", "--octopus", "--independent"},
    "ls-tree": {"-r", "-t", "-z", "-l", "--long", "--name-only", "--name-status", "--full-name", "--full-tree"},
}


class EvidenceError(ValueError):
    """An evidence or capture boundary could not be verified."""


def diff_object_ids(args: list[str]) -> list[str]:
    """Reject comparisons that can read/filter files from the working tree."""
    tail = args[1:args.index("--")] if "--" in args else args[1:]
    objects = [arg for arg in tail if not arg.startswith("-")]
    staged = "--cached" in tail or "--staged" in tail
    if (staged and len(objects) > 1) or (not staged and len(objects) != 2):
        raise EvidenceError("diff requires --cached/--staged with at most one frozen base, or two full commit/tree object IDs")
    if any(GIT_OBJECT_RE.fullmatch(object_id) is None for object_id in objects):
        raise EvidenceError("diff revisions must be full 40/64-digit hexadecimal commit/tree object IDs")
    return objects


def validate_git_args(args: list[str]) -> None:
    if not args or any("\0" in arg for arg in args):
        raise EvidenceError("capture-git requires a read-only Git command")
    command, *tail = args
    if command == "cat-file":
        if len(tail) != 2 or tail[0] not in {"blob", "commit", "tree", "tag", "-p", "-t", "-s", "-e"} or tail[1].startswith("-"):
            raise EvidenceError("cat-file requires an allowed mode and one object")
        return
    if command not in FLAGS:
        raise EvidenceError(f"Git command is not allowlisted: {command}")
    paths = False
    for arg in tail:
        if paths:
            continue
        if arg == "--":
            if command in {"rev-parse", "merge-base"}:
                raise EvidenceError(f"path separator is unsupported for {command}")
            paths = True
        elif arg.startswith("-") and arg not in FLAGS[command]:
            if command == "diff" and re.fullmatch(r"--find-renames=\d{1,3}%", arg):
                continue
            if command == "log" and re.fullmatch(r"(?:--max-count=|-n)[1-9]\d{0,3}", arg):
                continue
            raise EvidenceError(f"Git option is not allowlisted: {arg}")
    if command == "diff":
        diff_object_ids(args)


def git_argv(repo: Path, args: list[str]) -> list[str]:
    validate_git_args(args)
    prefix = ["git", "--no-pager", "--no-optional-locks", "-c", "core.fsmonitor=false", "-c", "log.showSignature=false", "-c", "submodule.recurse=false", "-c", "status.submoduleSummary=false", "-C", str(repo)]
    if args[0] in {"diff", "show", "log"}:
        return prefix + [args[0], "--no-ext-diff", "--no-textconv", *args[1:]]
    return prefix + args


def run_git(repo: Path, args: list[str]) -> tuple[list[str], subprocess.CompletedProcess[bytes]]:
    argv = git_argv(repo, args)
    if args[0] == "diff":
        for object_id in diff_object_ids(args):
            _, object_type = run_git(repo, ["cat-file", "-t", object_id])
            if object_type.returncode or object_type.stdout.rstrip(b"\r\n") not in {b"commit", b"tree"}:
                raise EvidenceError("diff revisions must identify existing commit/tree objects")
    # Inherited Git overrides could silently select a different index or repo.
    env = {key: value for key, value in os.environ.items() if not key.upper().startswith("GIT_")}
    env.update(GIT_OPTIONAL_LOCKS="0", GIT_TERMINAL_PROMPT="0", GIT_NO_REPLACE_OBJECTS="1", GIT_NO_LAZY_FETCH="1")
    return argv, subprocess.run(argv, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, check=False)


def resolve_repo(repo: Path) -> Path:
    candidate = repo.resolve(strict=True)
    _, result = run_git(candidate, ["rev-parse", "--show-toplevel"])
    if result.returncode:
        raise EvidenceError("--repo must name a Git working tree")
    try:
        return Path(result.stdout.rstrip(b"\r\n").decode("utf-8")).resolve(strict=True)
    except (UnicodeError, OSError) as exc:
        raise EvidenceError("cannot resolve Git checkout root") from exc


def resolve_git_directory(repo: Path, option: str) -> Path:
    _, result = run_git(repo, ["rev-parse", option])
    if result.returncode:
        raise EvidenceError(f"cannot resolve {option}")
    directory = Path(result.stdout.rstrip(b"\r\n").decode("utf-8"))
    return (directory if directory.is_absolute() else repo / directory).resolve(strict=True)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")


class EvidenceStore:
    def __init__(self, repo: Path, store: Path):
        self.repo = resolve_repo(repo)
        self.root = store.resolve()
        self.boundaries = [self.repo, resolve_git_directory(self.repo, "--git-dir"), resolve_git_directory(self.repo, "--git-common-dir")]
        if any(self.root.is_relative_to(directory) for directory in self.boundaries):
            raise EvidenceError("evidence store must resolve outside the reviewed checkout and Git directories")

    def check_path(self, path: Path) -> None:
        resolved = path.resolve()
        if not resolved.is_relative_to(self.root):
            raise EvidenceError("evidence path escapes the resolved store")
        if any(resolved.is_relative_to(directory) for directory in self.boundaries):
            raise EvidenceError("evidence path overlaps the reviewed checkout or Git directories")

    def path(self, category: str, sha: str) -> Path:
        path = self.root / category / (sha + (".json" if category == "receipts" else ""))
        self.check_path(path)
        return path

    def descriptor(self, data: bytes, category: str = "objects") -> dict[str, object]:
        sha = digest(data)
        return {"id": "sha256:" + sha, "sha256": sha, "size": len(data), "path": str(self.path(category, sha))}

    def publish(self, data: bytes, category: str = "objects") -> dict[str, object]:
        result = self.descriptor(data, category)
        path = Path(str(result["path"]))
        self.check_path(path.parent)
        path.parent.mkdir(parents=True, exist_ok=True)
        pending = path.parent / (".pending-" + uuid.uuid4().hex)
        try:
            with pending.open("xb") as stream:
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
            try:
                # Hard-link publication is atomic and refuses an existing name.
                os.link(pending, path)
            except FileExistsError:
                pass
            self.verify_descriptor(result)
        finally:
            pending.unlink(missing_ok=True)
        if os.name != "nt":
            # Windows does not expose directory fsync through os.open.
            directory = os.open(path.parent, os.O_RDONLY)
            try:
                os.fsync(directory)
            finally:
                os.close(directory)
        return result

    def verify_descriptor(self, descriptor: dict[str, object]) -> bytes:
        object_id = descriptor.get("id")
        match = ID_RE.fullmatch(object_id) if isinstance(object_id, str) else None
        if match is None or descriptor.get("sha256") != match[1]:
            raise EvidenceError("invalid evidence content identifier")
        declared = Path(str(descriptor.get("path", "")))
        allowed = {self.path("objects", match[1]), self.path("receipts", match[1])}
        if not declared.is_absolute() or declared not in allowed or not declared.resolve().is_relative_to(self.root):
            raise EvidenceError("invalid evidence path")
        data = declared.read_bytes()
        if digest(data) != match[1] or len(data) != descriptor.get("size"):
            raise EvidenceError(f"evidence hash/size mismatch: {declared}")
        return data

    def receipt(self, kind: str, objects: dict[str, dict[str, object]], origin: dict[str, object]) -> dict[str, object]:
        if not kind.strip():
            raise EvidenceError("evidence kind must not be empty")
        for descriptor in objects.values():
            self.verify_descriptor(descriptor)
        payload = {"schema": SCHEMA, "repo": str(self.repo), "kind": kind, "origin": origin, "objects": objects}
        raw = canonical_json(payload)
        frozen = self.publish(raw)
        self.publish(raw, "receipts")
        return {"receipt": frozen, "kind": kind, "objects": objects}

    def put(self, data: bytes, kind: str, origin: dict[str, object]) -> dict[str, object]:
        return self.receipt(kind, {"content": self.publish(data)}, origin)

    def capture_git(self, args: list[str]) -> dict[str, object]:
        argv, result = run_git(self.repo, args)
        origin = {"argv": argv, "git_args": args, "cwd": str(self.repo), "exit_code": result.returncode, "byte_capture": True, "lazy_fetch_disabled": True}
        return self.receipt("git-capture", {"stdout": self.publish(result.stdout), "stderr": self.publish(result.stderr)}, origin)

    def get(self, object_id: str) -> bytes:
        match = ID_RE.fullmatch(object_id)
        if match is None:
            raise EvidenceError("expected sha256:<64 lowercase hex digits>")
        path = self.path("objects", match[1])
        data = path.read_bytes()
        return self.verify_descriptor(self.descriptor(data)) if digest(data) == match[1] else self._corrupt(path)

    @staticmethod
    def _corrupt(path: Path) -> bytes:
        raise EvidenceError(f"evidence hash mismatch: {path}")

    def verify(self, object_id: str | None = None) -> dict[str, object]:
        if not self.root.is_dir():
            raise EvidenceError("evidence store does not exist or is not a directory")
        if object_id is not None:
            raw = self.get(object_id)
            try:
                payload = json.loads(raw)
            except (ValueError, UnicodeError):
                payload = None
            if isinstance(payload, dict) and payload.get("schema") == SCHEMA:
                self.verify_receipt(payload)
            return {"verified": True, "object": object_id, "size": len(raw)}
        count = 0
        for path in sorted((self.root / "objects").glob("*")):
            if path.name.startswith(".pending-"):
                continue
            self.get("sha256:" + path.name)
            count += 1
        receipt_count = 0
        for path in sorted((self.root / "receipts").glob("*.json")):
            raw = path.read_bytes()
            self.verify_descriptor({"id": "sha256:" + path.stem, "sha256": path.stem, "size": len(raw), "path": str(path)})
            self.get("sha256:" + path.stem)
            self.verify_receipt(json.loads(raw))
            receipt_count += 1
        return {"verified": True, "objects": count, "receipts": receipt_count}

    def verify_receipt(self, payload: object) -> None:
        if not isinstance(payload, dict) or payload.get("schema") != SCHEMA or not isinstance(payload.get("objects"), dict):
            raise EvidenceError("invalid evidence receipt")
        for descriptor in payload["objects"].values():
            if not isinstance(descriptor, dict):
                raise EvidenceError("invalid evidence reference")
            self.verify_descriptor(descriptor)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("put", "capture-git", "verify", "get"):
        command = commands.add_parser(name)
        command.add_argument("--repo", type=Path, required=True)
        command.add_argument("--store", type=Path, required=True)
        if name == "put":
            command.add_argument("--kind", required=True)
            command.add_argument("--source", type=Path)
            command.add_argument("--origin", default="{}", help="JSON object describing provenance")
        if name in {"get", "verify"}:
            command.add_argument("--object", required=name == "get")
        if name == "capture-git":
            command.add_argument("git_args", nargs=argparse.REMAINDER)
    options = parser.parse_args(argv)
    try:
        store = EvidenceStore(options.repo, options.store)
        if options.command == "put":
            origin = json.loads(options.origin)
            if not isinstance(origin, dict):
                raise EvidenceError("--origin must be a JSON object")
            data = options.source.read_bytes() if options.source else sys.stdin.buffer.read()
            result = store.put(data, options.kind, origin)
        elif options.command == "capture-git":
            args = options.git_args[1:] if options.git_args[:1] == ["--"] else options.git_args
            result = store.capture_git(args)
        elif options.command == "get":
            sys.stdout.buffer.write(store.get(options.object))
            return 0
        else:
            result = store.verify(options.object)
        sys.stdout.buffer.write(canonical_json(result))
        return 0
    except (EvidenceError, OSError, ValueError) as exc:
        print(f"review-evidence: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
