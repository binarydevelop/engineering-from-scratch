#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 15 Experiment: Running Idempotent Consumer Simulation ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/idempotent_consumer.py
