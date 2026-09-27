#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 54 Experiment: Displaying Kafka Golden Metrics Framework ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/cluster_metrics_collector.py
