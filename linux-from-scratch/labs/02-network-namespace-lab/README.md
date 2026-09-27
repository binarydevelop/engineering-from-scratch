# Lab 02: Network Namespace Sandbox

## Objective
Safely practice configuring network interfaces, IP addresses, routing tables, and firewall rules without cutting off your primary SSH connection or altering host networking.

## Setup Procedure
```bash
# 1. Create two isolated network namespaces
sudo ip netns add net-client
sudo ip netns add net-server

# 2. Create a virtual ethernet cable (veth pair)
sudo ip link add veth-c type veth peer name veth-s

# 3. Move endpoints into namespaces
sudo ip link set veth-c netns net-client
sudo ip link set veth-s netns net-server

# 4. Configure IP addresses
sudo ip netns exec net-client ip addr add 10.200.1.1/24 dev veth-c
sudo ip netns exec net-client ip link set veth-c up
sudo ip netns exec net-client ip link set lo up

sudo ip netns exec net-server ip addr add 10.200.1.2/24 dev veth-s
sudo ip netns exec net-server ip link set veth-s up
sudo ip netns exec net-server ip link set lo up

# 5. Test isolated connectivity
sudo ip netns exec net-client ping -c 3 10.200.1.2
```

## Teardown
```bash
sudo ip netns del net-client
sudo ip netns del net-server
```
