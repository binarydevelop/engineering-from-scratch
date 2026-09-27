#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 25 Experiment: Hot Keys: Workload Skew & Thread Saturation ==="
python3 phases/25-hot-keys/code/hot_key_lab.py
echo "✓ Phase 25 Experiment Complete."
