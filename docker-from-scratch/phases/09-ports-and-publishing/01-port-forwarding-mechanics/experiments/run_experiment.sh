#!/usr/bin/env bash
# phases/09-ports-and-publishing/01-port-forwarding-mechanics/experiments/run_experiment.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LESSON_DIR="$(dirname "$SCRIPT_DIR")"

echo "=== Running Phase 09 Experiment: Ports and Publishing ==="

# Cleanup prior containers
docker rm -f dfs-unpub dfs-pub >/dev/null 2>&1 || true

echo "Step 1: Building image with EXPOSE 8000 instruction"
docker build -t dfs-port-demo:v1 "$LESSON_DIR/code" >/dev/null

echo ""
echo "Step 2: Running container WITHOUT -p flag (testing EXPOSE alone)"
docker run -d --name dfs-unpub dfs-port-demo:v1
sleep 1

echo "Testing connection to localhost:8000 (Expect Failure):"
set +e
curl -s --connect-timeout 2 http://localhost:8000
FAIL_EXIT=$?
set -e
echo "Exit code: $FAIL_EXIT (Failed! EXPOSE does NOT publish ports to host)"

echo ""
echo "Step 3: Running second container WITH port publishing (-p 8888:8000)"
docker run -d --name dfs-pub -p 8888:8000 dfs-port-demo:v1
sleep 1

echo "Testing connection to host published port http://localhost:8888 (Expect Success):"
curl -s http://localhost:8888
echo ""

echo ""
echo "Step 4: Inspecting Docker port mappings"
docker port dfs-pub
echo "NetworkSettings.Ports inspection:"
docker inspect dfs-pub --format '{{json .NetworkSettings.Ports}}'

# Cleanup
docker rm -f dfs-unpub dfs-pub >/dev/null

echo ""
echo "Phase 09 Experiment Completed Successfully."
