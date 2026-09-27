#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 52 Experiment: Classifying Producer Failure Scenarios ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/chaos_producer_failure.py
