#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
target="${HOME}/.copilot"
dry_run=false

usage() {
  printf 'Usage: %s [--target PATH] [--dry-run]\n' "$0"
}

while (($#)); do
  case "$1" in
    --target)
      [[ $# -ge 2 ]] || { usage >&2; exit 2; }
      target="$2"
      shift 2
      ;;
    --dry-run)
      dry_run=true
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      printf 'Unknown argument: %s\n' "$1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

for directory in skills agents instructions; do
  [[ -d "${repo_root}/${directory}" ]] || {
    printf 'Missing source directory: %s\n' "${repo_root}/${directory}" >&2
    exit 1
  }
done

printf 'Install target: %s\n' "$target"
for directory in skills agents instructions; do
  printf '%s -> %s\n' "${repo_root}/${directory}" "${target}/${directory}"
done

if [[ "$dry_run" == true ]]; then
  exit 0
fi

mkdir -p "$target/skills" "$target/agents" "$target/instructions"

# Retire only the catalog entries removed by this migration. Never follow a
# redirected runtime directory when pruning, and preserve unrelated customizations.
canonical_target=$(cd "$target" && pwd -P)
canonical_skills=$(cd "$target/skills" && pwd -P)
canonical_agents=$(cd "$target/agents" && pwd -P)
[[ "$canonical_skills" == "$canonical_target/skills" ]] || {
  printf 'Refusing to prune a redirected skills directory: %s\n' "$target/skills" >&2
  exit 1
}
[[ "$canonical_agents" == "$canonical_target/agents" ]] || {
  printf 'Refusing to prune a redirected agents directory: %s\n' "$target/agents" >&2
  exit 1
}
retired_skills=(webapp-testing playwright-cli playwright-best-practices browser-testing-with-devtools accessibility accessibility-compliance fixing-motion-performance animation-performance frontend-debug-workflow frontend-task-preflight)
for skill in "${retired_skills[@]}"; do
  retired="$canonical_skills/$skill"
  [[ "${retired%/*}" == "$canonical_target/skills" ]] || exit 1
  if [[ -L "$retired" ]]; then
    rm -- "$retired"
  elif [[ -d "$retired" ]]; then
    rm -rf -- "$retired"
  fi
done

retired_agents=(frontend-debug.agent.md frontend-task-preflight.agent.md frontend-researcher.agent.md frontend-plan-reviewer.agent.md)
for agent in "${retired_agents[@]}"; do
  retired="$canonical_agents/$agent"
  [[ "${retired%/*}" == "$canonical_target/agents" ]] || exit 1
  if [[ -L "$retired" || -f "$retired" ]]; then
    rm -- "$retired"
  fi
done

cp -a "$repo_root/skills/." "$target/skills/"
cp -a "$repo_root/agents/." "$target/agents/"
cp -a "$repo_root/instructions/." "$target/instructions/"

printf 'Installed. Open VS Code and run Chat: Open Customizations, then inspect Chat Diagnostics.\n'
