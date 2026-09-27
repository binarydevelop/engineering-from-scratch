#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 57 Experiment: Running Capstone 2 Event-Driven Architecture ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/event_driven_app.py
