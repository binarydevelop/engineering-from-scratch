#!/usr/bin/env bash
# phases/01-processes-before-containers/01-host-process-lifecycle/experiments/run_experiment.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LESSON_DIR="$(dirname "$SCRIPT_DIR")"

echo "=== Running Phase 01 Experiment: Process Lifecycle ==="

echo "Step 1: Launching server.py as a background host process"
APP_ENV="production" python3 "$LESSON_DIR/code/server.py" > /tmp/dfs_server.stdout 2> /tmp/dfs_server.stderr &
SERVER_PID=$!
echo "Launched server PID: $SERVER_PID"

sleep 1

echo ""
echo "Step 2: Sending HTTP request to process"
curl -s http://127.0.0.1:8001

echo ""
echo "Step 3: Inspecting process table and listening port"
python3 "$LESSON_DIR/code/inspect_process.py" "$SERVER_PID"

echo ""
echo "Step 4: Sending SIGTERM to process (testing graceful shutdown)"
kill -TERM "$SERVER_PID"
wait "$SERVER_PID" || true

echo "Stderr log during shutdown:"
cat /tmp/dfs_server.stderr

echo ""
echo "Step 5: Testing uncatchable SIGKILL"
python3 "$LESSON_DIR/code/server.py" > /dev/null 2>&1 &
KILL_PID=$!
sleep 0.5
kill -9 "$KILL_PID"
set +e
wait "$KILL_PID"
EXIT_CODE=$?
set -e
echo "Process killed with SIGKILL (9). Exit code: $EXIT_CODE (128 + 9 = 137)"

rm -f /tmp/dfs_server.stdout /tmp/dfs_server.stderr
echo ""
echo "Phase 01 Experiment Completed Successfully."
