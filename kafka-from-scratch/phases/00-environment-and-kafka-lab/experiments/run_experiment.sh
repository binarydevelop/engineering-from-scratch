#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 00 Experiment: Verifying Kafka Lab Environment ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/verify_lab.py
