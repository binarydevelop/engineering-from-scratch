#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 65 Experiment: Running Capstone 3 Production Lab ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/production_lab_runner.py
