#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 41 Experiment: Contrasting Queue vs Log Architectures ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/queue_vs_log_comparison.py
