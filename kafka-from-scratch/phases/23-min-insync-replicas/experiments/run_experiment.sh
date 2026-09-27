#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 23 Experiment: Testing min.insync.replicas Enforcement ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/min_isr_lab.py
