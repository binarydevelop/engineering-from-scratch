#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 66 Experiment: Reviewing the 20-Question System Design Framework ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/system_design_evaluator.py
