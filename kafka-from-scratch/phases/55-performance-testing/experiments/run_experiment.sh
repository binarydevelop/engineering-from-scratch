#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 55 Experiment: Running Standardized Kafka Performance Benchmark ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/benchmark_runner.py
