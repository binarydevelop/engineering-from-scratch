#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 32 Experiment: Simulating Backpressure and Catch-up Capacity ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/backpressure_sim.py
