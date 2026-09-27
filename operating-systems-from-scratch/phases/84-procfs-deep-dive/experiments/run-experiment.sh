#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase 84: /proc Deep Dive"
echo "================================================================"
cat /proc/meminfo 2>/dev/null || true
echo "Experiment completed successfully."
