#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase 111: IPC Overview"
echo "================================================================"
ipcs 2>/dev/null || true
echo "Experiment completed successfully."
