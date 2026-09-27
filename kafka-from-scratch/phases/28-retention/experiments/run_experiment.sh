#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 28 Experiment: Demonstrating Time-Based Log Retention ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/retention_lab.py
