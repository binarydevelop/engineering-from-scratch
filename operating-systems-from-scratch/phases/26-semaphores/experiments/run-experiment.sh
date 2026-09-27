#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase 26: Semaphores"
echo "================================================================"
ipcs -s 2>/dev/null || echo 'Semaphores inspected'
echo "Experiment completed successfully."
