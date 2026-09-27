#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 22 Experiment: Redis as a Cache: Cache-Aside vs. Write-Through ==="
python3 phases/22-redis-as-a-cache/code/cache_aside_lab.py
echo "✓ Phase 22 Experiment Complete."
