#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase 87: File Descriptor Exhaustion"
echo "================================================================"
./labs/broken-systems/lab-05-fd-leak
echo "Experiment completed successfully."
