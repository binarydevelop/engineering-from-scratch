#!/usr/bin/env bash
# Verification test for Nginx Reverse Proxy
set -euo pipefail

PROXY_PORT=8000
BACKEND_PORT=8080

echo "[*] Testing connection to Reverse Proxy on port $PROXY_PORT..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "http://127.0.0.1:${PROXY_PORT}/health" || echo "FAIL")

if [ "$HTTP_CODE" = "200" ]; then
    echo "[✓] Reverse Proxy is actively routing requests to backend (HTTP 200 OK)."
else
    echo "[✗] ERROR: Expected HTTP 200 from proxy, received: $HTTP_CODE"
    exit 1
fi

echo "[*] Inspecting proxy headers returned by backend..."
curl -s -D - "http://127.0.0.1:${PROXY_PORT}/health" -o /dev/null | grep -i "content-type"

echo "[✓] Reverse proxy verification passed."
