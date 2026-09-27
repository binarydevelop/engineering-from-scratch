#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase 10: Shell Redirection"
echo "================================================================"
ls -l /proc/$$/fd || echo 'FD table redirected'
echo "Experiment completed successfully."
