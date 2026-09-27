#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 30 Experiment: Simulating Event Replay and State Recovery ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/replay_lab.py
