#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase 02: User Space and Kernel Space"
echo "================================================================"
cat /proc/kallsyms | head -n 10 || echo 'Kernel symbols protected'
echo "Experiment completed successfully."
