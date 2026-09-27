#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 19 Experiment: Simulating Distributed Replication and Failover ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/replication_sim.py
