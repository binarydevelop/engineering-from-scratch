#!/usr/bin/env bash
# Verification test for Project 07
set -euo pipefail

LAB_DIR="/tmp/lfs-lab/project-07"

echo "[*] Checking Fault 1: Verifying port 8080 is freed..."
if [ -f "$LAB_DIR/rogue_port.pid" ]; then
    PID=$(cat "$LAB_DIR/rogue_port.pid")
    if ps -p "$PID" >/dev/null 2>&1; then
        echo "[✗] FAILURE: Rogue process PID $PID is still holding port 8080."
        exit 1
    fi
fi
echo "[✓] Port 8080 is clear."

echo "[*] Checking Fault 2: Verifying socket permissions..."
if [ -f "$LAB_DIR/app.sock" ]; then
    if [ ! -r "$LAB_DIR/app.sock" ]; then
        echo "[✗] FAILURE: app.sock is not readable."
        exit 1
    fi
fi
echo "[✓] Socket permissions verified."

echo "[✓] All Project 07 faults remediated successfully!"
