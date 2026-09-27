#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase 12: File Descriptors"
echo "================================================================"
ls -la /proc/$$/fd 2>/dev/null || lsof -p $$
echo "Experiment completed successfully."
