#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 33 Experiment: Simulating Network Drops and Retry Duplication ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/network_retry_duplicate_sim.py
