#!/usr/bin/env bash
# ==============================================================================
# Reset Lab Script: Data Engineering From Scratch
# Cleans temporary files, reset databases, and regenerates sample datasets
# ==============================================================================
set -euo pipefail

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "Resetting Data Engineering Lab..."

# Remove runtime artifacts, temporary DuckDB files, logs, and caches
rm -rf "${BASE_DIR}/outputs/runs"
rm -rf "${BASE_DIR}/data/runtime"
rm -rf "${BASE_DIR}/data/warehouse"
rm -rf "${BASE_DIR}/data/lakehouse"
rm -rf "${BASE_DIR}"/*.duckdb
rm -rf "${BASE_DIR}"/*.duckdb.wal
rm -rf "${BASE_DIR}"/.pytest_cache
find "${BASE_DIR}" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

# Recreate fresh sample datasets
if [ -f "${BASE_DIR}/.venv/bin/python" ]; then
    "${BASE_DIR}/.venv/bin/python" "${BASE_DIR}/scripts/generate-data.py"
elif command -v python3 &> /dev/null; then
    python3 "${BASE_DIR}/scripts/generate-data.py"
fi

echo "Lab reset successfully completed."
