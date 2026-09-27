#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase 33: Memory Before Virtual Memory"
echo "================================================================"
dmesg | grep BIOS-e820 2>/dev/null || true
echo "Experiment completed successfully."
