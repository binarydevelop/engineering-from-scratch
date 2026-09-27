#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 56 Experiment: Running Capstone 1 - Mini-Kafka Engine ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/mini_kafka.py
