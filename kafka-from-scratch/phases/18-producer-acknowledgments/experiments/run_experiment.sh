#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 18 Experiment: Measuring Producer Acknowledgment Latency ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/acks_durability_lab.py
