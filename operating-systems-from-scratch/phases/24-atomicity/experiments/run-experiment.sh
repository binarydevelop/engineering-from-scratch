#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase 24: Atomicity"
echo "================================================================"
otool -tv ./benchmarks/syscall_overhead || objdump -d ./benchmarks/syscall_overhead
echo "Experiment completed successfully."
