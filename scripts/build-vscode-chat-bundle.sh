#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
output="${repo_root}/dist/frontend-skill-vscode-chat-bundle.tar.gz"

usage() {
  printf 'Usage: %s [--output FILE]\n' "$0"
}

while (($#)); do
  case "$1" in
    --output)
      [[ $# -ge 2 ]] || { usage >&2; exit 2; }
      output="$2"
      shift 2
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

for path in \
  skills \
  agents \
  instructions \
  scripts/install-vscode-chat.sh \
  scripts/validate_skill_catalog.py \
  tests/test_vscode_conversion.py \
  requirements-dev.txt \
  docs/AGENT_USAGE_GUIDE.zh-TW.md \
  docs/VM_COPY_GUIDE.zh-TW.md \
  docs/VS_CODE_CHAT_SETUP.zh-TW.md; do
  [[ -e "${repo_root}/${path}" ]] || {
    printf 'Missing bundle input: %s\n' "${repo_root}/${path}" >&2
    exit 1
  }
done

output_dir="$(dirname "$output")"
mkdir -p "$output_dir"
output="$(cd "$output_dir" && pwd -P)/$(basename "$output")"

temp_root="$(mktemp -d)"
trap 'rm -rf "$temp_root"' EXIT
bundle_root="${temp_root}/frontend-skill-vscode-chat"
mkdir -p "${bundle_root}/scripts" "${bundle_root}/tests" "${bundle_root}/docs"

cp -a "${repo_root}/skills" "${bundle_root}/skills"
cp -a "${repo_root}/agents" "${bundle_root}/agents"
cp -a "${repo_root}/instructions" "${bundle_root}/instructions"
cp "${repo_root}/scripts/install-vscode-chat.sh" "${bundle_root}/scripts/"
cp "${repo_root}/scripts/validate_skill_catalog.py" "${bundle_root}/scripts/"
cp "${repo_root}/tests/test_vscode_conversion.py" "${bundle_root}/tests/"
cp "${repo_root}/requirements-dev.txt" "${bundle_root}/"
cp "${repo_root}/docs/AGENT_USAGE_GUIDE.zh-TW.md" "${bundle_root}/docs/"
cp "${repo_root}/docs/VM_COPY_GUIDE.zh-TW.md" "${bundle_root}/docs/"
cp "${repo_root}/docs/VS_CODE_CHAT_SETUP.zh-TW.md" "${bundle_root}/docs/"

find "$bundle_root" -type d -name __pycache__ -prune -exec rm -rf {} +
find "$bundle_root" -type f \( -name '*.pyc' -o -name '*.pyo' \) -delete

(
  cd "$temp_root"
  tar -czf "$output" frontend-skill-vscode-chat
)

printf 'Bundle created: %s\n' "$output"
printf 'On the Ubuntu VM:\n'
printf '  tar -xzf %s\n' "$(basename "$output")"
printf '  cd frontend-skill-vscode-chat\n'
printf '  bash scripts/install-vscode-chat.sh\n'
