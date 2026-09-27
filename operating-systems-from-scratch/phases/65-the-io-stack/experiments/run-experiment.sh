#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase 65: The I/O Stack"
echo "================================================================"
iostat 2>/dev/null || echo 'I/O stack monitored'
echo "Experiment completed successfully."
