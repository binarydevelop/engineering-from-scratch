#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase 39: Page Faults"
echo "================================================================"
vmstat 1 3
echo "Experiment completed successfully."
