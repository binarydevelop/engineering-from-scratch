#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 08 Experiment: Verifying Key-to-Partition Routing Consistency ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/key_partitioning.py
