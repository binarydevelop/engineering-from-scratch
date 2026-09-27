#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CODE_DIR="${SCRIPT_DIR}/../code"

echo "============================================================"
echo "Lab 28-07: Service Dependency Startup Race Condition"
echo "============================================================"

cleanup() {
    echo "[*] Cleaning up lab-07 containers..."
    docker compose -f "${CODE_DIR}/docker-compose.yml" down -v --remove-orphans >/dev/null 2>&1 || true
    docker compose -f "${CODE_DIR}/docker-compose.fixed.yml" down -v --remove-orphans >/dev/null 2>&1 || true
    docker rm -f lab07-broken-db lab07-broken-app lab07-fixed-db lab07-fixed-app >/dev/null 2>&1 || true
}
trap cleanup EXIT
cleanup

echo "[+] Step 1: Reproduce startup race condition with naive depends_on..."
set +e
docker compose -f "${CODE_DIR}/docker-compose.yml" up --abort-on-container-exit app
RACE_EXIT=$?
set -e

echo "[*] Inspecting app logs from broken run:"
docker compose -f "${CODE_DIR}/docker-compose.yml" logs app || true

if [ ${RACE_EXIT} -ne 0 ]; then
    echo "[+] CONFIRMED: App failed because db was not yet accepting TCP connections."
fi

docker compose -f "${CODE_DIR}/docker-compose.yml" down -v >/dev/null 2>&1 || true

echo ""
echo "[+] Step 2: Run fixed compose with healthcheck and condition: service_healthy..."
docker compose -f "${CODE_DIR}/docker-compose.fixed.yml" up --abort-on-container-exit app

echo ""
echo "============================================================"
echo "[+] Lab 28-07 Completed successfully: Dependency race resolved."
echo "============================================================"
