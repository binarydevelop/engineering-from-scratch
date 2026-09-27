#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase 63: Journaling Filesystems"
echo "================================================================"
python3 simulations/disk_consistency_sim.py
echo "Experiment completed successfully."
