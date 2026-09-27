#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 20 Experiment: Append-Only File: Write-Ahead Logging & fsync Tradeoffs ==="
python3 phases/20-append-only-file/code/aof_fsync.py
echo "✓ Phase 20 Experiment Complete."
