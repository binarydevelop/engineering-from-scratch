#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 12 Experiment: Observing Rebalance Callbacks ==="
cd "$(dirname "$0")/.."
# Run observer briefly
../../.venv/bin/python3 code/rebalance_observer.py Worker-A &
PID1=$!
sleep 2

../../.venv/bin/python3 code/rebalance_observer.py Worker-B &
PID2=$!
sleep 3

kill -SIGINT $PID2
sleep 2
kill -SIGINT $PID1
