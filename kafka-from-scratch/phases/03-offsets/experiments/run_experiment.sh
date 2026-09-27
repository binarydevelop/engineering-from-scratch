#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 03 Experiment: Demonstrating Offset Commit Mechanics & Failure Modes ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/offsets_experiment.py
