#!/usr/bin/env bash
# ==============================================================================
# reset-lab.sh
# Emergency cleanup: deletes all experimental namespaces and resets virtual links
# ==============================================================================

set -euo pipefail

if [ "$(id -u)" -ne 0 ]; then
    echo "ERROR: Root privileges required. Run: sudo $0"
    exit 1
fi

echo "==> Performing emergency network lab reset..."

# Delete any namespaces starting with ns- or lab-
if command -v ip >/dev/null 2>&1; then
    NAMESPACES=$(ip netns list | awk '{print $1}' || true)
    for ns in $NAMESPACES; do
        if [[ "$ns" =~ ^(ns-|lab-) ]]; then
            echo "Deleting namespace $ns..."
            ip netns delete "$ns" 2>/dev/null || true
        fi
    done

    # Clean orphaned test veth links and bridge
    for iface in $(ip link show | grep -E 'veth|br-test' | awk -F: '{print $2}' | tr -d ' ' || true); do
        echo "Removing test interface $iface..."
        ip link delete "$iface" 2>/dev/null || true
    done
fi

echo "SUCCESS: Emergency lab reset complete."
