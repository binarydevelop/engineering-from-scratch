#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 10 Experiment: Consumer Group Range Partition Assignment Simulation ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/consumer_group_sim.py
