# Project 04: IPv4 Router & Forwarding Simulator

> **Motto**: A router does not send packets to destination IPs; it decapsulates the link layer, consults a routing table for the next hop, rewrites the link-layer MAC headers, decrements TTL, and forwards the packet out the selected interface.

---

## 1. Overview
In this project, you construct a complete Layer-3 packet forwarder. It implements the Longest Prefix Match (LPM) algorithm across multiple virtual interfaces, resolves next-hop MAC addresses via an ARP neighbor table, validates and decrements TTL, and updates the IPv4 header checksum.

## 2. Forwarding Pipeline
```text
Ingress Frame (eth0)
  │
  ├─ 1. Decapsulate Ethernet II (Verify EtherType 0x0800)
  ├─ 2. Check TTL: If TTL <= 1, drop -> ICMP Time Exceeded
  ├─ 3. Longest Prefix Match on Destination IP -> Select Egress Interface & Next-Hop
  ├─ 4. Lookup Next-Hop IP in ARP Cache -> Obtain Next-Hop MAC
  ├─ 5. Decrement TTL by 1 & Recalculate IPv4 Checksum
  └─ 6. Re-encapsulate with (Router Egress MAC -> Next-Hop MAC)
  │
Egress Frame (eth1)
```

## 3. Running & Testing
```bash
python3 router.py
python3 test_router.py
```
