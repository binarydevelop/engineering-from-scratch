#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase 102: Build a Tiny Container Experiment"
echo "================================================================"
./projects/06-container-sandbox/container-launcher /bin/echo 'Sandbox initialized'
echo "Experiment completed successfully."
