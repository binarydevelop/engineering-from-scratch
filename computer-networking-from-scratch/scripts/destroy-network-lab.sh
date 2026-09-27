#!/usr/bin/env bash
# ==============================================================================
# destroy-network-lab.sh
# Safely tears down the isolated 3-node routed network namespace topology
# ==============================================================================

set -euo pipefail

if [ "$(id -u)" -ne 0 ]; then
    echo "ERROR: Root privileges required. Run: sudo $0"
    exit 1
fi

echo "==> Dismantling network namespace lab..."

for ns in ns-client ns-router ns-server; do
    if ip netns list | grep -q "$ns"; then
        echo "Deleting namespace $ns..."
        ip netns delete "$ns" 2>/dev/null || true
    fi
done

# Deleting namespaces automatically cleans up associated veth pairs inside them,
# but verify no orphaned veth interfaces remain in the host namespace:
for v in veth-c veth-rc veth-s veth-rs; do
    if ip link show "$v" >/dev/null 2>&1; then
        echo "Cleaning orphaned interface $v..."
        ip link delete "$v" 2>/dev/null || true
    fi
done

echo "SUCCESS: Network lab dismantled. Host network state clean."
