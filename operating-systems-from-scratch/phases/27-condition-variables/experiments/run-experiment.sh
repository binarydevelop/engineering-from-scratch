#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase 27: Condition Variables"
echo "================================================================"
cat /proc/self/wchan 2>/dev/null || true
echo "Experiment completed successfully."
