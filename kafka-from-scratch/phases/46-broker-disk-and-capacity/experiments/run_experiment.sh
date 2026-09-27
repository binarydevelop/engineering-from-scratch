#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 46 Experiment: Running Kafka Capacity Sizing Model ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/capacity_calculator.py
