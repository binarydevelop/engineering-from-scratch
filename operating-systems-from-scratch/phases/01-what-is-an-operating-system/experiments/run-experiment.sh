#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase 01: What Is an Operating System?"
echo "================================================================"
cat /proc/version || uname -v
echo "Experiment completed successfully."
