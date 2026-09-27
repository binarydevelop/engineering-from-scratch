#!/usr/bin/env bash
set -euo pipefail
sudo ip netns add ns-alpha
sudo ip netns add ns-beta
sudo ip link add veth-a type veth peer name veth-b
sudo ip link set veth-a netns ns-alpha
sudo ip link set veth-b netns ns-beta
sudo ip netns exec ns-alpha ip addr add 192.168.100.1/24 dev veth-a
sudo ip netns exec ns-beta ip addr add 192.168.100.2/24 dev veth-b
sudo ip netns exec ns-alpha ip link set veth-a up
sudo ip netns exec ns-beta ip link set veth-b up
sudo ip netns exec ns-alpha ip link set lo up
sudo ip netns exec ns-beta ip link set lo up
echo "Lab 01 active. Test with: sudo ip netns exec ns-alpha ping 192.168.100.2"
