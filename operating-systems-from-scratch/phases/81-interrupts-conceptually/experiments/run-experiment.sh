#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase 81: Interrupts Conceptually"
echo "================================================================"
cat /proc/interrupts 2>/dev/null || true
echo "Experiment completed successfully."
