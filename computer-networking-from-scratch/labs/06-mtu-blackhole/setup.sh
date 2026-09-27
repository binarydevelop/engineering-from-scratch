#!/usr/bin/env bash
set -euo pipefail
sudo ip netns add ns-mtu-client
sudo ip netns add ns-mtu-server
sudo ip link add v-c type veth peer name v-s
sudo ip link set v-c netns ns-mtu-client
sudo ip link set v-s netns ns-mtu-server
sudo ip netns exec ns-mtu-client ip addr add 192.168.200.1/24 dev v-c
sudo ip netns exec ns-mtu-server ip addr add 192.168.200.2/24 dev v-s
sudo ip netns exec ns-mtu-client ip link set v-c up
sudo ip netns exec ns-mtu-server ip link set v-s up
# Reduce MTU on server interface to 1400
sudo ip netns exec ns-mtu-server ip link set v-s mtu 1400
echo "Lab 06 active. Test with: sudo ip netns exec ns-mtu-client ping -M do -s 1472 192.168.200.2"
