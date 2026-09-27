#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 61 Experiment: Exploring Stream Processing Topologies ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/stream_processing_concepts.py
