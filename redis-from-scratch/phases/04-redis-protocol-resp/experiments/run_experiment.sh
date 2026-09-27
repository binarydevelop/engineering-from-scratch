#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 04 Experiment: Raw RESP Serialization ==="
python3 phases/04-redis-protocol-resp/code/resp_codec.py
echo "✓ Phase 04 Experiment Complete."
