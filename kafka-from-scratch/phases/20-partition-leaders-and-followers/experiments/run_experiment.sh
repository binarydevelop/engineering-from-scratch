#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 20 Experiment: Inspecting Partition Leaders and Followers ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/cluster_metadata_inspector.py
