#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase 80: Timers and Clocks"
echo "================================================================"
python3 -c "import time; print('Monotonic:', time.monotonic())"
echo "Experiment completed successfully."
