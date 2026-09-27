#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 22 Experiment: Demonstrating Resilient Leader Failover ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/leader_failover_lab.py
