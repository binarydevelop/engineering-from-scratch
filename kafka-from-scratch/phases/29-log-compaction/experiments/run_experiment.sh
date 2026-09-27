#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 29 Experiment: Demonstrating Log Compaction and Tombstones ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/log_compaction_lab.py
