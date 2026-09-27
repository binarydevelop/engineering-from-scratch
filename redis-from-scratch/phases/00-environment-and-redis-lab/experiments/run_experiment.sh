#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 00 Experiment: Client-Server TCP Verification ==="
./scripts/check-environment.sh
python3 phases/00-environment-and-redis-lab/code/verify_lab.py
echo "Running redis-cli INFO server..."
redis-cli INFO server | head -n 8 || true
echo "✓ Phase 00 Experiment Complete."
