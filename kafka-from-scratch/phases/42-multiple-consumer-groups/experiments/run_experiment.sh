#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 42 Experiment: Demonstrating Multiple Consumer Group Fan-Out ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/multi_group_fanout.py
