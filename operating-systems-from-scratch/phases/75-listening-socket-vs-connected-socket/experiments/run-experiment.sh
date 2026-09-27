#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase 75: Listening Socket vs Connected Socket"
echo "================================================================"
lsof -iTCP 2>/dev/null || true
echo "Experiment completed successfully."
