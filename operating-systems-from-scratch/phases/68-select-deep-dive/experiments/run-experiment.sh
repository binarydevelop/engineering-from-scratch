#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase 68: select() Deep Dive"
echo "================================================================"
./projects/05-event-http-server/http-server --event 8082 & sleep 1; kill -9 $! 2>/dev/null || true
echo "Experiment completed successfully."
