#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 13 Experiment: Verifying Manual Offset Commits ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/commit_semantics_demo.py
