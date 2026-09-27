#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase 90: Memory Pressure"
echo "================================================================"
cat /proc/meminfo 2>/dev/null || vm_stat
echo "Experiment completed successfully."
