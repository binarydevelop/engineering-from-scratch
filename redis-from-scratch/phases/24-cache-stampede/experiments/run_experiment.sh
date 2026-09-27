#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 24 Experiment: Cache Stampede: The Thundering Herd Problem ==="
python3 phases/24-cache-stampede/code/stampede_simulator.py
echo "✓ Phase 24 Experiment Complete."
