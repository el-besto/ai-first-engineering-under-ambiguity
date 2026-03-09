#!/usr/bin/env bash
set -euo pipefail

action="${1:-}"
repo_root="$(git rev-parse --show-toplevel)"
state_dir="${repo_root}/.git/.precommit"
state_file="${state_dir}/originally_staged_paths.zlist"

capture_staged_files() {
  mkdir -p "${state_dir}"
  git -C "${repo_root}" diff --cached --name-only --diff-filter=ACMR -z > "${state_file}"
}

restage_staged_files() {
  if [[ ! -f "${state_file}" ]]; then
    exit 0
  fi

  captured_paths=()
  while IFS= read -r -d '' path; do
    captured_paths+=("${path}")
  done < "${state_file}"
  rm -f "${state_file}"

  if [[ ${#captured_paths[@]} -eq 0 ]]; then
    exit 0
  fi

  paths_to_add=()
  for path in "${captured_paths[@]}"; do
    if [[ -e "${repo_root}/${path}" || -L "${repo_root}/${path}" ]]; then
      paths_to_add+=("${path}")
      continue
    fi

    if git -C "${repo_root}" ls-files --error-unmatch -- "${path}" >/dev/null 2>&1; then
      paths_to_add+=("${path}")
    fi
  done

  if [[ ${#paths_to_add[@]} -eq 0 ]]; then
    exit 0
  fi

  git -C "${repo_root}" add -- "${paths_to_add[@]}" || true
}

case "${action}" in
  capture)
    capture_staged_files
    ;;
  restage)
    restage_staged_files
    ;;
  *)
    echo "Usage: ${0} {capture|restage}" >&2
    exit 2
    ;;
esac
