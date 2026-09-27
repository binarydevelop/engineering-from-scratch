#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 59 Experiment: Simulating Database Change Data Capture ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/cdc_simulation.py
