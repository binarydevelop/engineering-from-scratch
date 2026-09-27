#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 24 Experiment: Exploring KRaft Cluster Metadata ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/kraft_metadata_explorer.py
