#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase 97: Mount Namespace"
echo "================================================================"
mount | head -n 10
echo "Experiment completed successfully."
