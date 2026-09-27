#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 47 Experiment: Running Partition Sizing Recommendation Tool ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/partition_sizing_tool.py
