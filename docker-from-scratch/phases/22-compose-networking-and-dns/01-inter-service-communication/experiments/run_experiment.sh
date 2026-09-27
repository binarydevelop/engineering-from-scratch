#!/usr/bin/env bash
# phases/22-compose-networking-and-dns/01-inter-service-communication/experiments/run_experiment.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LESSON_DIR="$(dirname "$SCRIPT_DIR")"
CODE_DIR="$LESSON_DIR/code"

echo "=== Running Phase 22 Experiment: Compose Networking & DNS ==="

# Cleanup prior state
docker compose -f "$CODE_DIR/docker-compose.yml" down -v >/dev/null 2>&1 || true

echo "Step 1: Launching multi-tier Compose topology"
docker compose -f "$CODE_DIR/docker-compose.yml" up -d

WEB_CID=$(docker compose -f "$CODE_DIR/docker-compose.yml" ps -q web)
docker cp "$CODE_DIR/test_connections.py" "$WEB_CID:/test_connections.py"

echo "Waiting 2 seconds for Postgres cluster initialization..."
sleep 2

echo ""
echo "Step 2: Connecting from 'web' to 'redis' and 'postgres' using SERVICE NAMES"
docker exec "$WEB_CID" python3 /test_connections.py redis 6379
docker exec "$WEB_CID" python3 /test_connections.py postgres 5432

echo ""
echo "Step 3: [MANDATORY EXPERIMENT] Replacing 'redis' with 'localhost' inside web container"
echo "Command: python3 /test_connections.py localhost 6379 (Expect Failure)"
set +e
docker exec "$WEB_CID" python3 /test_connections.py localhost 6379
LOCAL_EXIT=$?
set -e
if [ "$LOCAL_EXIT" -ne 0 ]; then
    echo "--> VERIFIED: Connecting to 'localhost:6379' fails inside web container!"
    echo "    Reason: Redis runs in its own network namespace, NOT on web's loopback interface."
fi

echo ""
echo "Step 4: Testing Multi-Tier Network Isolation"
echo "Launching test client on 'frontend' network only (Expect inability to reach postgres):"
set +e
docker run --rm --network dfs-net-demo_frontend alpine:latest \
    nc -z -w 2 postgres 5432 2>&1
NET_ISO_EXIT=$?
set -e
if [ "$NET_ISO_EXIT" -ne 0 ]; then
    echo "--> VERIFIED: Frontend network CANNOT reach or resolve Postgres on backend network!"
fi

# Cleanup
docker compose -f "$CODE_DIR/docker-compose.yml" down -v >/dev/null

echo ""
echo "Phase 22 Experiment Completed Successfully."
