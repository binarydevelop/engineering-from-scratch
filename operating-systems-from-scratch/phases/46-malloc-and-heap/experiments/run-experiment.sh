#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase 46: malloc and Heap"
echo "================================================================"
cat /proc/sys/vm/overcommit_memory 2>/dev/null || true
echo "Experiment completed successfully."
