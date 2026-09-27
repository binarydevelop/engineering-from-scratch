#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase 37: Page Tables"
echo "================================================================"
grep PageTables /proc/meminfo 2>/dev/null || true
echo "Experiment completed successfully."
