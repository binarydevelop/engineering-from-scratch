#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 05 Experiment: Testing Multi-Topic Log Isolation ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/topic_log_manager.py
