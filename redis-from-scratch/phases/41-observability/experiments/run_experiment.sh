#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 41 Experiment: Observability: Metrics, Prometheus, and the Top 8 Signals ==="
python3 phases/41-observability/code/observability_collector.py
echo "✓ Phase 41 Experiment Complete."
