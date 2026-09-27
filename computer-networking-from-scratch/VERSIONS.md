# Protocol Specifications, RFC Standards & Tooling Baselines

> **Protocol-Version Discipline**: In computer networking, clarity on protocol versions, Request for Comments (RFC) standards, operating system kernel behaviors, and common operational conventions is essential. We never treat obsolete specifications as modern defaults without explicitly identifying their historical status.

---

## 1. Core Internet Protocol Standards (IETF RFCs)

| Layer | Protocol | Standard RFC | Key Concepts & Historical Notes |
| :--- | :--- | :--- | :--- |
| **Link (L2)** | **Ethernet II / IEEE 802.3** | IEEE 802.3-2022 / RFC 894 | 48-bit MAC addresses, 1500-byte default MTU, DIX Ethernet framing vs 802.3 LLC/SNAP. |
| **Link / IP** | **ARP (IPv4)** | [RFC 826](https://www.rfc-editor.org/rfc/rfc826) | Address Resolution Protocol. IPv4 only. Dynamic broadcast query, unicast reply, ARP cache. |
| **Link / IP** | **NDP (IPv6)** | [RFC 4861](https://www.rfc-editor.org/rfc/rfc4861) | Neighbor Discovery Protocol. Replaces ARP in IPv6 using ICMPv6 multicast solicitation & advertisement. |
| **Internet (L3)** | **IPv4** | [RFC 791](https://www.rfc-editor.org/rfc/rfc791), [RFC 4632](https://www.rfc-editor.org/rfc/rfc4632) | 32-bit addresses, Classless Inter-Domain Routing (CIDR), header checksum, TTL, fragmentation flags. |
| **Internet (L3)** | **IPv6** | [RFC 8200](https://www.rfc-editor.org/rfc/rfc8200) | 128-bit addresses, fixed 40-byte base header, Hop Limit replaces TTL, router fragmentation prohibited. |
| **Internet (L3)** | **ICMPv4** | [RFC 792](https://www.rfc-editor.org/rfc/rfc792) | Internet Control Message Protocol: Echo Request/Reply (Type 8/0), Destination Unreachable (Type 3), Time Exceeded (Type 11). |
| **Internet (L3)** | **ICMPv6** | [RFC 4443](https://www.rfc-editor.org/rfc/rfc4443) | Integrated control and neighbor discovery protocol for IPv6. |
| **Transport (L4)** | **UDP** | [RFC 768](https://www.rfc-editor.org/rfc/rfc768) | User Datagram Protocol. 8-byte fixed header, connectionless, unreliable, message-boundary preserving. |
| **Transport (L4)** | **TCP** | [RFC 9293](https://www.rfc-editor.org/rfc/rfc9293) | Transmission Control Protocol (supersedes RFC 793). Connection-oriented, stream-oriented, 3-way handshake, sequence numbers, sliding window, flow & congestion control. |
| **Transport (L4)** | **QUIC** | [RFC 9000](https://www.rfc-editor.org/rfc/rfc9000) | Multiplexed transport protocol built on top of UDP with integrated TLS 1.3 encryption. |
| **Application (L7)**| **DNS** | [RFC 1034](https://www.rfc-editor.org/rfc/rfc1034), [RFC 1035](https://www.rfc-editor.org/rfc/rfc1035), [RFC 6891](https://www.rfc-editor.org/rfc/rfc6891) | Domain Name System. Hierarchical distributed database, resource records (A, AAAA, CNAME, PTR, MX, TXT), EDNS(0). |
| **Application (L7)**| **HTTP/1.1** | [RFC 9112](https://www.rfc-editor.org/rfc/rfc9112) | Textual request/response protocol, persistent connections (Keep-Alive), chunked transfer encoding. |
| **Application (L7)**| **HTTP/2** | [RFC 9113](https://www.rfc-editor.org/rfc/rfc9113) | Binary framing, multiplexed streams over single TCP connection, HPACK header compression. |
| **Application (L7)**| **HTTP/3** | [RFC 9114](https://www.rfc-editor.org/rfc/rfc9114) | HTTP semantics mapped onto QUIC transport, eliminating TCP head-of-line blocking. |
| **Security / L5** | **TLS 1.2** | [RFC 5246](https://www.rfc-editor.org/rfc/rfc5246) | Transport Layer Security (2-RTT handshake, RSA/DHE key exchange, deprecated cipher suites). |
| **Security / L5** | **TLS 1.3** | [RFC 8446](https://www.rfc-editor.org/rfc/rfc8446) | Modern TLS standard (1-RTT handshake, mandatory forward secrecy via (EC)DHE, removal of obsolete crypto). |
| **Addressing** | **Private IPv4** | [RFC 1918](https://www.rfc-editor.org/rfc/rfc1918) | Non-routable private ranges: `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`. |
| **Addressing** | **Test IPv4** | [RFC 5737](https://www.rfc-editor.org/rfc/rfc5737) | Documentation & lab prefixes: `192.0.2.0/24` (TEST-NET-1), `198.51.100.0/24`, `203.0.113.0/24`. |

---

## 2. Specification vs. Implementation vs. Operational Convention

We strictly maintain the following tripartite distinction throughout the course:

```text
┌───────────────────────────────────────────────────────────────────────────┐
│ 1. PROTOCOL SPECIFICATION (IETF RFC)                                      │
│    What the standard formally demands (e.g. TCP checksum calculation,     │
│    sequence number wraparound, three-way handshake state machine).        │
├───────────────────────────────────────────────────────────────────────────┤
│ 2. LINUX KERNEL IMPLEMENTATION                                            │
│    How the Linux kernel actually behaves (e.g., cubic/bbr congestion      │
│    control algorithms, SO_REUSEADDR/SO_REUSEPORT socket flags, TCP syncookies,│
│    ephemeral port selection from /proc/sys/net/ipv4/ip_local_port_range). │
├───────────────────────────────────────────────────────────────────────────┤
│ 3. COMMON OPERATIONAL CONVENTION                                          │
│    Practices adopted in production infrastructure (e.g., standard HTTP    │
│    ports 80/443, reverse proxy load balancer routing, /24 subnetting,     │
│    cloud security group default-deny policies).                           │
└───────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Tooling and Runtime Baselines

All exercises and scripts are verified against the following toolchain:

| Tool | Recommended Linux Baseline | Verification Command | Purpose |
| :--- | :--- | :--- | :--- |
| **Linux Kernel** | >= 5.15 LTS (6.x preferred) | `uname -r` | Network namespaces, veth pairs, nftables, eBPF, TCP stack. |
| **iproute2 (`ip`)** | >= 5.15 | `ip -V` | Interface configuration, routing tables, neighbor table, namespaces. |
| **iproute2 (`ss`)** | >= 5.15 | `ss -v` | Socket statistics, socket buffer inspection, TCP state introspection. |
| **tcpdump** | >= 4.99 (libpcap >= 1.10) | `tcpdump --version` | Packet capture, raw packet dissection, pcap creation. |
| **iptables** | >= 1.8.7 (legacy/nft) | `iptables --version` | Stateful packet filtering, NAT, connection tracking. |
| **nftables** | >= 1.0.0 | `nft --version` | Modern Linux packet classification and firewall framework. |
| **bind9-dnsutils (`dig`)**| >= 9.18 | `dig -v` | DNS queries, TTL inspection, DNS trace. |
| **curl** | >= 7.81 | `curl --version` | HTTP/1.1, HTTP/2, HTTP/3, TLS inspection, connection timing. |
| **netcat (`nc`)** | OpenBSD or traditional | `nc -h` | Raw TCP/UDP socket probing. |
| **Python** | >= 3.10 (3.11, 3.12, 3.14 tested) | `python3 --version` | All protocol simulations, educational servers, and benchmark suites. |
| **GCC / Clang** | >= 11.0 / LLVM 14.0 | `gcc --version` | Low-level C socket programming track. |
| **Docker** | >= 24.0 (Docker Desktop / CE) | `docker --version` | Cross-platform containerized Linux networking lab. |
