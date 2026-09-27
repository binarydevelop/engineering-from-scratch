#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 62 Experiment: Running Tumbling Window Aggregator ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/tumbling_window_aggregator.py
