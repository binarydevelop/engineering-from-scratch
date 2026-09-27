#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase 15: CPU Execution"
echo "================================================================"
sysctl -a | grep machdep.cpu || cat /proc/cpuinfo
echo "Experiment completed successfully."
