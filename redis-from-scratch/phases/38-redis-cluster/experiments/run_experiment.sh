#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 38 Experiment: Redis Cluster: 16,384 Hash Slots & -MOVED Redirects ==="
python3 phases/38-redis-cluster/code/cluster_slots.py
echo "✓ Phase 38 Experiment Complete."
