#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 51 Experiment: Simulating Consumer Failure Modes ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/chaos_consumer_failure.py
