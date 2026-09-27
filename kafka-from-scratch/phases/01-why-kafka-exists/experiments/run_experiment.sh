#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 01 Experiment: Measuring Fragility of Direct Synchronous Coupling ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/direct_coupled_services.py
