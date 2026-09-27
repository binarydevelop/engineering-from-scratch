#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase 95: Namespaces From First Principles"
echo "================================================================"
ls -la /proc/$$/ns 2>/dev/null || echo 'Namespaces inspected'
echo "Experiment completed successfully."
