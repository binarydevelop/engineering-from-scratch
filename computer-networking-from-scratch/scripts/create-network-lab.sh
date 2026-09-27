#!/usr/bin/env bash
# ==============================================================================
# create-network-lab.sh
# Safely constructs an isolated 3-node routed network topology using Linux namespaces
#
# Topology:
#   [ ns-client ]                [ ns-router ]                [ ns-server ]
#    10.99.1.10/24 <─veth─> 10.99.1.1/24 | 10.99.2.1/24 <─veth─> 10.99.2.10/24
#   (Subnet 10.99.1.0/24)                                    (Subnet 10.99.2.0/24)
# ==============================================================================

set -euo pipefail

if [ "$(id -u)" -ne 0 ]; then
    echo "ERROR: This script requires root privileges to manage network namespaces."
    echo "Please run: sudo $0"
    exit 1
fi

echo "==> Creating network namespaces..."
ip netns add ns-client
ip netns add ns-router
ip netns add ns-server

echo "==> Bringing up loopback interfaces..."
ip netns exec ns-client ip link set lo up
ip netns exec ns-router ip link set lo up
ip netns exec ns-server ip link set lo up

echo "==> Creating veth pairs..."
# Client to Router link
ip link add veth-c type veth peer name veth-rc
ip link set veth-c netns ns-client
ip link set veth-rc netns ns-router

# Server to Router link
ip link add veth-s type veth peer name veth-rs
ip link set veth-s netns ns-server
ip link set veth-rs netns ns-router

echo "==> Assigning IP addresses and bringing interfaces UP..."
# Client network: 10.99.1.0/24
ip netns exec ns-client ip addr add 10.99.1.10/24 dev veth-c
ip netns exec ns-client ip link set veth-c up

ip netns exec ns-router ip addr add 10.99.1.1/24 dev veth-rc
ip netns exec ns-router ip link set veth-rc up

# Server network: 10.99.2.0/24
ip netns exec ns-server ip addr add 10.99.2.10/24 dev veth-s
ip netns exec ns-server ip link set veth-s up

ip netns exec ns-router ip addr add 10.99.2.1/24 dev veth-rs
ip netns exec ns-router ip link set veth-rs up

echo "==> Configuring routing tables..."
# Client default route via Router
ip netns exec ns-client ip route add default via 10.99.1.1 dev veth-c

# Server default route via Router
ip netns exec ns-server ip route add default via 10.99.2.1 dev veth-s

echo "==> Enabling IPv4 forwarding on ns-router..."
ip netns exec ns-router sysctl -w net.ipv4.ip_forward=1 >/dev/null

echo "==> Verifying end-to-end connectivity across router..."
if ip netns exec ns-client ping -c 2 -W 2 10.99.2.10 >/dev/null 2>&1; then
    echo "SUCCESS: Ping from ns-client (10.99.1.10) to ns-server (10.99.2.10) SUCCEEDED!"
else
    echo "WARNING: Initial ping failed. Inspect routes with: sudo ip netns exec ns-client ip route"
fi

echo ""
echo "=================================================================="
echo "Network Lab Topology Active:"
echo "  [ns-client] (10.99.1.10) ──veth──► (10.99.1.1) [ns-router]"
echo "                                     (10.99.2.1) ──veth──► [ns-server] (10.99.2.10)"
echo "To execute commands:"
echo "  sudo ip netns exec ns-client ping 10.99.2.10"
echo "  sudo ip netns exec ns-server python3 -m http.server 8080"
echo "  sudo ip netns exec ns-client curl http://10.99.2.10:8080"
echo "To tear down:"
echo "  sudo ./scripts/destroy-network-lab.sh"
echo "=================================================================="
