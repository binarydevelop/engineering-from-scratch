#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 50: Cluster Health Transitions ==="
python3 phases/50-cluster-health/code/50_cluster_health.py
