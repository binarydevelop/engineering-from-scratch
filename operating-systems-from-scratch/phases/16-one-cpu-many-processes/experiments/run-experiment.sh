#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase 16: One CPU, Many Processes"
echo "================================================================"
top -b -n 1 | head -n 15
echo "Experiment completed successfully."
