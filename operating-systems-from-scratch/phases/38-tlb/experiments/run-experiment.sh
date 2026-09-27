#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase 38: TLB (Translation Lookaside Buffer)"
echo "================================================================"
python3 simulations/virtual_memory_sim.py
echo "Experiment completed successfully."
