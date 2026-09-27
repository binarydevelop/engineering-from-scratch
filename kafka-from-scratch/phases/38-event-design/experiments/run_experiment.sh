#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 38 Experiment: Generating Standard Domain Event Envelopes ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/event_design_patterns.py
