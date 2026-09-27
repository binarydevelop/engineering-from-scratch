# computer-networking-from-scratch

> **Understand it. Build it. Send it. Capture it. Break it. Trace it. Debug it. Scale it.**

An experimental, first-principles curriculum that transforms computer networking from a collection of abstract protocol acronyms and certification trivia into a transparent, mechanical set of operating system, packet, and distributed system realities.

---

## What This Repository Is

This is **NOT** a networking certification cram guide.  
This is **NOT** a vendor router CLI configuration manual.  
This is a course in **understanding how machines actually communicate**.

When most software engineers encounter a network failure, their instincts look like this:

```text
               THE CARGO-CULT INSTINCT (Guessing)
   ┌────────────────────────────────────────────────────────┐
   │  "API is unreachable"       ──> curl -k in a loop      │
   │  "Port already in use"      ──> reboot the machine     │
   │  "Connection refused"       ──> disable the firewall   │
   │  "Slow response times"      ──> increase server RAM    │
   │  "Docker container fails"   ──> bind to --net=host     │
   │  "DNS lookup fails"         ──> hardcode IP in hosts   │
   └────────────────────────────────────────────────────────┘
```

This repository replaces blind guessing with an accurate, mechanical mental model:

```text
               THE FIRST-PRINCIPLES REALITY
   ┌────────────────────────────────────────────────────────┐
   │                   APPLICATION PROCESS                  │
   │           curl / python / nginx / redis / app          │
   ├────────────────────────────────────────────────────────┤
   │                  POSIX SOCKET LAYER                    │
   │          File Descriptors, Buffers, Syscalls           │
   ├────────────────────────────────────────────────────────┤
   │                  TRANSPORT LAYER (L4)                  │
   │       TCP (State Machine, Congestion, Seq/Ack)         │
   │       UDP (Datagrams) / QUIC                           │
   ├────────────────────────────────────────────────────────┤
   │                   NETWORK LAYER (L3)                   │
   │       IP Addresses, CIDR Subnets, Routing Tables       │
   ├────────────────────────────────────────────────────────┤
   │                 LINK / DATA LINK (L2)                  │
   │       Ethernet Frames, MAC Addresses, ARP / NDP        │
   ├────────────────────────────────────────────────────────┤
   │                   PHYSICAL / DRIVER                    │
   │         Network Interfaces (NIC, veth, lo, tap)        │
   └────────────────────────────────────────────────────────┘
```

Every major concept connects directly to concrete inspection and debugging tools: `ip`, `ss`, `ping`, `traceroute`, `dig`, `curl`, `nc`, `tcpdump`, and `iptables`/`nftables`.

---

## The 9 Core Disciplines

1. **Networking Fundamentals**: Deriving communication boundaries, bitrates, latency components, and layering without memorization.
2. **Practical Linux Networking**: Network namespaces (`ip netns`), virtual ethernet pairs (`veth`), Linux bridges, and loopback mechanics.
3. **Protocol Understanding**: Deep IETF RFC discipline across IPv4, IPv6, ARP, ICMP, UDP, TCP, DNS, HTTP/1.1-3, and TLS 1.3.
4. **Packet-Level Reasoning**: Dissecting raw wire frames with `tcpdump` and Wireshark to verify hypotheses before reading log files.
5. **Socket Programming**: Implementing low-level network clients and multi-threaded/event-driven servers in Python and C.
6. **Network Debugging**: Distinguishing between DNS failures, routing drops, firewall timeouts, closed ports (TCP RST), and TLS handshake aborts.
7. **Performance & Traffic Control**: Measuring latency, throughput, jitter, queueing delay, bufferbloat, and tuning TCP socket buffers.
8. **Security Boundaries**: Packet filtering, stateful connection tracking (`conntrack`), NAT/masquerading, and TLS certificate validation.
9. **System-Design Networking**: Applying network constraints to real-world architectures: Docker CNI, Kubernetes ClusterIP, AWS VPC, Redis pipelining, and Kafka batching.

---

## Curriculum Progression

```text
Bits & Bandwidth (01-05)
         │
         ▼
Interfaces & Loopback (06-07)
         │
         ▼
Ethernet, MAC & Switching (08-11)
         │
         ▼
IPv4 & Subnetting (12-15)
         │
         ▼
ARP & Neighbor Discovery (16-18)
         │
         ▼
Routing Tables & Routers (19-23)
         │
         ▼
ICMP, traceroute & MTU (24-27)
         │
         ▼
IPv6 Fundamentals (28-29)
         │
         ▼
UDP & Socket Programming (30-35)
         │
         ▼
TCP Handshakes, Reliability & Flow Control (36-47)
         │
         ▼
Socket Concurrency & Ephemeral Ports (48-52)
         │
         ▼
DNS Hierarchy & Resolution (53-59)
         │
         ▼
HTTP/1.1, HTTP/2 & HTTP/3 (60-67)
         │
         ▼
TLS 1.3 Cryptography & Certificates (68-73)
         │
         ▼
NAT & Port Forwarding (74-78)
         │
         ▼
Firewalls & nftables (79-82)
         │
         ▼
Proxies & Load Balancing (83-90)
         │
         ▼
Namespaces, Bridges & Linux Routing (91-95)
         │
         ▼
tcpdump & Packet Dissection (96-99)
         │
         ▼
Network Performance & Queueing (100-107)
         │
         ▼
Distributed Systems Reality (108-112)
         │
         ▼
Broken Network Troubleshooting Labs (113-120)
         │
         ▼
Capstone Engineering Projects (121-129)
         │
         ▼
Docker, Kubernetes, AWS & System Design (130-138)
```

---

## Core Visual Mental Models

### 1. Local Subnet Delivery vs. Routed Gateway Delivery

```text
  LOCAL SUBNET DELIVERY (Same /24)         ROUTED GATEWAY DELIVERY (Different Subnet)
  Host A: 10.0.1.10/24                     Host A: 10.0.1.10/24
         │                                        │
         │ Broadcasts ARP:                        │ Resolves Gateway MAC:
         │ "Who has 10.0.1.20?"                   │ "Who has 10.0.1.1 (Gateway)?"
         │                                        ▼
         ▼                                ┌────────────────┐
    ┌──────────┐                          │ Router/Gateway │
    │ Switch   │                          │ 10.0.1.1       │
    └────┬─────┘                          └───────┬────────┘
         │                                        │ Rewrites L2 MACs
         ▼                                        ▼
  Host B: 10.0.1.20/24                     Host C: 10.0.2.50/24
```

### 2. End-to-End Packet Encapsulation & Decapsulation

```text
[ APPLICATION ]       HTTP Payload: "GET /api HTTP/1.1"
      │
      ▼
[ TRANSPORT ]         [ TCP Header | Ports: 54321 -> 443 | Seq: 1000 | SYN/ACK ]
      │
      ▼
[ NETWORK ]           [ IP Header | Src: 192.0.2.10 | Dst: 198.51.100.5 | TTL: 64 ]
      │
      ▼
[ LINK / DATA ]       [ Ethernet Header | Src MAC: AA:.. | Dst MAC: BB:.. | Type: 0x0800 ]
      │
      ▼
[ PHYSICAL WIRE ]     0101010101010100101010101010101010101010101010101010101010101010
```

### 3. The End-to-End Web Request Path (`curl https://example.com/api`)

```text
Process: curl
  │
  ├─ 1. DNS Resolution ──► Stub Resolver ──► Recursive DNS Server ──► A/AAAA Record (93.184.216.34)
  │
  ├─ 2. Route Lookup ────► Kernel checks routing table ──► selects interface eth0, gateway 192.168.1.1
  │
  ├─ 3. L2 ARP Lookup ───► ARP table check ──► Gateway MAC (52:54:00:12:34:56)
  │
  ├─ 4. TCP 3-Way Handshake
  │     Client ──[ SYN ]─────────────────────────────────────────► Server
  │     Client ◄─[ SYN-ACK ]───────────────────────────────────── Server
  │     Client ──[ ACK ]─────────────────────────────────────────► Server
  │
  ├─ 5. TLS 1.3 Handshake
  │     Client ──[ ClientHello + Key Share ]─────────────────────► Server
  │     Client ◄─[ ServerHello + Encrypted Extensions + Cert ]─── Server
  │     Client validates X.509 Certificate Chain of Trust
  │
  ├─ 6. Application Request & Response
  │     Client ──[ Encrypted HTTP GET /api ]────────────────────► Server
  │     Client ◄─[ Encrypted HTTP 200 OK Response ]────────────── Server
  │
  └─ 7. Connection Teardown (or Keep-Alive reuse)
```

---

## Platform Strategy & Safety

* **Primary Platform**: Linux (native Linux, Linux VM, or WSL2).
* **Cross-Platform Simulators**: All simulations (`simulations/`), Python socket programs, and benchmarks execute seamlessly on macOS, Linux, and Windows.
* **Network Namespaces & Containerization**: All destructive firewall (`iptables`/`nftables`), routing mutation, and interface isolation experiments are executed strictly inside disposable network namespaces (`ip netns`) or Docker containers.
* **Safety Rules**: Review [`SAFETY.md`](file:///Users/tushar/Desktop/private/repos/computer-networking-from-scratch/SAFETY.md) before executing privileged commands. Never alter your host's default route or flush your primary firewall.

---

## Repository Structure

```text
computer-networking-from-scratch/
├── README.md                  # Flagship syllabus and system mental models
├── ROADMAP.md                 # Complete 139-phase curriculum breakdown
├── LEARNING.md                # 12-point completion rule & learning feedback loop
├── LESSON_TEMPLATE.md         # Mandatory 19-section structure for every lesson
├── VERSIONS.md                # RFC standards & Linux kernel/tool baselines
├── SAFETY.md                  # Strict network isolation & containment rules
├── CONTRIBUTING.md            # Guidelines for code & lesson contributions
├── Makefile                   # Automation for test execution, labs, and cleanup
│
├── scripts/                   # Core environment and namespace management tools
│   ├── check-environment.sh   # Validates system tools, Python version, and kernel
│   ├── create-network-lab.sh  # Creates isolated multi-namespace routed topology
│   ├── destroy-network-lab.sh # Safely dismantles virtual interfaces and namespaces
│   ├── reset-lab.sh           # Emergency teardown and recovery tool
│   └── run-all-tests.sh       # Executes complete test and validation suite
│
├── phases/                    # 139 structured curriculum lessons (Phases 00 to 138)
├── labs/                      # Reusable lab topologies (veth, bridge, router, NAT)
├── simulations/               # Standalone Python simulators for core protocols
├── socket-programs/           # Low-level socket implementations (Python & C)
├── broken-networks/           # 32 hands-on failure injection & troubleshooting labs
├── packet-captures/           # 20 dissected wire captures with filters & predictions
├── benchmarks/                # Empirical latency, throughput, and connection benchmarks
├── projects/                  # 9 practical capstone engineering implementations
├── docs/                      # Architectural reference guides
│   ├── command-map.md         # Diagnostic commands organized by clinical question
│   ├── glossary.md            # Precise terminology across L2 through L7
│   ├── mental-models.md       # Architectural deep dives & state diagrams
│   ├── protocol-map.md        # Protocol headers, RFC standards, and byte layouts
│   ├── packet-debugging.md    # The 4-question packet hypothesis methodology
│   ├── common-misconceptions.md # Debunking 8+ fatal networking myths
│   └── troubleshooting.md     # The universal 14-step incident isolation framework
└── outputs/
    └── evidence-template.md   # Standard empirical lab report template
```

---

## Quick Start

### 1. Verify Your Environment

```bash
git clone https://github.com/rohitg00/computer-networking-from-scratch.git
cd computer-networking-from-scratch

# Run the environment diagnosis script
./scripts/check-environment.sh
```

### 2. Run All Protocol Simulations & Socket Tests

```bash
make test
```

### 3. Launch an Isolated Linux Namespace Lab

```bash
# Creates 3 isolated namespaces (ns-client, ns-router, ns-server) with veth links
sudo ./scripts/create-network-lab.sh

# Ping through the virtual router
sudo ip netns exec ns-client ping -c 3 10.99.2.10

# Tear down safely
sudo ./scripts/destroy-network-lab.sh
```

---

## Educational Projects Overview

| Project | Description | Core Protocols & Techniques |
| :--- | :--- | :--- |
| **01. Raw TCP Chat** | Multi-client conversational server | POSIX sockets, non-blocking I/O, `select`/`epoll` |
| **02. HTTP/1.1 Server** | Clean web server from scratch | Request parsing, status codes, Keep-Alive |
| **03. DNS-Like Resolver** | In-memory recursive name server | UDP sockets, DNS wire framing, TTL caching |
| **04. Router Simulator** | Longest Prefix Match IPv4 engine | Radix/Trie lookup, TTL decrement, L2 rewrite |
| **05. Reliable Transport** | TCP-like reliability over UDP | Sliding window, Go-Back-N, sequence numbers |
| **06. Reverse Proxy** | HTTP reverse proxy | Connection forwarding, header injection |
| **07. Load Balancer** | Layer-7 proxy with health checks | Round-robin, least connections, circuit breaking |
| **08. Tiny Internet** | Multi-hop routed virtual topology | Namespaces, veth pairs, routing, DNS, HTTP |
| **09. Production Web Path** | End-to-end microservice architecture | Edge proxy -> LB -> App servers -> Datastore |

---

> **Networking is no longer invisible plumbing.**
>
> We started with bits moving between machines, gave interfaces addresses, discovered local neighbors, routed packets across networks, built reliable communication on top of IP, resolved names with DNS, exchanged application messages with HTTP, encrypted them with TLS, and then built proxies, load balancers, NAT, and firewalls around those primitives.
>
> Now when two systems cannot communicate, we can trace the path one layer at a time, inspect the packets, identify where reality diverges from our expectation, and reason toward the root cause.
