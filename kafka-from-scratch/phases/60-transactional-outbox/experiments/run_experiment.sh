#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 60 Experiment: Demonstrating Transactional Outbox Pattern ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/transactional_outbox_lab.py
