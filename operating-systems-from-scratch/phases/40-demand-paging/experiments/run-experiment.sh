#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase 40: Demand Paging"
echo "================================================================"
python3 simulations/virtual_memory_sim.py
echo "Experiment completed successfully."
