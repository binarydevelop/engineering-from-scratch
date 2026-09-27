# Project 08: Tiny Internet Capstone

> **Motto**: The global Internet is not fundamentally different from your local host; it is simply multiple local area networks stitched together across autonomous routing hops exchanging packets via longest prefix matches.

---

## 1. Overview
In this capstone project, you instantiate an entire multi-network Internet topology inside 4 isolated Linux namespaces:
1. `net-client`: Local client workstation LAN (`10.10.1.0/24`)
2. `net-router-a`: Egress Gateway router connecting client LAN to transit backbone
3. `net-router-b`: Destination Gateway router connecting transit backbone to server LAN
4. `net-server`: Datacenter server LAN (`10.20.1.0/24`) running DNS and HTTP services

## 2. Multi-Hop Topology Diagram
```text
[ net-client ]            [ net-router-a ]           [ net-router-b ]           [ net-server ]
 10.10.1.10/24             10.10.1.1/24               172.16.0.2/30              10.20.1.10/24
       │                         │                          │                          │
       └──( veth-c <-> veth-ra )─┘                          └──( veth-rb <-> veth-s )──┘
                                 │                          │
                                 └──( veth-ra-t <-> veth-rb-t )──┘
                                        172.16.0.0/30
                                       (Transit Network)
```

## 3. Running & Inspecting on Linux
```bash
# Setup topology
sudo ./setup_tiny_internet.sh

# Run end-to-end multi-hop traceroute from Client to Server
sudo ip netns exec net-client traceroute -n 10.20.1.10

# Capture packets at intermediate transit hop while sending traffic
sudo ip netns exec net-router-a tcpdump -i veth-ra-t -nn &
sudo ip netns exec net-client ping -c 3 10.20.1.10

# Tear down safely
sudo ./teardown_tiny_internet.sh
```

## 4. Cross-Platform Simulation
```bash
python3 verify_tiny_internet.py
```
