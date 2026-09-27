#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase 69: poll() Deep Dive"
echo "================================================================"
python3 -c "import select; print(dir(select))"
echo "Experiment completed successfully."
