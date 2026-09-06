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
cp -a "$repo_root/skills/." "$target/skills/"
cp -a "$repo_root/agents/." "$target/agents/"
cp -a "$repo_root/instructions/." "$target/instructions/"

printf 'Installed. Open VS Code and run Chat: Open Customizations, then inspect Chat Diagnostics.\n'
