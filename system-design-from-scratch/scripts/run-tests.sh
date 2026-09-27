#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
VENV_PYTEST="${REPO_ROOT}/.venv/bin/pytest"

echo "Executing System Design From Scratch Master Test Suite..."
"$VENV_PYTEST" -v "$@"
