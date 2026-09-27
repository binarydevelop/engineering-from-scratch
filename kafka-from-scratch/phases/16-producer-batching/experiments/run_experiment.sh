#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 16 Experiment: Benchmarking Producer Batching Impact ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/batching_benchmark.py
