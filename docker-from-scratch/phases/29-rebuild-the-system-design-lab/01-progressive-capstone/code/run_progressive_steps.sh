#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../../../../" && pwd)"
LAB_DIR="${REPO_ROOT}/projects/capstone-system-lab"

echo "================================================================================"
echo "Phase 29 Capstone: Rebuilding the System Design Lab Across 14 Progressive Steps"
echo "================================================================================"

cleanup_all() {
    echo "[*] Cleaning up any running containers, networks, and volumes..."
    docker compose -f "${LAB_DIR}/docker-compose.yml" down -v --remove-orphans >/dev/null 2>&1 || true
    docker rm -f capstone-step-app capstone-step-redis capstone-step-postgres capstone-step-nats capstone-step-prometheus capstone-step-grafana >/dev/null 2>&1 || true
    docker network rm capstone-manual-net >/dev/null 2>&1 || true
    docker volume rm capstone-step-pgdata >/dev/null 2>&1 || true
    # Kill host python app if running
    pkill -f "projects/capstone-system-lab/app/app.py" >/dev/null 2>&1 || true
}
trap cleanup_all EXIT
cleanup_all

# STEP 1: Run app directly on host
echo ""
echo "[Step 1/14] Running app directly on host..."
APP_PORT=8888 python3 "${LAB_DIR}/app/app.py" > /tmp/step1_app.log 2>&1 &
APP_PID=$!
sleep 1
curl -s http://127.0.0.1:8888/ | grep -q "Capstone System Design Lab"
echo "[+] Step 1 SUCCESS: App is running directly on host (PID: ${APP_PID})."
kill -9 ${APP_PID} >/dev/null 2>&1 || true
wait ${APP_PID} 2>/dev/null || true
sleep 1

# STEP 2: Containerize app
echo ""
echo "[Step 2/14] Containerizing app with Dockerfile..."
docker build -t capstone-app:v1 "${LAB_DIR}/app" >/dev/null
echo "[+] Step 2 SUCCESS: Built image 'capstone-app:v1'."

# STEP 3: Add Redis manually
echo ""
echo "[Step 3/14] Adding Redis manually via docker run..."
docker run -d --name capstone-step-redis redis:7-alpine >/dev/null
echo "[+] Step 3 SUCCESS: Redis container started."

# STEP 4: Create Docker network manually
echo ""
echo "[Step 4/14] Creating user-defined bridge network 'capstone-manual-net'..."
docker network create capstone-manual-net >/dev/null
echo "[+] Step 4 SUCCESS: Network created."

# STEP 5: Connect app -> Redis
echo ""
echo "[Step 5/14] Connecting Redis to network and running app container..."
docker network connect capstone-manual-net capstone-step-redis
docker run -d --name capstone-step-app --network capstone-manual-net \
  -e REDIS_HOST=capstone-step-redis -e REDIS_PORT=6379 \
  -p 8000:8000 capstone-app:v1 >/dev/null
sleep 2
HEALTH_JSON=$(curl -s http://127.0.0.1:8000/health || true)
echo "${HEALTH_JSON}" | python3 -c "import sys, json; d=json.load(sys.stdin); assert d['services']['redis']['status'] == 'ok'"
echo "[+] Step 5 SUCCESS: Containerized app resolved and communicated with Redis!"

# STEP 6: Add Postgres
echo ""
echo "[Step 6/14] Adding PostgreSQL manually on capstone-manual-net..."
docker run -d --name capstone-step-postgres --network capstone-manual-net \
  -e POSTGRES_PASSWORD=capstone_secret postgres:16-alpine >/dev/null
echo "[+] Step 6 SUCCESS: Postgres container started."

# STEP 7: Add Volume
echo ""
echo "[Step 7/14] Creating persistent named volume for Postgres..."
docker volume create capstone-step-pgdata >/dev/null
echo "[+] Step 7 SUCCESS: Created named volume 'capstone-step-pgdata'."

# STEP 8: Add NATS
echo ""
echo "[Step 8/14] Adding NATS message broker on capstone-manual-net..."
docker run -d --name capstone-step-nats --network capstone-manual-net nats:2.10-alpine >/dev/null
echo "[+] Step 8 SUCCESS: NATS container started."

# STEP 9: Add Prometheus
echo ""
echo "[Step 9/14] Adding Prometheus metrics collector..."
docker run -d --name capstone-step-prometheus --network capstone-manual-net \
  -v "${LAB_DIR}/monitoring/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml:ro" \
  prom/prometheus:v2.51.0 >/dev/null
echo "[+] Step 9 SUCCESS: Prometheus container started."

# STEP 10: Add Grafana
echo ""
echo "[Step 10/14] Adding Grafana visualization engine..."
docker run -d --name capstone-step-grafana --network capstone-manual-net \
  grafana/grafana:10.4.0 >/dev/null
echo "[+] Step 10 SUCCESS: All 6 components running manually!"

# STEP 11: Convert manual commands into Compose
echo ""
echo "[Step 11/14] Transitioning to Docker Compose specification..."
# Stop and wipe manual containers
docker rm -f capstone-step-app capstone-step-redis capstone-step-postgres capstone-step-nats capstone-step-prometheus capstone-step-grafana >/dev/null 2>&1 || true
docker network rm capstone-manual-net >/dev/null 2>&1 || true

docker compose -f "${LAB_DIR}/docker-compose.yml" up -d
echo "[+] Step 11 SUCCESS: Stack launched declaratively via Docker Compose."

# STEP 12: Add & Verify health checks
echo ""
echo "[Step 12/14] Verifying health checks and dependency gating..."
echo "[*] Waiting for PostgreSQL and Redis to report healthy..."
for i in $(seq 1 20); do
    PG_HEALTH=$(docker inspect capstone-postgres --format '{{.State.Health.Status}}' 2>/dev/null || echo "starting")
    RD_HEALTH=$(docker inspect capstone-redis --format '{{.State.Health.Status}}' 2>/dev/null || echo "starting")
    if [ "${PG_HEALTH}" = "healthy" ] && [ "${RD_HEALTH}" = "healthy" ]; then
        echo "[+] Both postgres and redis are HEALTHY!"
        break
    fi
    sleep 1
done

HEALTH_RESP=$(curl -s http://127.0.0.1:8000/health)
echo "[*] App /health payload: ${HEALTH_RESP}"
echo "${HEALTH_RESP}" | python3 -c "import sys, json; d=json.load(sys.stdin); assert d['status'] == 'healthy'"
echo "[+] Step 12 SUCCESS: Multi-service health checks confirmed healthy."

# STEP 13: Intentionally break dependencies
echo ""
echo "[Step 13/14] Intentionally breaking dependencies (stopping Redis)..."
docker stop capstone-redis >/dev/null
sleep 1
BROKEN_RESP=$(curl -s http://127.0.0.1:8000/health || true)
echo "[*] Degraded /health payload: ${BROKEN_RESP}"
echo "${BROKEN_RESP}" | python3 -c "import sys, json; d=json.load(sys.stdin); assert d['status'] == 'unhealthy'; assert d['services']['redis']['status'] == 'down'"
echo "[+] Step 13 CONFIRMED: Dependency failure cleanly detected."

# STEP 14: Debug and restore failures
echo ""
echo "[Step 14/14] Debugging and restoring the failed service..."
echo "[*] Restarting redis container..."
docker start capstone-redis >/dev/null
sleep 3
RESTORED_RESP=$(curl -s http://127.0.0.1:8000/health)
echo "[*] Restored /health payload: ${RESTORED_RESP}"
echo "${RESTORED_RESP}" | python3 -c "import sys, json; d=json.load(sys.stdin); assert d['status'] == 'healthy'"
echo "[+] Step 14 SUCCESS: System automatically reconciled and returned to healthy state!"

echo ""
echo "================================================================================"
echo "[+] All 14 Progressive Capstone Steps Completed and Verified!"
echo "================================================================================"
