# The Learning Methodology

> **Motto**: Understand it. Build it. Send it. Capture it. Break it. Trace it. Debug it. Scale it.

Computer networking is often taught backwards: learners are inundated with the 7-layer OSI model, hundreds of acronyms (ARP, BGP, CIDR, DNS, ICMP, MTU, NAT), and RFC specs before they ever understand why two processes on separate computers need a packet in the first place.

In this repository, we teach **mechanics first, protocols second, and tools as the lens into reality**.

---

## 1. The Core Scientific Feedback Loop

Do not passively read code or execute shell scripts without engaging your predictive faculties. Every lesson follows this loop:

```text
               ┌──────────────────────────────────────────────┐
               │                  1. PROBLEM                  │
               │   Process A cannot exchange state with B     │
               └──────────────────────┬───────────────────────┘
                                      │
                                      ▼
               ┌──────────────────────────────────────────────┐
               │           2. PREDICT PACKET PATH             │
               │  Sketch L2/L3/L4 headers before transmitting │
               └──────────────────────┬───────────────────────┘
                                      │
                                      ▼
               ┌──────────────────────────────────────────────┐
               │          3. CONFIGURE LAB (Isolated)         │
               │   Setup namespaces, veth pairs, IPs, routes  │
               └──────────────────────┬───────────────────────┘
                                      │
                                      ▼
               ┌──────────────────────────────────────────────┐
               │            4. SEND & CAPTURE WIRE            │
               │     Run tcpdump on veth interface & send     │
               └──────────────────────┬───────────────────────┘
                                      │
                                      ▼
               ┌──────────────────────────────────────────────┐
               │            5. INSPECT & MEASURE              │
               │    Correlate tcpdump frames with ss / ip     │
               └──────────────────────┬───────────────────────┘
                                      │
                                      ▼
               ┌──────────────────────────────────────────────┐
               │            6. BREAK ONE LAYER SAFELY         │
               │    Drop ARP, alter MTU, close port, bad IP   │
               └──────────────────────┬───────────────────────┘
                                      │
                                      ▼
               ┌──────────────────────────────────────────────┐
               │            7. TRACE & IDENTIFY LAYER         │
               │  Did it fail at L2, L3, L4, or L7? Why?      │
               └──────────────────────┬───────────────────────┘
                                      │
                                      ▼
               ┌──────────────────────────────────────────────┐
               │            8. RESTORE & RECORD EVIDENCE      │
               │    Repair state and document empirical proof │
               └──────────────────────────────────────────────┘
```

---

## 2. The 12 Golden Habits of Master Networkers

1. **Always draw the physical and logical path**: If you cannot sketch every intermediate hop (interface, bridge, router, NAT gateway, firewall) between sender and receiver, you do not understand the connection.
2. **Predict before capturing**: Never launch `tcpdump` without already knowing what frames, flags (SYN, ACK, FIN, RST), and IP addresses you expect to observe.
3. **Calculate subnets manually**: Do not rely on online CIDR calculators during training. Calculate binary network prefixes, host masks, and broadcast boundaries by hand until it is second nature.
4. **Inspect routing tables before sending**: When a connection stalls, run `ip route get <dest_ip>`. Confirm which interface and next-hop gateway the kernel selected.
5. **Inspect listening sockets and bind addresses**: Never assume a port is open. Run `ss -tulpn` or `lsof -i`. Distinguish `127.0.0.1` (loopback only) from `0.0.0.0` (all interfaces) and `::` (IPv6 all).
6. **Never treat `ping` as complete diagnosis**: An ICMP echo request proves only Layer-3 IP reachability. It tells you nothing about whether a firewall drops Layer-4 TCP port 443, whether an HTTP service is overloaded, or whether TLS validation succeeded.
7. **Dissect failures layer by layer**:
   - `name does not resolve` -> **Layer 7 (DNS)**
   - `network is unreachable` -> **Layer 3 (Routing / Missing Gateway)**
   - `destination host unreachable` -> **Layer 2 (ARP resolution failed)**
   - `connection refused` -> **Layer 4 (TCP RST: host reachable, nothing listening on port)**
   - `connection timed out` -> **Layer 3/4 (Silent packet drop: firewall / blackhole route)**
   - `SSL/TLS handshake failure` -> **Layer 5/6 (Certificate mismatch / cipher negotiation)**
   - `HTTP 502 / 504` -> **Layer 7 (Reverse proxy / backend timeout)**
8. **Measure latency before guessing**: Break latency into its 4 physical components: processing delay, queueing delay, transmission delay, and propagation delay.
9. **Break only one variable at a time**: In failure labs, isolate your hypothesis. Do not change the routing table, firewall, and DNS configuration simultaneously.
10. **Rebuild network topologies from memory**: Test yourself by deleting an isolated lab (`./scripts/destroy-network-lab.sh`) and rebuilding the entire two-router multi-subnet network from scratch with pure `ip` commands.
11. **Explain every packet hop to a peer**: Can you trace an HTTP GET request from socket `send()` down through TCP segment segmentation, IP packet routing, Ethernet frame encapsulation, bridge forwarding, router decapsulation, and back up the remote kernel stack?
12. **Record empirical evidence**: Maintain a lab notebook using `outputs/evidence-template.md`. Real engineering is founded on reproducible measurements.

---

## 3. The 12-Point Completion Rule

A lesson or lab is **NOT** complete merely because a script ran with exit code 0. You have only mastered a concept when you can satisfy all 12 points:

1. [ ] **Explain the problem**: Articulate why the protocol or mechanism is needed from first principles.
2. [ ] **Predict packet behavior**: State the exact sequence of wire frames expected.
3. [ ] **Run the experiment**: Execute the synthetic test or socket program.
4. [ ] **Inspect the state**: Validate interfaces (`ip link`), addresses (`ip addr`), routes (`ip route`), and sockets (`ss`).
5. [ ] **Capture on the wire**: Record traffic with `tcpdump` or Wireshark.
6. [ ] **Dissect the capture**: Explain the meaning of every header field and flag observed.
7. [ ] **Intentionally break it**: Safely inject a failure into an isolated namespace.
8. [ ] **Identify the failing layer**: Pinpoint whether Layer 2, Layer 3, Layer 4, or Layer 7 failed without guessing.
9. [ ] **Systematically repair it**: Restore configuration and verify recovery.
10. [ ] **Measure performance**: Record latency, packet count, or socket buffer behavior.
11. [ ] **Differentiate environments**: Explain what changes across host, Docker, Kubernetes, and AWS cloud VPC.
12. [ ] **Document evidence**: Record the full trace in `outputs/evidence-template.md`.
