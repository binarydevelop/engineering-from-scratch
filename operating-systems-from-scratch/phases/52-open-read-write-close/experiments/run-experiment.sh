#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase 52: open/read/write/close"
echo "================================================================"
strace -e trace=file ls
echo "Experiment completed successfully."
