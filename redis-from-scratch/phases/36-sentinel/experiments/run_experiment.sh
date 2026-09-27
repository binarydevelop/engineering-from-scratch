#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 36 Experiment: Redis Sentinel: Quorum, Health Checks, and Failover ==="
python3 phases/36-sentinel/code/sentinel_lab.py
echo "✓ Phase 36 Experiment Complete."
