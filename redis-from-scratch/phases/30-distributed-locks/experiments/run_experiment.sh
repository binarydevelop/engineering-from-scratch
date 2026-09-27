#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 30 Experiment: Distributed Locks: Safety, TTLs, and Fencing Tokens ==="
python3 phases/30-distributed-locks/code/distributed_lock_lab.py
echo "✓ Phase 30 Experiment Complete."
