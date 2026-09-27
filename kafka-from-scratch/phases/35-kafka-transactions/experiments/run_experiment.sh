#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 35 Experiment: Simulating Kafka Two-Phase Transactions ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/transactional_processor.py
