#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase 14: strace Laboratory"
echo "================================================================"
strace -e trace=openat,read,write ls
echo "Experiment completed successfully."
