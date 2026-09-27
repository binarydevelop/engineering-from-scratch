#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase 123: Capstone 5: Event-Driven HTTP Server"
echo "================================================================"
make -C projects/05-event-http-server
echo "Experiment completed successfully."
