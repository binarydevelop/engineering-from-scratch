#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 04 Experiment: Testing TCP Log Server and Client ==="
cd "$(dirname "$0")/.."

# Start server in background
../../.venv/bin/python3 code/tcp_log_server.py &
SERVER_PID=$!
sleep 1

# Run client requests
../../.venv/bin/python3 code/tcp_log_client.py

# Terminate background server
kill $SERVER_PID
echo "Server terminated."
