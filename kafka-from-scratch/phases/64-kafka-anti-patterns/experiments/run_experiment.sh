#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 64 Experiment: Analyzing Kafka Production Anti-Patterns ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/anti_patterns_analyzer.py
