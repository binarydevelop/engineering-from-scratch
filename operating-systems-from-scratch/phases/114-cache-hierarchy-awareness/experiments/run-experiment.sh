#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase 114: Cache Hierarchy Awareness"
echo "================================================================"
sysctl -a | grep cache 2>/dev/null || lscpu | grep cache 2>/dev/null || true
echo "Experiment completed successfully."
