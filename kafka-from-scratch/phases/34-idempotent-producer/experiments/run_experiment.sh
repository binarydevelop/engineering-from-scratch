#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 34 Experiment: Verifying Idempotent Producer Execution ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/idempotent_producer_lab.py
