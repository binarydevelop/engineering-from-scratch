#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase 34: Address Spaces"
echo "================================================================"
cat /proc/self/maps 2>/dev/null || vmmap $$ | head -n 10
echo "Experiment completed successfully."
