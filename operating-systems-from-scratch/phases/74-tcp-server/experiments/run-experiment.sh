#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase 74: TCP Server"
echo "================================================================"
ss -tulpn 2>/dev/null || lsof -iTCP -sTCP:LISTEN
echo "Experiment completed successfully."
