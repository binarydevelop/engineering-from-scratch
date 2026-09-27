#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 12 Experiment: Expiration and TTL: Active vs. Passive Deletion ==="
python3 phases/12-expiration-and-ttl/code/expiration_engine.py
echo "✓ Phase 12 Experiment Complete."
