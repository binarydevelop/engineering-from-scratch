#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 67 Experiment: Tracing the Complete Record Lifecycle ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/trace_record_lifecycle.py
