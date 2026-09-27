#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 39 Experiment: Verifying Partition-Scoped Ordering ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/ordering_guarantees_lab.py
