#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 40 Experiment: Inspecting Kafka Timestamp Semantics ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/time_semantics_lab.py
