#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase 41: Virtual Memory and Disk"
echo "================================================================"
free -h 2>/dev/null || vm_stat
echo "Experiment completed successfully."
