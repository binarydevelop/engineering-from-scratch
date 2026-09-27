#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 36 Experiment: Exploring EOS Boundaries ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/eos_boundaries_lab.py
