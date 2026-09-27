#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase 21: Threads From First Principles"
echo "================================================================"
ps -M $$ || ps -T -p $$
echo "Experiment completed successfully."
