#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase 112: Shared Memory"
echo "================================================================"
ls -la /dev/shm 2>/dev/null || true
echo "Experiment completed successfully."
