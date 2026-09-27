#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 14 Experiment: Demonstrating At-Most-Once vs At-Least-Once Failure Modes ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/delivery_semantics_lab.py
