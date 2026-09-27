#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 11 Experiment: Demonstrating Consumer Parallelism Ceiling ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/parallelism_limits.py
