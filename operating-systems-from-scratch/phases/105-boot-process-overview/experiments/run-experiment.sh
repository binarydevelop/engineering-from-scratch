#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase 105: Boot Process Overview"
echo "================================================================"
dmesg | head -n 15 2>/dev/null || true
echo "Experiment completed successfully."
