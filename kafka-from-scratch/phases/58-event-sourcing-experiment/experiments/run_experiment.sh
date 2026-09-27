#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 58 Experiment: Simulating Event Sourcing and State Reconstruction ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/event_sourcing_lab.py
