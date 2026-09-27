#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 60: Slow Queries & Diagnostics ==="
python3 phases/60-slow-queries/code/60_slow_queries.py
