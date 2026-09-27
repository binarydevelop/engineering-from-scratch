#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

echo "Resetting local simulation states, databases, and temporary caches..."
find "$REPO_ROOT" -type f -name "*.db" -delete
find "$REPO_ROOT" -type f -name "*.sqlite3" -delete
find "$REPO_ROOT" -type f -name "*.log" -delete
find "$REPO_ROOT" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
rm -rf "${REPO_ROOT}/.pytest_cache"

echo "Lab reset completed cleanly."
