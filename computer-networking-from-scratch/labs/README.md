# Reusable Linux Network Namespace Labs

> **Rule**: All routing mutations, bridge setups, firewall rules, and NAT tests must occur strictly inside these isolated namespaces. Never mutate your host interface configuration.

| ID | Lab Topology | Description | Setup Script |
| :--- | :--- | :--- | :--- |
| **01** | [Two-Node Direct veth Link](01-two-node-veth/) | Constructs two namespaces (ns-alpha and ns-beta) connected by a point-to-point virtual ethernet pair. | `./setup.sh` |
| **02** | [Multi-Host Linux Bridge LAN](02-bridge-lan/) | Connects three isolated namespaces (ns1, ns2, ns3) into a single Layer-2 broadcast domain via a Linux software bridge. | `./setup.sh` |
| **03** | [Multi-Subnet Routed Network](03-three-node-router/) | Constructs Client LAN (10.99.1.0/24) and Server LAN (10.99.2.0/24) bridged by an intermediate Linux router namespace with IP forwarding enabled. | `./setup.sh` |
| **04** | [Source NAT / Masquerade Gateway](04-nat-gateway/) | Sets up a private host behind a Linux router with iptables SNAT (MASQUERADE) enabled. | `./setup.sh` |
| **05** | [Stateful Firewall Inspection Lab](05-firewall-isolation/) | Constructs a testbed to inspect iptables/nftables stateful connection tracking (conntrack). | `./setup.sh` |
| **06** | [Path MTU Black Hole Simulation](06-mtu-blackhole/) | Simulates path MTU reduction to 1400 bytes with ICMP drop to reproduce PMTUD failure. | `./setup.sh` |
