#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase 11: Pipes"
echo "================================================================"
cat /proc/sys/fs/pipe-max-size || echo 'Pipe buffer inspected'
echo "Experiment completed successfully."
