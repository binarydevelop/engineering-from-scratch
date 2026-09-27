#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 44 Experiment: Simulating Poison Pill Quarantine to DLT ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/dead_letter_queue_lab.py
