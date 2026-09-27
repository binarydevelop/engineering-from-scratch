#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 01 Experiment: Storage Latency Comparison ==="
python3 phases/01-why-redis-exists/code/measure_storage.py
echo "✓ Phase 01 Experiment Complete."
