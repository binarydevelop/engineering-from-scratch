#!/usr/bin/env bash
# phases/10-docker-bridge-networks/01-custom-bridge-interfaces/experiments/run_experiment.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LESSON_DIR="$(dirname "$SCRIPT_DIR")"

echo "=== Running Phase 10 Experiment: Docker Bridge Networks ==="

# Cleanup prior test resources
docker rm -f dfs-node-a dfs-node-b dfs-isolated >/dev/null 2>&1 || true
docker network rm dfs-learning-net >/dev/null 2>&1 || true

echo "Step 1: Creating custom bridge network 'dfs-learning-net'"
docker network create --subnet 172.28.0.0/16 dfs-learning-net

echo ""
echo "Step 2: Starting two containers attached to dfs-learning-net"
docker run -d --name dfs-node-a --network dfs-learning-net alpine:latest sleep 60
docker run -d --name dfs-node-b --network dfs-learning-net alpine:latest sleep 60

echo ""
echo "Step 3: Inspecting the custom bridge network"
python3 "$LESSON_DIR/code/inspect_bridge.py" dfs-learning-net

echo ""
echo "Step 4: Testing point-to-point packet flow between Node A and Node B"
NODE_B_IP=$(docker inspect dfs-node-b --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}')
echo "Node B Allocated IP: $NODE_B_IP"
echo "Pinging Node B from Node A across the bridge:"
docker exec dfs-node-a ping -c 2 "$NODE_B_IP"

echo ""
echo "Step 5: Testing network isolation against an unattached container"
docker run -d --name dfs-isolated alpine:latest sleep 60
ISOLATED_IP=$(docker inspect dfs-isolated --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}')
echo "Isolated container (default bridge) IP: $ISOLATED_IP"

echo "Attempting to ping isolated container from Node A (Expect Timeout/Failure):"
set +e
docker exec dfs-node-a ping -W 2 -c 2 "$ISOLATED_IP"
PING_EXIT=$?
set -e
if [ "$PING_EXIT" -ne 0 ]; then
    echo "Confirmed: Network boundaries prevent cross-bridge communication!"
fi

# Cleanup
docker rm -f dfs-node-a dfs-node-b dfs-isolated >/dev/null
docker network rm dfs-learning-net >/dev/null

echo ""
echo "Phase 10 Experiment Completed Successfully."
