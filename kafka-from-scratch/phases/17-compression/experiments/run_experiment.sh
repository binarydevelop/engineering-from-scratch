#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 17 Experiment: Measuring Batch Compression Efficiency ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/compression_benchmark.py
