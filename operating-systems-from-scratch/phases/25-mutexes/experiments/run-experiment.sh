#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase 25: Mutexes"
echo "================================================================"
cat /proc/sys/kernel/sched_wakeup_granularity_ns 2>/dev/null || true
echo "Experiment completed successfully."
