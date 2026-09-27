#!/usr/bin/env bash
# ==============================================================================
# projects/08-tiny-internet/teardown_tiny_internet.sh
# Dismantles the 4-namespace Tiny Internet topology safely
# ==============================================================================

set -euo pipefail

if [ "$(id -u)" -ne 0 ]; then
    echo "ERROR: Root privileges required. Run with sudo: sudo $0"
    exit 1
fi

echo "==> Dismantling Tiny Internet topology..."
for ns in net-client net-router-a net-router-b net-server; do
    if ip netns list | grep -q "$ns"; then
        echo "Deleting namespace $ns..."
        ip netns delete "$ns" 2>/dev/null || true
    fi
done

echo "SUCCESS: Tiny Internet topology completely cleaned up."
