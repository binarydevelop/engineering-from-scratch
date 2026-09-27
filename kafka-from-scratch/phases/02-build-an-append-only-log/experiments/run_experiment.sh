#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 02 Experiment: Running MiniLog Append-Only Implementation ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/mini_log.py
