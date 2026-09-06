from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
AGENTS = ROOT / "agents"
INSTRUCTIONS = ROOT / "instructions"
EXPECTED_SKILL_COUNT = 67
EXPECTED_AGENT_COUNT = 17
EXPECTED_INSTRUCTION_COUNT = 2

REQUIRED_WORKFLOW_SKILLS = {
    "frontend-task-preflight",
    "frontend-debug-workflow",
    "frontend-staged-review-workflow",
    "frontend-heavy-staged-review-workflow",
    "frontend-branch-review-workflow",
    "frontend-staged-commit-message",
}

REQUIRED_COORDINATORS = {
    "Frontend Task Preflight",
    "Frontend Implementation",
    "Frontend Debug",
    "Frontend Staged Review",
    "Frontend Heavy Staged Review",
    "Frontend Branch Review",
    "Frontend Staged Commit Message",
    "VS Code Skill Creator",
}

REQUIRED_WORKERS = {
    "Frontend Researcher",
    "Frontend Plan Reviewer",
    "Frontend Implementer",
    "Frontend Verifier",
    "Frontend Reviewer",
    "Frontend Security Reviewer",
    "Frontend Review Validator",
    "Skill Trigger Evaluator",
    "Skill Description Optimizer",
}

ALLOWED_SKILL_FRONTMATTER = {
    "name",
    "description",
    "license",
    "allowed-tools",
    "compatibility",
    "metadata",
    "argument-hint",
    "user-invocable",
    "disable-model-invocation",
    "context",
}

ALLOWED_AGENT_FRONTMATTER = {
    "name",
    "description",
    "tools",
    "agents",
    "model",
    "user-invocable",
    "disable-model-invocation",
    "target",
    "handoffs",
    "hooks",
    "mcp-servers",
}

ALLOWED_AGENT_TOOLS = {"agent", "read", "search", "edit", "execute", "web"}

FORBIDDEN_RUNTIME_PATTERNS = {
    "legacy Kilo path": re.compile(r"(?i)(?:\.kilo(?:code)?/|~/.kilo|\bkilo code\b)"),
    "Kilo-only subagent API": re.compile(
        r"(?i)\b(?:delegate_task|new_task|attempt_completion|ask_followup_question|switch_mode|apply_diff|write_to_file)\b"
    ),
    "namespaced Superpowers skill": re.compile(r"\bsuperpowers:[a-z0-9-]+"),
}

FOREIGN_SKILL_TOOL_PATTERN = re.compile(
    r"\b(?:delegate_task|new_task|attempt_completion|ask_followup_question|"
    r"switch_mode|apply_diff|write_to_file|WebFetch|WebSearch|TodoWrite)\b|Bash\("
)

OBSOLETE_SKILLS = {
    "using-superpowers",
    "react-router-declarative-mode",
    "react-router-data-mode",
    "react-router-framework-mode",
    "ag-grid",
    "tailwind-v4-shadcn",
    "vitest-testing",
    "playwright-mcp-usage",
    "openapi-to-typescript",
}


def parse_frontmatter(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8-sig")
    if not text.startswith("---\n"):
        raise ValueError("frontmatter must start at byte 0")
    closing = text.find("\n---\n", 4)
    if closing < 0:
        raise ValueError("missing closing frontmatter delimiter")
    data = yaml.safe_load(text[4:closing])
    body = text[closing + 5 :]
    if not isinstance(data, dict):
        raise ValueError("frontmatter must be a mapping")
    if not body.strip():
        raise ValueError("body is empty")
    return data, body


def skill_directories() -> list[Path]:
    return sorted(path for path in SKILLS.iterdir() if path.is_dir() and (path / "SKILL.md").is_file())


def parse_manifest_names(path: Path) -> set[str]:
    names: set[str] = set()
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        if not line.startswith("| ") or "`" not in line:
            continue
        columns = [column.strip() for column in line.strip("|").split("|")]
        if len(columns) < 8 or columns[1] == "Skill":
            continue
        names.add(columns[1].strip("`"))
    return names


def validate_relative_links(skill_dir: Path, errors: list[str]) -> None:
    markdown_files = sorted(skill_dir.glob("*.agent.md")) if skill_dir == AGENTS else [skill_dir / "SKILL.md"]
    for markdown_file in markdown_files:
        text = markdown_file.read_text(encoding="utf-8-sig")
        targets = re.findall(r"\[[^\]]*\]\((?!https?://|mailto:|#)([^)\s]+)", text)
        targets += re.findall(r"`((?:references|scripts|templates|assets)/[^`\n]+)`", text)
        for raw_target in targets:
            target = raw_target.split("#", 1)[0]
            if re.search(r":\d+(?::\d+)?$", target):
                continue
            if target.startswith(".playwright-cli/") or any(char in target for char in "<>*?[]{}$"):
                continue
            if not (markdown_file.parent / target).exists():
                errors.append(f"{markdown_file.relative_to(ROOT)}: missing relative reference {target}")


def validate_runtime_terms(root: Path, errors: list[str]) -> None:
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        is_script = "scripts" in path.parts and path.suffix.lower() in {"", ".py", ".sh", ".js", ".cjs", ".mjs"}
        if path.suffix.lower() not in {".md", ".json", ".jsonc"} and not is_script:
            continue
        try:
            text = path.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError:
            continue
        for label, pattern in FORBIDDEN_RUNTIME_PATTERNS.items():
            match = pattern.search(text)
            if match:
                line = text.count("\n", 0, match.start()) + 1
                errors.append(f"{path.relative_to(ROOT)}:{line}: {label}: {match.group(0)!r}")


def validate_skills(errors: list[str]) -> set[str]:
    directories = skill_directories()
    names = {path.name for path in directories}
    if len(directories) != EXPECTED_SKILL_COUNT:
        errors.append(f"expected {EXPECTED_SKILL_COUNT} skills, found {len(directories)}")
    missing_workflows = sorted(REQUIRED_WORKFLOW_SKILLS - names)
    if missing_workflows:
        errors.append(f"missing workflow skills: {missing_workflows}")
    obsolete = sorted(OBSOLETE_SKILLS & names)
    if obsolete:
        errors.append(f"obsolete skill directories remain: {obsolete}")

    for directory in directories:
        path = directory / "SKILL.md"
        try:
            data, body = parse_frontmatter(path)
        except Exception as exc:
            errors.append(f"{path.relative_to(ROOT)}: {exc}")
            continue
        name = data.get("name")
        if name != directory.name:
            errors.append(f"{path.relative_to(ROOT)}: name {name!r} does not match directory")
        if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
            errors.append(f"{path.relative_to(ROOT)}: invalid VS Code skill name {name!r}")
        description = data.get("description")
        if not isinstance(description, str) or not description.strip() or len(description) > 1024:
            errors.append(f"{path.relative_to(ROOT)}: description must contain 1..1024 characters")
        unexpected = sorted(set(data) - ALLOWED_SKILL_FRONTMATTER)
        if unexpected:
            errors.append(f"{path.relative_to(ROOT)}: unsupported frontmatter keys {unexpected}")
        foreign_tool = FOREIGN_SKILL_TOOL_PATTERN.search(body)
        if foreign_tool:
            errors.append(
                f"{path.relative_to(ROOT)}: foreign runtime tool identifier {foreign_tool.group(0)!r}"
            )
        for flag in ("user-invocable", "disable-model-invocation"):
            if flag in data and not isinstance(data[flag], bool):
                errors.append(f"{path.relative_to(ROOT)}: {flag} must be a boolean")
        if "argument-hint" in data and not isinstance(data["argument-hint"], str):
            errors.append(f"{path.relative_to(ROOT)}: argument-hint must be a string")
        if data.get("context") not in (None, "fork"):
            errors.append(f"{path.relative_to(ROOT)}: context must be 'fork' when present")
        if data.get("context") == "fork" and "agent/runSubagent" in body:
            errors.append(
                f"{path.relative_to(ROOT)}: forked skill must not require nested subagents by default"
            )
        metadata = data.get("metadata")
        if metadata is not None and (
            not isinstance(metadata, dict)
            or any(
                not isinstance(key, str) or not isinstance(value, str)
                for key, value in metadata.items()
            )
        ):
            errors.append(f"{path.relative_to(ROOT)}: metadata must be a flat string-to-string mapping")
        validate_relative_links(directory, errors)

    manifest = SKILLS / "SKILLS_MANIFEST.md"
    manifest_names = parse_manifest_names(manifest)
    if manifest_names != names:
        errors.append(
            "manifest skill set differs from catalog: "
            f"missing={sorted(names - manifest_names)}, extra={sorted(manifest_names - names)}"
        )
    return names


def validate_agents(errors: list[str]) -> set[str]:
    paths = sorted(AGENTS.glob("*.agent.md"))
    if len(paths) != EXPECTED_AGENT_COUNT:
        errors.append(f"expected {EXPECTED_AGENT_COUNT} custom agents, found {len(paths)}")

    parsed: dict[str, tuple[Path, dict[str, Any]]] = {}
    for path in paths:
        try:
            data, _ = parse_frontmatter(path)
        except Exception as exc:
            errors.append(f"{path.relative_to(ROOT)}: {exc}")
            continue
        name = data.get("name")
        description = data.get("description")
        tools = data.get("tools")
        if not isinstance(name, str) or not name.strip():
            errors.append(f"{path.relative_to(ROOT)}: missing agent name")
            continue
        if name in parsed:
            errors.append(f"{path.relative_to(ROOT)}: duplicate agent name {name!r}")
        parsed[name] = (path, data)
        if not isinstance(description, str) or not description.strip():
            errors.append(f"{path.relative_to(ROOT)}: missing agent description")
        if not isinstance(tools, list) or not all(isinstance(tool, str) for tool in tools):
            errors.append(f"{path.relative_to(ROOT)}: tools must be a string list")
        else:
            unknown_tools = sorted(set(tools) - ALLOWED_AGENT_TOOLS)
            if unknown_tools:
                errors.append(f"{path.relative_to(ROOT)}: unknown tool sets {unknown_tools}")
        unexpected = sorted(set(data) - ALLOWED_AGENT_FRONTMATTER)
        if unexpected:
            errors.append(f"{path.relative_to(ROOT)}: unsupported frontmatter keys {unexpected}")
        if data.get("target") not in (None, "vscode"):
            errors.append(f"{path.relative_to(ROOT)}: target must be 'vscode' when present")

    names = set(parsed)
    if not REQUIRED_COORDINATORS <= names:
        errors.append(f"missing coordinator agents: {sorted(REQUIRED_COORDINATORS - names)}")
    if not REQUIRED_WORKERS <= names:
        errors.append(f"missing worker agents: {sorted(REQUIRED_WORKERS - names)}")

    for name, (path, data) in parsed.items():
        tools = data.get("tools", [])
        allowed_agents = data.get("agents", [])
        if allowed_agents == "*":
            errors.append(f"{path.relative_to(ROOT)}: wildcard subagent access is forbidden")
            continue
        if not isinstance(allowed_agents, list) or not all(isinstance(item, str) for item in allowed_agents):
            errors.append(f"{path.relative_to(ROOT)}: agents must be a string list")
            continue
        unresolved = sorted(set(allowed_agents) - names)
        if unresolved:
            errors.append(f"{path.relative_to(ROOT)}: unresolved agents {unresolved}")
        if allowed_agents and "agent" not in tools:
            errors.append(f"{path.relative_to(ROOT)}: agents allowlist requires the agent tool")
        if allowed_agents:
            agent_text = path.read_text(encoding="utf-8-sig")
            if "#tool:agent/runSubagent" not in agent_text:
                errors.append(
                    f"{path.relative_to(ROOT)}: coordinator must reference #tool:agent/runSubagent"
                )
        if name in REQUIRED_WORKERS:
            if data.get("user-invocable") is not False:
                errors.append(f"{path.relative_to(ROOT)}: worker must be hidden from the agent picker")
            if data.get("disable-model-invocation") is True:
                errors.append(f"{path.relative_to(ROOT)}: worker must remain available for model subagent invocation")
            if "agent" in tools:
                errors.append(f"{path.relative_to(ROOT)}: worker must not have the agent tool")
            if allowed_agents:
                errors.append(f"{path.relative_to(ROOT)}: worker must not invoke nested subagents")
        for handoff in data.get("handoffs", []) or []:
            if not isinstance(handoff, dict) or handoff.get("agent") not in names:
                errors.append(f"{path.relative_to(ROOT)}: handoff references an unknown agent")
    referenced_workers = {
        worker
        for _, data in parsed.values()
        for worker in (data.get("agents", []) if isinstance(data.get("agents", []), list) else [])
    }
    unreferenced_workers = sorted(REQUIRED_WORKERS - referenced_workers)
    if unreferenced_workers:
        errors.append(f"worker agents are not allowlisted by any coordinator: {unreferenced_workers}")
    validate_relative_links(AGENTS, errors)
    return names


def validate_instructions(errors: list[str]) -> None:
    paths = sorted(INSTRUCTIONS.glob("*.instructions.md"))
    if len(paths) != EXPECTED_INSTRUCTION_COUNT:
        errors.append(f"expected {EXPECTED_INSTRUCTION_COUNT} instruction files, found {len(paths)}")
    for path in paths:
        try:
            data, _ = parse_frontmatter(path)
        except Exception as exc:
            errors.append(f"{path.relative_to(ROOT)}: {exc}")
            continue
        if not isinstance(data.get("description"), str) or not data["description"].strip():
            errors.append(f"{path.relative_to(ROOT)}: missing description")
        if not isinstance(data.get("applyTo"), str) or not data["applyTo"].strip():
            errors.append(f"{path.relative_to(ROOT)}: missing applyTo glob")
        unexpected = sorted(set(data) - {"description", "applyTo"})
        if unexpected:
            errors.append(f"{path.relative_to(ROOT)}: unsupported frontmatter keys {unexpected}")


def main() -> int:
    errors: list[str] = []
    if (ROOT / ".kilo").exists():
        errors.append("legacy .kilo directory still exists")
    for required in (SKILLS, AGENTS, INSTRUCTIONS, ROOT / "scripts" / "install-vscode-chat.sh"):
        if not required.exists():
            errors.append(f"missing required path: {required.relative_to(ROOT)}")

    skill_names = validate_skills(errors) if SKILLS.is_dir() else set()
    agent_names = validate_agents(errors) if AGENTS.is_dir() else set()
    if INSTRUCTIONS.is_dir():
        validate_instructions(errors)
    for runtime_root in (SKILLS, AGENTS, INSTRUCTIONS):
        if runtime_root.is_dir():
            validate_runtime_terms(runtime_root, errors)

    if errors:
        print(f"VS Code Chat catalog validation failed with {len(errors)} issue(s):")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "VS Code Chat catalog validation passed: "
        f"{len(skill_names)} skills, {len(agent_names)} custom agents, "
        f"{EXPECTED_INSTRUCTION_COUNT} instruction files, no legacy runtime artifacts"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
