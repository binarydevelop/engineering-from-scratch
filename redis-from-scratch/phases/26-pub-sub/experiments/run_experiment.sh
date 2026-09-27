#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 26 Experiment: Pub/Sub: Ephemeral Messaging vs. Durable Queuing ==="
python3 phases/26-pub-sub/code/pubsub_lab.py
echo "✓ Phase 26 Experiment Complete."
