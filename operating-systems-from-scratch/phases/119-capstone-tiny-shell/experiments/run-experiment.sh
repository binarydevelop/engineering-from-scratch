#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase 119: Capstone 1: Expanded Unix Shell"
echo "================================================================"
make -C projects/01-tiny-shell && ./projects/01-tiny-shell/mini-shell
echo "Experiment completed successfully."
