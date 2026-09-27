#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CODE_DIR="${SCRIPT_DIR}/../code"

echo "============================================================"
echo "Lab 28-08: Zombie Process Reaping and PID 1 Signal Handling"
echo "============================================================"

cleanup() {
    echo "[*] Cleaning up lab-08 containers..."
    docker rm -f lab08-broken-test lab08-fixed-test >/dev/null 2>&1 || true
}
trap cleanup EXIT
cleanup

echo "[+] Step 1: Build broken container (shell form CMD)..."
docker build -t lab08-broken:latest -f "${CODE_DIR}/Dockerfile.broken" "${CODE_DIR}" >/dev/null

echo "[+] Step 2: Run broken container and inspect process hierarchy..."
docker run -d --name lab08-broken-test lab08-broken:latest >/dev/null
sleep 1

echo "[*] Process tree inside broken container (via docker top):"
docker top lab08-broken-test || true

echo ""
echo "[*] Testing stop behavior on broken container (with 2s timeout)..."
START_TIME=$(date +%s)
set +e
docker stop -t 2 lab08-broken-test >/dev/null
STOP_TIME=$(date +%s)
set -e

DURATION=$((STOP_TIME - START_TIME))
EXIT_CODE=$(docker inspect lab08-broken-test --format '{{.State.ExitCode}}')
echo "[+] Stopped in ${DURATION}s with exit code ${EXIT_CODE}"

if [ "${EXIT_CODE}" -eq 137 ]; then
    echo "[+] CONFIRMED: Process failed to handle SIGTERM and was SIGKILLed (exit code 137)."
fi

echo ""
echo "[+] Step 3: Build fixed container and run with --init (tini subreaper)..."
docker build -t lab08-fixed:latest -f "${CODE_DIR}/Dockerfile.fixed" "${CODE_DIR}" >/dev/null
docker run -d --init --name lab08-fixed-test lab08-fixed:latest >/dev/null
sleep 1

echo "[*] Process tree inside fixed container (via docker top, note docker-init):"
docker top lab08-fixed-test || true

echo ""
echo "[*] Testing stop behavior on fixed container..."
START_TIME=$(date +%s)
docker stop -t 2 lab08-fixed-test >/dev/null
STOP_TIME=$(date +%s)
DURATION=$((STOP_TIME - START_TIME))
EXIT_CODE=$(docker inspect lab08-fixed-test --format '{{.State.ExitCode}}')

echo "[+] Fixed container stopped in ${DURATION}s with exit code ${EXIT_CODE}"
if [ "${EXIT_CODE}" -eq 0 ]; then
    echo "[+] SUCCESS: Graceful shutdown verified under PID 1 init supervisor!"
fi

echo ""
echo "============================================================"
echo "[+] Lab 28-08 Completed successfully."
echo "============================================================"
