#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 07 Experiment: Partitioning Mechanics & Local Offsets ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/partitioned_log_sim.py
