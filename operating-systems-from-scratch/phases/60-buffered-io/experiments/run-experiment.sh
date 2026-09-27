#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase 60: Buffered I/O"
echo "================================================================"
./benchmarks/io_buffering
echo "Experiment completed successfully."
