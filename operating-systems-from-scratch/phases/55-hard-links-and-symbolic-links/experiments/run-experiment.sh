#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase 55: Hard Links and Symbolic Links"
echo "================================================================"
ln -s Makefile test_symlink && ls -l test_symlink && rm test_symlink
echo "Experiment completed successfully."
