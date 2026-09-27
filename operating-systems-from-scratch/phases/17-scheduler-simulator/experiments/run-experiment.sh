#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase 17: Scheduler Simulator"
echo "================================================================"
python3 simulations/scheduler_sim.py
echo "Experiment completed successfully."
