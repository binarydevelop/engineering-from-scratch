#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 26 Experiment: Benchmarking Sequential vs Random Disk I/O ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/sequential_vs_random_io.py
