#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 31 Experiment: Calculating Real-Time Consumer Lag ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/lag_monitor.py
