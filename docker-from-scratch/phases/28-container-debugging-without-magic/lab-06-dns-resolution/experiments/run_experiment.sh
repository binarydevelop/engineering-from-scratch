#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CODE_DIR="${SCRIPT_DIR}/../code"

echo "============================================================"
echo "Lab 28-06: Container DNS Resolution Failure"
echo "============================================================"

cleanup() {
    echo "[*] Cleaning up lab-06 containers and networks..."
    docker compose -f "${CODE_DIR}/docker-compose.yml" down -v --remove-orphans >/dev/null 2>&1 || true
    docker compose -f "${CODE_DIR}/docker-compose.fixed.yml" down -v --remove-orphans >/dev/null 2>&1 || true
    docker rm -f lab06-broken-cache lab06-broken-client lab06-fixed-cache lab06-fixed-client >/dev/null 2>&1 || true
}
trap cleanup EXIT
cleanup

echo "[+] Step 1: Reproduce DNS resolution failure on default bridge..."
docker compose -f "${CODE_DIR}/docker-compose.yml" up -d cache

echo "[*] Starting client container on default bridge (network_mode: bridge)..."
set +e
docker compose -f "${CODE_DIR}/docker-compose.yml" run --rm client
CLIENT_EXIT=$?
set -e

if [ ${CLIENT_EXIT} -ne 0 ]; then
    echo "[+] CONFIRMED: DNS lookup failed as expected (exit code: ${CLIENT_EXIT})."
fi

echo ""
echo "[+] Step 2: Inspect /etc/resolv.conf on default bridge container..."
RESOLV_DEFAULT=$(docker exec lab06-broken-cache cat /etc/resolv.conf)
echo "${RESOLV_DEFAULT}"

if echo "${RESOLV_DEFAULT}" | grep -q "127.0.0.11"; then
    echo "[-] Unexpected: 127.0.0.11 found on default bridge!"
else
    echo "[+] CONFIRMED: Embedded DNS 127.0.0.11 is ABSENT on default bridge."
fi

echo ""
echo "[+] Step 3: Run the fix using a user-defined bridge network..."
docker compose -f "${CODE_DIR}/docker-compose.yml" down >/dev/null 2>&1 || true

docker compose -f "${CODE_DIR}/docker-compose.fixed.yml" up -d cache
echo "[*] Inspecting /etc/resolv.conf on user-defined bridge container..."
RESOLV_CUSTOM=$(docker exec lab06-fixed-cache cat /etc/resolv.conf)
echo "${RESOLV_CUSTOM}"

if echo "${RESOLV_CUSTOM}" | grep -q "127.0.0.11"; then
    echo "[+] CONFIRMED: Embedded DNS 127.0.0.11 is ACTIVE on user-defined bridge."
fi

echo "[*] Running client container on user-defined bridge..."
docker compose -f "${CODE_DIR}/docker-compose.fixed.yml" run --rm client

echo ""
echo "============================================================"
echo "[+] Lab 28-06 Completed successfully: DNS resolution verified."
echo "============================================================"
