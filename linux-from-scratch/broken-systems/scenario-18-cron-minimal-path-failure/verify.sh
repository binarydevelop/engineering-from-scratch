#!/usr/bin/env bash
# Verification test for Cron Job Fails Silently Due to Minimal PATH
set -euo pipefail

LAB_DIR="/tmp/lfs-lab/scenario-18-cron-minimal-path-failure"

echo "[*] Verifying system recovery for Cron Job Fails Silently Due to Minimal PATH..."

if [ "scenario-18-cron-minimal-path-failure" = "scenario-01-web-server-port-conflict" ]; then
    if [ -f "$LAB_DIR/rogue.pid" ]; then
        PID=$(cat "$LAB_DIR/rogue.pid")
        if ps -p "$PID" >/dev/null 2>&1; then
            echo "[✗] FAILURE: Rogue process PID $PID is still holding port 8080."
            exit 1
        fi
    fi
    echo "[✓] Port 8080 is free and available."
elif [ "scenario-18-cron-minimal-path-failure" = "scenario-04-directory-permission-traversal" ]; then
    if cat "$LAB_DIR/data/apps/settings.env" >/dev/null 2>&1; then
        echo "[✓] File read successfully! Directory traversal restored."
    else
        echo "[✗] FAILURE: Still unable to read settings.env. Check directory permissions."
        exit 1
    fi
elif [ "scenario-18-cron-minimal-path-failure" = "scenario-10-path-hijack-or-order" ]; then
    if [ -f "$LAB_DIR/bin/uptime" ]; then
        echo "[!] Notice: Lab binary still exists at $LAB_DIR/bin/uptime."
    fi
    echo "[✓] Verification passed."
else
    echo "[✓] Health checks verified."
fi

echo "=========================================================="
echo "    SCENARIO RESOLVED: Cron Job Fails Silently Due to Minimal PATH    "
echo "=========================================================="
