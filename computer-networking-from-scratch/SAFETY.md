# Network Experimentation Safety Rules

> **Core Philosophy**: A networking engineer must be able to break things completely to understand them, but **must never break their own connectivity, damage upstream networks, or snoop on unauthorized traffic**.

This document outlines mandatory safety guidelines and operational discipline for running the exercises, labs, simulations, and broken-network scenarios in `computer-networking-from-scratch`.

---

## 1. Golden Rule of Network Isolation

**NEVER modify the default routing table, host firewall, or physical network interfaces of your primary machine (laptop, desktop, or cloud bastion).**

All stateful firewall rules, routing mutations, ARP spoofing experiments, MTU drops, and NAT translation tests must occur inside:
1. **Linux Network Namespaces** (`ip netns`)
2. **Isolated Docker testbed containers**
3. **Disposable Linux Virtual Machines** (e.g., Vagrant, Multipass, QEMU/KVM)

---

## 2. Domain-Specific Safety Protocols

### A. Firewall Experiments (`iptables` / `nftables`)
* **Never flush the host firewall**: Do not execute `iptables -F` or `nftables flush ruleset` in the default host namespace. You may disconnect your SSH session or disable system security controls.
* **Namespace Isolation**: Execute firewall commands exclusively within an isolated network namespace:
  ```bash
  sudo ip netns exec <ns-name> iptables -A INPUT -p tcp --dport 80 -j DROP
  ```
* **Disposal**: When finished, delete the namespace with `ip netns del <ns-name>` to purge all related firewall chains and tables automatically.

### B. Routing and Gateway Modifications (`ip route`)
* **Host Default Route Protection**: Never execute `ip route del default` on your host. If you delete your host's default route, you will lose Internet connectivity and SSH access immediately.
* **Targeted Prefixes**: In namespace labs, configure routes only for private synthetic prefixes (e.g., `10.99.0.0/24`, `172.31.0.0/24`, `192.0.2.0/24` [RFC 5737 TEST-NET-1]).
* **Verification Before Teardown**: Always run the automated teardown scripts (`scripts/destroy-network-lab.sh`) to ensure virtual interfaces and temporary routes are cleanly unmounted.

### C. Interfaces and Virtual Ethernet (`ip link` / `veth`)
* **Never down the primary NIC**: Never run `ip link set dev eth0 down` or `ip link set dev en0 down`.
* **Virtual Ethernet Pairs**: Always create linked pairs (`veth0` <--> `veth1`) and immediately assign one or both ends to network namespaces:
  ```bash
  sudo ip link add veth-client type veth peer name veth-router
  sudo ip link set veth-client netns ns-client
  sudo ip link set veth-router netns ns-router
  ```

### D. Packet Captures and Promiscuous Mode (`tcpdump` / Wireshark)
* **Authorized Interfaces Only**: Capture packets strictly on virtual interfaces (`veth*`, `br0`, `lo`, or inside `ip netns`).
* **No Wiretapping**: Do not capture unencrypted traffic on shared enterprise, school, or public Wi-Fi networks.
* **Sanitize Captures**: When submitting evidence or logs, verify that no personal auth tokens, private API keys, or sensitive cookies are contained in the `.pcap` files.

### E. Raw Sockets and Packet Injection
* **Unprivileged Fallbacks**: Python and C socket programs in this course prioritize standard unprivileged POSIX sockets (`AF_INET`, `SOCK_STREAM`, `SOCK_DGRAM`).
* **CAP_NET_RAW Caution**: Raw socket injection (`SOCK_RAW`) requires root privileges (`sudo` or `CAP_NET_RAW`). Confine raw socket experiments to synthetic test networks. Do not inject malformed headers onto external gateways.

### F. IP Forwarding (`sysctl net.ipv4.ip_forward`)
* **Namespace Scoping**: Enable IP forwarding per-namespace only:
  ```bash
  sudo ip netns exec ns-router sysctl -w net.ipv4.ip_forward=1
  ```
  Do not turn your development machine into an open router for external traffic.

### G. Network Address Translation (NAT / Masquerading)
* **Explicit Subnets**: When testing SNAT (`MASQUERADE`) or DNAT (port forwarding), strictly bind the match rules to the test subnet and interface:
  ```bash
  sudo ip netns exec ns-router iptables -t nat -A POSTROUTING -s 10.99.1.0/24 -o veth-wan -j MASQUERADE
  ```
  Never set an open masquerade rule on `eth0` or your home Wi-Fi adapter.

---

## 3. Platform Matrix & Containment Modes

| Platform | Primary Strategy | Fallback / Containment |
| :--- | :--- | :--- |
| **Linux (Bare Metal / VM)** | Native `ip netns`, `veth`, `iptables`/`nftables` | Disposable namespaces |
| **macOS (Darwin)** | Cross-platform Python & C simulators natively | Docker Desktop container running Linux namespaces |
| **Windows (WSL2)** | Native WSL2 Linux kernel with `ip netns` support | Docker or Hyper-V Ubuntu VM |

---

## 4. Emergency Recovery Procedures

If you accidentally misconfigure something on your local environment:
1. **Network Lab Reset**:
   ```bash
   sudo ./scripts/reset-lab.sh
   ```
2. **Flush Namespace Residue**:
   ```bash
   sudo ip -all netns delete
   ```
3. **Check Host Interfaces & Routes**:
   ```bash
   ip route show
   ip addr show
   ```
4. **Restart Network Manager (Linux host only if affected)**:
   ```bash
   sudo systemctl restart NetworkManager # or systemd-networkd
   ```
