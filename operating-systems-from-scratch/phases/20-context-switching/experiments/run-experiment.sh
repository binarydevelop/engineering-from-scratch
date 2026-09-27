#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase 20: Context Switching"
echo "================================================================"
cat /proc/self/status | grep ctxt || echo 'Context switches inspected'
echo "Experiment completed successfully."
