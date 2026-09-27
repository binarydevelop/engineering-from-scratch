#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 21 Experiment: AOF Rewrite & Compaction: Log Compaction Mechanics ==="
python3 phases/21-aof-rewrite-and-persistence-tradeoffs/code/aof_rewrite.py
echo "✓ Phase 21 Experiment Complete."
