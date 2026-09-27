#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase 98: Network Namespace"
echo "================================================================"
ip addr 2>/dev/null || ifconfig | head -n 15
echo "Experiment completed successfully."
