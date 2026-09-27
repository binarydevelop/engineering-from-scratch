#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 21 Experiment: Monitoring ISR Set Changes ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/isr_monitor.py
