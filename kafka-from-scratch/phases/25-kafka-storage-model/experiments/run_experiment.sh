#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 25 Experiment: Inspecting Kafka On-Disk Storage Structure ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/inspect_storage_segments.py
