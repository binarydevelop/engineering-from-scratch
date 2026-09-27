#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase 73: Sockets From First Principles"
echo "================================================================"
ss -tl 2>/dev/null || netstat -an | head -n 10
echo "Experiment completed successfully."
