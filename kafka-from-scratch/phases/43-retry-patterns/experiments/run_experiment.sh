#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 43 Experiment: Demonstrating Non-Blocking Retry Topics ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/retry_topic_pattern.py
