#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase 66: Blocking I/O"
echo "================================================================"
./projects/05-event-http-server/http-server --seq 8081 & sleep 1; kill -9 $! 2>/dev/null || true
echo "Experiment completed successfully."
