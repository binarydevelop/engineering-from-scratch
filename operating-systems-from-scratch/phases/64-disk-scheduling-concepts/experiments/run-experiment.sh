#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase 64: Disk Scheduling Concepts"
echo "================================================================"
cat /sys/block/*/queue/scheduler 2>/dev/null || true
echo "Experiment completed successfully."
