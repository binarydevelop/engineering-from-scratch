#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 03 Experiment: Custom TCP Key-Value Server ==="
python3 phases/03-make-the-key-value-store-a-server/code/tcp_kv_server.py
echo "✓ Phase 03 Experiment Complete."
