#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase 100: cgroups Practical Lab"
echo "================================================================"
cat /sys/fs/cgroup/cgroup.controllers 2>/dev/null || true
echo "Experiment completed successfully."
