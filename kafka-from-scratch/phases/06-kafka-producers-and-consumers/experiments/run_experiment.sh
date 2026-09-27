#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 06 Experiment: Running Real Kafka Producer and Consumer ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/producer.py
../../.venv/bin/python3 code/consumer.py
