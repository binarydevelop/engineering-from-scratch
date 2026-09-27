#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 75: Index Aliases & Zero-Downtime Swaps ==="
python3 phases/75-aliases-and-zero-downtime-index-migration/code/75_aliases_and_zero_downtime_index_migration.py
