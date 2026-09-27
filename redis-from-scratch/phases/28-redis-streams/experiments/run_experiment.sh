#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 28 Experiment: Redis Streams: Consumer Groups, PEL, and Crash Recovery ==="
python3 phases/28-redis-streams/code/streams_lab.py
echo "✓ Phase 28 Experiment Complete."
