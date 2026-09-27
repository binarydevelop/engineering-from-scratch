#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase 03: Programs vs Processes"
echo "================================================================"
ps -o pid,ppid,comm,state
echo "Experiment completed successfully."
