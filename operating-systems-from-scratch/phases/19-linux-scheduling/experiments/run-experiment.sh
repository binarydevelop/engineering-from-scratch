#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase 19: Linux Scheduling"
echo "================================================================"
ps -eo pid,ni,pri,comm | head -n 10
echo "Experiment completed successfully."
