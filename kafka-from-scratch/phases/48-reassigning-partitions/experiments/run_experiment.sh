#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 48 Experiment: Generating and Verifying Partition Reassignment ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/reassign_partitions_demo.py
