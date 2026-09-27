#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase 08: wait() and Process Lifecycle"
echo "================================================================"
ps -eo pid,ppid,stat,comm | grep -E 'Z|defunct'
echo "Experiment completed successfully."
