#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 09 Experiment: Analyzing Key Skew and Hot Partitions ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/hot_partition_analyzer.py
