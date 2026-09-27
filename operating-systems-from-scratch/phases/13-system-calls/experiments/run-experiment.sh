#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase 13: System Calls"
echo "================================================================"
strace -c ls
echo "Experiment completed successfully."
