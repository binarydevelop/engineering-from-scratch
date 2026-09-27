#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 49 Experiment: Demonstrating Broker Join Semantics ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/add_broker_simulation.py
