#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase 88: CPU Saturation"
echo "================================================================"
top -b -n 1 | head -n 12
echo "Experiment completed successfully."
