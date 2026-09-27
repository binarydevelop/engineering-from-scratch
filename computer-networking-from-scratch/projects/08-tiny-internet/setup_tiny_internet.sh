#!/usr/bin/env bash
# ==============================================================================
# projects/08-tiny-internet/setup_tiny_internet.sh
# Constructs a complete virtual multi-hop Internet topology using Linux namespaces
#
# Topology:
#   [net-client]                [net-router-a]             [net-router-b]             [net-server]
#   10.10.1.10/24 <──veth──> 10.10.1.1 | 172.16.0.1 <─veth─> 172.16.0.2 | 10.20.1.1 <──veth──> 10.20.1.10/24
#     (Client LAN)                 (Transit Network)                 (Server LAN)
# ==============================================================================

set -euo pipefail

if [ "$(id -u)" -ne 0 ]; then
    echo "ERROR: Root privileges required. Run with sudo: sudo $0"
    exit 1
fi

echo "==> 1. Creating 4 isolated network namespaces..."
for ns in net-client net-router-a net-router-b net-server; do
    ip netns add "$ns"
    ip netns exec "$ns" ip link set lo up
done

echo "==> 2. Creating virtual ethernet (veth) links..."
# Link 1: Client LAN (net-client <-> net-router-a)
ip link add veth-c type veth peer name veth-ra-c
ip link set veth-c netns net-client
ip link set veth-ra-c netns net-router-a

# Link 2: Transit Network (net-router-a <-> net-router-b)
ip link add veth-ra-t type veth peer name veth-rb-t
ip link set veth-ra-t netns net-router-a
ip link set veth-rb-t netns net-router-b

# Link 3: Server LAN (net-router-b <-> net-server)
ip link add veth-rb-s type veth peer name veth-s
ip link set veth-rb-s netns net-router-b
ip link set veth-s netns net-server

echo "==> 3. Configuring IP addresses & bringing interfaces UP..."
# Client LAN: 10.10.1.0/24
ip netns exec net-client ip addr add 10.10.1.10/24 dev veth-c
ip netns exec net-client ip link set veth-c up

ip netns exec net-router-a ip addr add 10.10.1.1/24 dev veth-ra-c
ip netns exec net-router-a ip link set veth-ra-c up

# Transit Network: 172.16.0.0/30
ip netns exec net-router-a ip addr add 172.16.0.1/30 dev veth-ra-t
ip netns exec net-router-a ip link set veth-ra-t up

ip netns exec net-router-b ip addr add 172.16.0.2/30 dev veth-rb-t
ip netns exec net-router-b ip link set veth-rb-t up

# Server LAN: 10.20.1.0/24
ip netns exec net-router-b ip addr add 10.20.1.1/24 dev veth-rb-s
ip netns exec net-router-b ip link set veth-rb-s up

ip netns exec net-server ip addr add 10.20.1.10/24 dev veth-s
ip netns exec net-server ip link set veth-s up

echo "==> 4. Configuring Routing Tables & Enabling IP Forwarding..."
# Router A forwarding and static routes
ip netns exec net-router-a sysctl -w net.ipv4.ip_forward=1 >/dev/null
ip netns exec net-router-a ip route add 10.20.1.0/24 via 172.16.0.2 dev veth-ra-t

# Router B forwarding and static routes
ip netns exec net-router-b sysctl -w net.ipv4.ip_forward=1 >/dev/null
ip netns exec net-router-b ip route add 10.10.1.0/24 via 172.16.0.1 dev veth-rb-t

# Client default route
ip netns exec net-client ip route add default via 10.10.1.1 dev veth-c

# Server default route
ip netns exec net-server ip route add default via 10.20.1.1 dev veth-s

echo "==> 5. Verifying Multi-Hop End-to-End Traceroute..."
if ip netns exec net-client ping -c 2 -W 2 10.20.1.10 >/dev/null 2>&1; then
    echo "SUCCESS: Multi-hop connectivity established across both routers!"
else
    echo "WARNING: Connectivity check failed. Inspect routes with ip route."
fi

echo ""
echo "=================================================================="
echo "Tiny Internet Virtual Network Active:"
echo "  net-client (10.10.1.10) ──► net-router-a (172.16.0.1)"
echo "                           ──► net-router-b (172.16.0.2)"
echo "                           ──► net-server (10.20.1.10)"
echo "Execute:"
echo "  sudo ip netns exec net-client traceroute -n 10.20.1.10"
echo "  sudo ./projects/08-tiny-internet/teardown_tiny_internet.sh"
echo "=================================================================="
