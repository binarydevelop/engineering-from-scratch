#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 33 Experiment: Memory Analysis: Fragmentation, RSS, and jemalloc ==="
python3 phases/33-memory-analysis/code/memory_audit.py
echo "✓ Phase 33 Experiment Complete."
