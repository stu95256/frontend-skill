from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
KILO = ROOT / ".kilo"

REQUIRED_SKILLS = {
    "react-router",
    "ag-dev",
    "ag-update",
    "shadcn",
    "vitest",
    "playwright-cli",
    "openapi-typescript",
}

OBSOLETE_SKILLS = {
    "react-router-declarative-mode",
    "react-router-data-mode",
    "react-router-framework-mode",
    "ag-grid",
    "tailwind-v4-shadcn",
    "vitest-testing",
    "playwright-mcp-usage",
    "openapi-to-typescript",
    "design-system-starter",
    "e2e-testing-patterns",
    "audit-code-reviewer",
    "code-review-excellence",
}

OBSOLETE_REFERENCE_NAMES = OBSOLETE_SKILLS - {"ag-grid"}

ALLOWED_FRONTMATTER = {
    "name",
    "description",
    "license",
    "allowed-tools",
    "compatibility",
    "metadata",
}

WORKFLOW_ROOTS = (
    SKILLS / "frontend-staged-review-workflow",
    SKILLS / "frontend-branch-review-workflow",
    SKILLS / "frontend-debug-workflow",
    KILO / "skills" / "frontend-staged-review-workflow",
    KILO / "skills" / "frontend-branch-review-workflow",
    KILO / "skills" / "frontend-debug-workflow",
    KILO / "skills" / "frontend-heavy-staged-review-workflow",
    KILO / "skills" / "frontend-task-preflight",
    KILO / "workflows",
)

MIRRORS = (
    (
        SKILLS / "frontend-staged-review-workflow" / "SKILL.md",
        KILO / "skills" / "frontend-staged-review-workflow" / "SKILL.md",
    ),
    (
        SKILLS / "frontend-staged-review-workflow" / "SKILL.md",
        KILO / "workflows" / "FRONTEND_STAGED_REVIEW_WORKFLOW.md",
    ),
    (
        SKILLS / "frontend-branch-review-workflow" / "SKILL.md",
        KILO / "skills" / "frontend-branch-review-workflow" / "SKILL.md",
    ),
    (
        SKILLS / "frontend-branch-review-workflow" / "SKILL.md",
        KILO / "workflows" / "FRONTEND_BRANCH_REVIEW_WORKFLOW.md",
    ),
    (
        SKILLS / "frontend-debug-workflow" / "references" / "FRONTEND_DEBUG_WORKFLOW.md",
        KILO / "workflows" / "FRONTEND_DEBUG_WORKFLOW.md",
    ),
    (
        SKILLS / "frontend-branch-review-workflow" / "SKILL.md",
        ROOT / "FRONTEND_BRANCH_REVIEW_WORKFLOW.md",
    ),
    (
        SKILLS / "frontend-debug-workflow" / "references" / "FRONTEND_DEBUG_WORKFLOW.md",
        ROOT / "FRONTEND_DEBUG_WORKFLOW.md",
    ),
    (
        KILO / "skills" / "frontend-heavy-staged-review-workflow" / "references" / "FRONTEND_HEAVY_STAGED_REVIEW_WORKFLOW.md",
        ROOT / "FRONTEND_HEAVY_STAGED_REVIEW_WORKFLOW.md",
    ),
    (
        KILO / "skills" / "frontend-task-preflight" / "references" / "FRONTEND_TASK_PREFLIGHT_WORKFLOW.md",
        ROOT / "FRONTEND_TASK_PREFLIGHT_WORKFLOW.md",
    ),
    (SKILLS / "SKILLS_MANIFEST.md", KILO / "manifests" / "SKILLS_MANIFEST.md"),
    (SKILLS / "VALIDATION_REPORT.md", KILO / "manifests" / "VALIDATION_REPORT.md"),
    (ROOT / "SKILL_SOURCES.md", KILO / "manifests" / "SKILL_SOURCES.md"),
)


def parse_frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8-sig")
    if not text.startswith("---\n"):
        raise ValueError("frontmatter must start at byte 0")
    try:
        _, raw, body = text.split("---", 2)
    except ValueError as exc:
        raise ValueError("missing closing frontmatter delimiter") from exc
    data = yaml.safe_load(raw)
    if not isinstance(data, dict):
        raise ValueError("frontmatter must be a mapping")
    if not body.strip():
        raise ValueError("skill body is empty")
    return data


def iter_skill_dirs(root: Path) -> list[Path]:
    if not root.is_dir():
        return []
    return sorted(path for path in root.iterdir() if (path / "SKILL.md").is_file())


def main() -> int:
    errors: list[str] = []
    skill_dirs = iter_skill_dirs(SKILLS)
    names = {path.name for path in skill_dirs}

    missing = sorted(REQUIRED_SKILLS - names)
    if missing:
        errors.append(f"missing required replacement skills: {missing}")

    remaining = sorted(OBSOLETE_SKILLS & names)
    if remaining:
        errors.append(f"obsolete skill directories remain: {remaining}")

    manifest_path = SKILLS / "SKILLS_MANIFEST.md"
    manifest_rows: dict[str, tuple[str, str, str]] = {}
    for line in manifest_path.read_text(encoding="utf-8-sig").splitlines():
        if not line.startswith("| ") or "`" not in line:
            continue
        columns = [column.strip() for column in line.strip("|").split("|")]
        if len(columns) < 8 or columns[1] == "Skill":
            continue
        name = columns[1].strip("`")
        manifest_rows[name] = (columns[3], columns[4].strip("`"), columns[6])

    if set(manifest_rows) != names:
        errors.append(
            "manifest skill set differs from catalog: "
            f"missing={sorted(names - set(manifest_rows))}, "
            f"extra={sorted(set(manifest_rows) - names)}"
        )
    for name, (source, revision, license_name) in manifest_rows.items():
        if license_name == "See upstream":
            errors.append(f"manifest {name}: license must be recorded explicitly")
        if "github.com/" in source and not re.search(r"(?<![0-9a-f])[0-9a-f]{40}(?![0-9a-f])", revision):
            errors.append(f"manifest {name}: GitHub source requires a full 40-character commit SHA")

    for directory in skill_dirs:
        path = directory / "SKILL.md"
        try:
            data = parse_frontmatter(path)
        except Exception as exc:  # report every catalog problem in one run
            errors.append(f"{path.relative_to(ROOT)}: {exc}")
            continue

        if data.get("name") != directory.name:
            errors.append(
                f"{path.relative_to(ROOT)}: name {data.get('name')!r} does not match directory"
            )
        description = data.get("description")
        if not isinstance(description, str) or not description.strip():
            errors.append(f"{path.relative_to(ROOT)}: missing description")
        unexpected = sorted(set(data) - ALLOWED_FRONTMATTER)
        if unexpected:
            errors.append(f"{path.relative_to(ROOT)}: unsupported frontmatter keys {unexpected}")

        metadata = data.get("metadata")
        if isinstance(metadata, dict):
            hermes = metadata.get("hermes")
            if isinstance(hermes, dict):
                related = hermes.get("related_skills", [])
                if isinstance(related, list):
                    unresolved = sorted(
                        value for value in related if isinstance(value, str) and value not in names
                    )
                    if unresolved:
                        errors.append(
                            f"{path.relative_to(ROOT)}: unresolved related_skills {unresolved}"
                        )

    obsolete_pattern = re.compile(
        r"(?<![\w-])(?:"
        + "|".join(re.escape(name) for name in sorted(OBSOLETE_REFERENCE_NAMES))
        + r")(?![\w-])|`ag-grid`|skills/ag-grid(?:/|\b)|(?:^|[ ,\[])ag-grid-[AB](?:$|[ ,\]])",
        re.MULTILINE,
    )
    for root in WORKFLOW_ROOTS:
        if not root.exists():
            continue
        paths = [root] if root.is_file() else list(root.rglob("*.md"))
        for path in paths:
            matches = sorted(set(obsolete_pattern.findall(path.read_text(encoding="utf-8-sig"))))
            if matches:
                errors.append(f"{path.relative_to(ROOT)}: obsolete workflow references {matches}")

    for source, mirror in MIRRORS:
        if not source.is_file() or not mirror.is_file():
            errors.append(
                f"workflow mirror missing: {source.relative_to(ROOT)} or {mirror.relative_to(ROOT)}"
            )
        elif source.read_bytes() != mirror.read_bytes():
            errors.append(
                f"workflow mirror drift: {source.relative_to(ROOT)} != {mirror.relative_to(ROOT)}"
            )

    smoke_requirements = {
        SKILLS / "frontend-staged-review-workflow" / "SKILL.md": (
            "git diff --cached",
            "at least two",
            "`react-router`",
            "`ag-dev`",
            "`playwright-cli`",
            "general baseline reviewer",
        ),
        SKILLS / "frontend-branch-review-workflow" / "SKILL.md": (
            "merge-base",
            "pinned",
            "at least two",
            "`react-router`",
        ),
        SKILLS / "frontend-debug-workflow" / "SKILL.md": (
            "root cause",
            "`react-doctor`",
            "`ag-update`",
            "`playwright-cli`",
            "fall back to `browser-testing-with-devtools`",
        ),
        SKILLS / "frontend-staged-commit-message" / "SKILL.md": (
            "git diff --cached",
            "Do not run `git commit`",
            "never stages files",
        ),
        KILO / "skills" / "frontend-task-preflight" / "references" / "FRONTEND_TASK_PREFLIGHT_WORKFLOW.md": (
            "`openapi-typescript`",
            "`vitest`",
            "`skill-scanner`",
            "`shadcn`",
            "dynamic, interactive, authenticated, or blocked pages",
            "documented DevTools fallback",
        ),
        KILO / "skills" / "frontend-heavy-staged-review-workflow" / "SKILL.md": (
            "minimum of two",
            "`accessibility`",
            "`playwright-cli`",
        ),
        KILO / "skills" / "frontend-heavy-staged-review-workflow" / "references" / "FRONTEND_HEAVY_STAGED_REVIEW_WORKFLOW.md": (
            "minimum of two",
            "`accessibility`",
            "`playwright-cli`",
        ),
    }
    for path, needles in smoke_requirements.items():
        text = path.read_text(encoding="utf-8-sig") if path.is_file() else ""
        missing_needles = [needle for needle in needles if needle not in text]
        if missing_needles:
            errors.append(
                f"{path.relative_to(ROOT)}: workflow smoke requirements missing {missing_needles}"
            )

    for catalog_root in (SKILLS, KILO / "skills"):
        for skill_dir in iter_skill_dirs(catalog_root):
            skill_md = skill_dir / "SKILL.md"
            text = skill_md.read_text(encoding="utf-8-sig")
            relative_targets = re.findall(
                r"\[[^\]]*\]\((?!https?://|mailto:|#)([^)\s]+)", text
            )
            relative_targets += re.findall(
                r"`((?:references|scripts|templates|assets)/[^`\n]+)`", text
            )
            for raw_target in relative_targets:
                if re.search(r":\d+(?::\d+)?$", raw_target):
                    continue  # Example source location, not a linked asset.
                target = raw_target.split()[0].split("#", 1)[0]
                if target.startswith(".playwright-cli/"):
                    continue  # Runtime-generated Playwright CLI artifact.
                if any(character in target for character in "<>*?[]{}$"):
                    continue  # Documented placeholder, not a vendored file.
                if not (skill_dir / target).exists():
                    errors.append(
                        f"{skill_md.relative_to(ROOT)}: missing relative reference {target}"
                    )

    support_files = (
        SKILLS / "webapp-testing" / "scripts" / "with_server.py",
        SKILLS / "web-artifacts-builder" / "scripts" / "init-artifact.sh",
        SKILLS / "web-artifacts-builder" / "scripts" / "bundle-artifact.sh",
    )
    for path in support_files:
        if not path.is_file():
            errors.append(f"missing supporting file: {path.relative_to(ROOT)}")

    if errors:
        print(f"catalog validation failed with {len(errors)} issue(s):")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        f"catalog validation passed: {len(skill_dirs)} skills, "
        f"{len(REQUIRED_SKILLS)} replacements present, no obsolete workflow references"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
