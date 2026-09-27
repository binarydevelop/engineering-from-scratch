#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase 05: Process Creation"
echo "================================================================"
pstree -p $$ || ps -ef | head -n 15
echo "Experiment completed successfully."
