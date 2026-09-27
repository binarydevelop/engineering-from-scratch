#!/usr/bin/env bash
# Automated Network Diagnostic Tree
# Systematically tests Interface -> IP -> Gateway -> DNS -> Remote Port
set -euo pipefail

TARGET_HOST="${1:-google.com}"
TARGET_PORT="${2:-443}"

echo "=== NETWORK DIAGNOSTIC SUITE : TARGET $TARGET_HOST:$TARGET_PORT ==="

echo "[1/5] Checking Local Loopback & Physical Interfaces..."
ip -br link

echo ""
echo "[2/5] Checking Local IP Assignments..."
ip -br addr

echo ""
echo "[3/5] Inspecting Default Gateway & Route..."
DEFAULT_GW=$(ip route show default | awk '{print $3}' | head -1)
if [ -n "$DEFAULT_GW" ]; then
    echo "  Default Gateway IP: $DEFAULT_GW"
    if ping -c 1 -W 2 "$DEFAULT_GW" >/dev/null 2>&1; then
        echo "  [✓] Default Gateway is reachable via ICMP."
    else
        echo "  [✗] WARNING: Cannot reach default gateway via ICMP."
    fi
else
    echo "  [✗] CRITICAL: No default gateway configured in routing table!"
fi

echo ""
echo "[4/5] Testing DNS Resolution for $TARGET_HOST..."
if getent hosts "$TARGET_HOST" >/dev/null 2>&1; then
    RESOLVED_IP=$(getent hosts "$TARGET_HOST" | awk '{print $1}' | head -1)
    echo "  [✓] Resolved $TARGET_HOST -> $RESOLVED_IP"
else
    echo "  [✗] CRITICAL: DNS resolution failed for $TARGET_HOST"
fi

echo ""
echo "[5/5] Testing TCP Connection to $TARGET_HOST:$TARGET_PORT..."
if command -v nc >/dev/null 2>&1; then
    if nc -z -w 3 "$TARGET_HOST" "$TARGET_PORT" 2>/dev/null; then
        echo "  [✓] TCP handshake successful with $TARGET_HOST:$TARGET_PORT"
    else
        echo "  [✗] FAILED to establish TCP connection to $TARGET_HOST:$TARGET_PORT"
    fi
fi
echo "================================================================="
