#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 13 Experiment: Memory and Eviction: Expiration != Eviction ==="
python3 phases/13-memory-and-eviction/code/eviction_policies.py
echo "✓ Phase 13 Experiment Complete."
