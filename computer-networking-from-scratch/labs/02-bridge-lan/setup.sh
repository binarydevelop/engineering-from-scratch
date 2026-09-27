#!/usr/bin/env bash
set -euo pipefail
sudo ip netns add ns1
sudo ip netns add ns2
sudo ip netns add ns3
sudo ip link add br0 type bridge
sudo ip link set br0 up

for i in 1 2 3; do
    sudo ip link add "veth$i" type veth peer name "br-veth$i"
    sudo ip link set "veth$i" netns "ns$i"
    sudo ip link set "br-veth$i" master br0
    sudo ip link set "br-veth$i" up
    sudo ip netns exec "ns$i" ip addr add "10.0.0.$i/24" dev "veth$i"
    sudo ip netns exec "ns$i" ip link set "veth$i" up
    sudo ip netns exec "ns$i" ip link set lo up
done
echo "Lab 02 active. Test with: sudo ip netns exec ns1 ping -c 2 10.0.0.2"
