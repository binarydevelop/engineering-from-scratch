#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 50 Experiment: Executing Controlled Chaos Broker Failure ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/chaos_broker_failure.py
