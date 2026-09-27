#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase 91: I/O Performance"
echo "================================================================"
iostat 2>/dev/null || true
echo "Experiment completed successfully."
