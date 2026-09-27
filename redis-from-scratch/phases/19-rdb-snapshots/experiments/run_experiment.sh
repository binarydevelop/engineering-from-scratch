#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 19 Experiment: RDB Snapshots: Point-in-Time Backups & Copy-on-Write ==="
python3 phases/19-rdb-snapshots/code/rdb_snapshots.py
echo "✓ Phase 19 Experiment Complete."
