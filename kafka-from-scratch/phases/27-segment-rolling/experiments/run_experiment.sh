#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 27 Experiment: Triggering and Observing Segment Rolling ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/segment_rolling_lab.py
