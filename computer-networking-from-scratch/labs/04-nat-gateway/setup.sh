#!/usr/bin/env bash
set -euo pipefail
sudo ip netns add ns-priv
sudo ip netns add ns-nat
sudo ip netns add ns-wan
sudo ip link add veth-p type veth peer name veth-np
sudo ip link set veth-p netns ns-priv
sudo ip link set veth-np netns ns-nat
sudo ip link add veth-nw type veth peer name veth-w
sudo ip link set veth-nw netns ns-nat
sudo ip link set veth-w netns ns-wan

sudo ip netns exec ns-priv ip addr add 10.0.1.10/24 dev veth-p
sudo ip netns exec ns-priv ip link set veth-p up
sudo ip netns exec ns-priv ip link set lo up
sudo ip netns exec ns-priv ip route add default via 10.0.1.1

sudo ip netns exec ns-nat ip addr add 10.0.1.1/24 dev veth-np
sudo ip netns exec ns-nat ip addr add 203.0.113.1/24 dev veth-nw
sudo ip netns exec ns-nat ip link set veth-np up
sudo ip netns exec ns-nat ip link set veth-nw up
sudo ip netns exec ns-nat sysctl -w net.ipv4.ip_forward=1 >/dev/null
sudo ip netns exec ns-nat iptables -t nat -A POSTROUTING -o veth-nw -j MASQUERADE

sudo ip netns exec ns-wan ip addr add 203.0.113.100/24 dev veth-w
sudo ip netns exec ns-wan ip link set veth-w up
sudo ip netns exec ns-wan ip link set lo up

echo "Lab 04 active. Test SNAT: sudo ip netns exec ns-priv ping -c 2 203.0.113.100"
