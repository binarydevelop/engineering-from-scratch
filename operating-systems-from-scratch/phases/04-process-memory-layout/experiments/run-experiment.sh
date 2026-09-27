#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase 04: Process Memory Layout"
echo "================================================================"
cat /proc/self/maps || vmmap $$ | head -n 20
echo "Experiment completed successfully."
