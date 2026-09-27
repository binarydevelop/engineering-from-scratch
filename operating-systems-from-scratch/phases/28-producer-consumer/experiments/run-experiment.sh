#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase 28: Producer Consumer"
echo "================================================================"
python3 simulations/concurrency_bank_sim.py
echo "Experiment completed successfully."
