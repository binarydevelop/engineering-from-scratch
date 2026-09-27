#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 37 Experiment: Demonstrating Schema Evolution and Breaking Changes ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/schema_evolution_lab.py
