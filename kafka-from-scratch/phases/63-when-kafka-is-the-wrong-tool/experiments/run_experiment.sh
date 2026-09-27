#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 63 Experiment: Evaluating When Kafka Is the Wrong Tool ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/evaluate_kafka_fit.py
