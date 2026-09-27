#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase 110: Process Security Boundaries"
echo "================================================================"
cat /proc/sys/kernel/yama/ptrace_scope 2>/dev/null || true
echo "Experiment completed successfully."
