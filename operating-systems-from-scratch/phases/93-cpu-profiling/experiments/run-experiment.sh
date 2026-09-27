#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase 93: CPU Profiling"
echo "================================================================"
time ./benchmarks/cache_locality
echo "Experiment completed successfully."
