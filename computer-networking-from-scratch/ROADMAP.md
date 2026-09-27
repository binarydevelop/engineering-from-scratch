# Master Curriculum Roadmap: Phases 00 to 138

> **Motto**: Understand it. Build it. Send it. Capture it. Break it. Trace it. Debug it. Scale it.

The curriculum is structured into 26 cohesive learning blocks spanning 139 focused, hands-on phases. Every single phase combines first-principles theory, runnable code or simulation, live packet capture or kernel inspection, fault injection, and production architecture connections.

---

## Block 0: Networking Lab & Environment Setup
- **Phase 00 — Networking Lab**: Environment verification, network namespaces, interfaces, IP addresses, routing tables, and socket inspection (`ip`, `ss`, `hostname`).

## Block 1: The Physics & Logic of Communication
- **Phase 01 — Why Networks Exist**: Inter-process communication boundaries; why memory sharing fails across machines; deriving messages, mediums, and protocols.
- **Phase 02 — Bits and Bytes on a Link**: Bit rates, byte serialization, bandwidth vs. latency, transmission delay calculation (1 MB over 10 Mbps).
- **Phase 03 — Latency Components**: Processing delay, queueing delay, transmission delay, and propagation delay; connecting formulas to real ping times.
- **Phase 04 — Layers From First Principles**: Why monolithic protocols fail; deriving Link, Internet, Transport, and Application layers; OSI vs. Internet Architecture.
- **Phase 05 — Encapsulation**: Data serialization through header wrapping (HTTP -> TCP -> IP -> Ethernet) and decapsulation simulation.

## Block 2: Host Interfaces, Loopback & Local Delivery
- **Phase 06 — Network Interfaces**: Device drivers, MAC binding, IP assignment, MTU, interface flags (`UP`, `BROADCAST`, `MULTICAST`), `ip link` and `ip addr`.
- **Phase 07 — Loopback**: The `lo` pseudo-interface; `127.0.0.1` and `::1`; why loopback bypasses physical network stacks and how Docker network isolation interacts with it.

## Block 3: Layer 2 — Ethernet, MAC, Switching & Broadcast
- **Phase 08 — Ethernet From First Principles**: Shared local mediums, preamble, source/dest MAC, EtherType, payload, and FCS.
- **Phase 09 — MAC Addresses**: IEEE OUI assignment, hardware burned-in address vs. virtual MACs, why MAC addresses cannot scale globally across the Internet.
- **Phase 10 — Switching**: Layer-2 learning bridge/switch mechanics, MAC address table (`CAM table`), source learning, flooding unknown unicasts, and forwarding.
- **Phase 11 — Broadcast**: Layer-2 broadcast MAC (`ff:ff:ff:ff:ff:ff`), collision domains vs. broadcast domains, why broadcast traffic does not cross routers.

## Block 4: Layer 3 Addressing — IPv4, Subnet Masks & CIDR Calculations
- **Phase 12 — IPv4 Addresses**: 32-bit integer representation, dotted-decimal notation, binary conversion, and network/host boundaries.
- **Phase 13 — Subnet Masks**: Bitwise AND operations, network prefixes, host masks, and prefix length notation (`/24`).
- **Phase 14 — Subnetting**: Calculating subnets for `/8`, `/16`, `/24`, `/30`, `/32`, and arbitrary prefixes (`/20`, `/26`, `/27`); network and broadcast addresses.
- **Phase 15 — Same Subnet or Different Subnet?**: The decision algorithm: direct local delivery via ARP vs. forwarding to the default gateway.

## Block 5: L2/L3 Binding — ARP, Neighbor Discovery & IPv6 Preview
- **Phase 16 — ARP**: Address Resolution Protocol (RFC 826); ARP request broadcast, unicast reply, cache inspection (`ip neigh`), and packet capture.
- **Phase 17 — Neighbor Discovery / IPv6 Preview**: Why IPv6 eliminates ARP in favor of ICMPv6 multicast neighbor solicitations and advertisements.
- **Phase 18 — Build a Tiny ARP Simulator**: Python simulation of ARP cache lookup, miss handling, request flooding, and cache aging.

## Block 6: Layer 3 Routing — Routing Tables, LPM, Routers & Hop Limits
- **Phase 19 — Routing From First Principles**: Multi-hop packet forwarding; routing tables as prefix-to-next-hop lookup tables.
- **Phase 20 — Routing Tables**: Kernel routing inspection (`ip route`), default routes, interface scopes, next-hop gateways, and route metrics.
- **Phase 21 — Longest Prefix Match (LPM)**: The fundamental forwarding rule; resolving overlapping routes with trie-based prefix lookup simulation.
- **Phase 22 — Routers**: Multi-homed hosts, packet forwarding, namespace router lab, and `net.ipv4.ip_forward=1`.
- **Phase 23 — TTL / Hop Limit**: Time-to-Live field; preventing routing loops; observing TTL decrement across multi-hop router paths.

## Block 7: Network Control, ICMP, Path Discovery & MTU
- **Phase 24 — ICMP**: Internet Control Message Protocol (RFC 792); Echo Request/Reply, Destination Unreachable, Time Exceeded, and error headers.
- **Phase 25 — traceroute**: Simulating hop discovery via intentional TTL expiration; incomplete responses, UDP/ICMP variants, and asymmetric paths.
- **Phase 26 — MTU**: Maximum Transmission Unit; 1500-byte Ethernet standard; jumbo frames; measuring path MTU with `ping -M do -s`.
- **Phase 27 — Fragmentation Concepts**: IPv4 `DF`/`MF` flags and fragment offsets; why modern systems avoid IP fragmentation; Path MTU Discovery (PMTUD).

## Block 8: Modern Addressing — IPv6 Architecture & Dual-Stack Realities
- **Phase 28 — IPv6 Fundamentals**: 128-bit addresses, zero-compression notation, prefix lengths, link-local (`fe80::/10`), and global unicast (`2000::/3`).
- **Phase 29 — IPv4 vs IPv6**: Detailed comparison of headers, elimination of broadcast, built-in multicast, router fragmentation prohibition, and dual-stack mechanics.

## Block 9: Layer 4 Transport — Ports, Sockets & UDP
- **Phase 30 — Transport Layer Problem**: Process-to-process multiplexing; why IP alone cannot address concurrent applications.
- **Phase 31 — Ports**: 16-bit port space (0-65535), privileged ports (<1024), registered ports, ephemeral ranges, and socket endpoints (`IP:Port`).
- **Phase 32 — Sockets**: Sockets as OS file descriptor abstractions, kernel socket buffers (`sk_buff`), `socket()`, `bind()`, and `close()`.
- **Phase 33 — UDP From First Principles**: User Datagram Protocol (RFC 768); lightweight datagrams, 8-byte header, stateless semantics, and checksum calculation.
- **Phase 34 — Build UDP Client/Server**: Implementation in Python and C; bidirectional messaging; inspecting source and destination ports via `tcpdump`.
- **Phase 35 — UDP Loss Simulation**: Simulating packet drops, packet reordering, and jitter; implementing application-layer reliability.

## Block 10: Layer 4 Transport — TCP Reliability, Handshakes & Sequence Numbers
- **Phase 36 — Why TCP Exists**: The requirements of reliable ordered byte streams over unreliable packet networks (RFC 9293).
- **Phase 37 — TCP Connection**: The 4-tuple identity (`src_ip`, `src_port`, `dst_ip`, `dst_port`), connection states, and Transmission Control Blocks (TCB).
- **Phase 38 — Three-Way Handshake**: SYN, SYN-ACK, ACK packet exchange; Initial Sequence Number (ISN) negotiation; packet capture analysis.
- **Phase 39 — TCP Sequence Numbers**: Byte-oriented sequence numbering, cumulative acknowledgments, and payload offset tracking.
- **Phase 40 — Retransmission**: Retransmission Timeouts (RTO), duplicate ACKs, Fast Retransmit, and dropped segment recovery simulation.
- **Phase 41 — Sliding Window**: Pipelining vs. stop-and-wait; window sizes; keeping the network pipe full.

## Block 11: Transport Mechanics — Flow Control, Congestion Control & Teardown
- **Phase 42 — Flow Control**: Receiver window (`rcv_wnd`), buffer overflow prevention, zero-window probes, and distinguishing flow control from congestion control.
- **Phase 43 — Congestion**: Bottleneck queues, packet dropping, latency inflation, and the shared tragedy of the commons.
- **Phase 44 — TCP Congestion Control**: Congestion window (`cwnd`), Slow Start, Congestion Avoidance, AIMD, Cubic vs. BBR algorithms.
- **Phase 45 — Bandwidth-Delay Product (BDP)**: Calculating `Bandwidth × RTT`; tuning socket buffers (`SO_SNDBUF`, `SO_RCVBUF`) for high-throughput fat pipes.
- **Phase 46 — TCP Connection Teardown**: Graceful bidirectional termination (`FIN`, `ACK`, `FIN`, `ACK`), half-closed sockets, and `RST` abortive resets.
- **Phase 47 — TIME_WAIT**: Preventing delayed segment collisions, ensuring last ACK delivery, 2*MSL duration, and why disabling TIME_WAIT is dangerous.

## Block 12: Socket Programming & Connection Lifecycle
- **Phase 48 — Connection Refused vs. Timeout**: Distinguishing TCP RST (port closed / daemon down) from silent drops / ICMP unreachables.
- **Phase 49 — TCP Server From Scratch**: Low-level POSIX API: `socket`, `bind`, `listen`, `accept`, `read`, `write`, `close`.
- **Phase 50 — Listening Socket vs. Connected Socket**: The fundamental OS dichotomy: one listening passive socket creating dedicated connected active sockets.
- **Phase 51 — Many TCP Connections**: Handling concurrent connections via non-blocking I/O (`select`, `poll`, `epoll`/`kqueue`).
- **Phase 52 — Ephemeral Ports**: Dynamic port allocation, range inspection (`ip_local_port_range`), and ephemeral port exhaustion scenarios.

## Block 13: Application Layer — Domain Name System (DNS)
- **Phase 53 — DNS Problem**: The failure of static `/etc/hosts` at scale; name-to-address mapping requirements.
- **Phase 54 — DNS Hierarchy**: The global tree: Root (`.`), TLD (`.com`), Second-Level Domain, Subdomains, and authoritative zones.
- **Phase 55 — Recursive Resolver**: Stub resolver (`glibc`), local caching resolver, recursive iterative queries, and root hints.
- **Phase 56 — DNS Record Types**: A, AAAA, CNAME, MX, TXT, NS, PTR, and SRV records; query structure via `dig`.
- **Phase 57 — DNS Caching and TTL**: Time-To-Live expiration, cache poisoning risks, negative caching (SOA TTL), and propagation mechanics.
- **Phase 58 — DNS Debugging**: Diagnosing resolution failures with `dig`, `host`, `nslookup`, and `/etc/resolv.conf`.
- **Phase 59 — Build a Tiny DNS Resolver Experiment**: A Python UDP DNS server supporting A-record queries and in-memory TTL caching.

## Block 14: Application Layer — HTTP/1.1, HTTP/2 & HTTP/3 (QUIC)
- **Phase 60 — HTTP From First Principles**: Plaintext ASCII request/response protocol over raw TCP; manual interaction via `nc`.
- **Phase 61 — HTTP Request/Response**: Request lines, headers, empty line delimiter (`\r\n\r\n`), bodies, and status lines.
- **Phase 62 — HTTP Methods**: GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS; safety and idempotency semantics.
- **Phase 63 — HTTP Status Codes**: 1xx Informational, 2xx Success, 3xx Redirection, 4xx Client Error, 5xx Server Error.
- **Phase 64 — HTTP Keep-Alive**: Persistent connections (`Connection: keep-alive`), reusing TCP handshakes, and measuring latency reductions.
- **Phase 65 — HTTP/1.1 Limitations**: Head-of-line blocking at the application layer, pipelining failure, header duplication overhead.
- **Phase 66 — HTTP/2 Concepts**: Binary framing, multiplexed streams over a single TCP connection, HPACK header compression.
- **Phase 67 — HTTP/3 / QUIC Concepts**: Replacing TCP with QUIC over UDP; stream multiplexing without transport head-of-line blocking; connection migration.

## Block 15: Transport Security — Cryptography, TLS 1.3 & PKI
- **Phase 68 — TLS Problem**: Eavesdropping, tampering, and impersonation on open networks; confidentiality, integrity, authentication.
- **Phase 69 — Cryptography Prerequisites**: Symmetric encryption (AES-GCM), asymmetric key exchange (ECDHE), cryptographic hashes (SHA-256), and digital signatures.
- **Phase 70 — TLS Handshake**: TLS 1.3 1-RTT handshake (ClientHello, ServerHello, EncryptedExtensions, Certificate, Finished); comparing with TLS 1.2.
- **Phase 71 — Certificates**: X.509 structure, Subject Alternative Names (SAN), public keys, signature algorithms, and inspection with `openssl s_client`.
- **Phase 72 — Certificate Validation**: Chain of trust, root Certificate Authorities (CAs), intermediate CAs, hostname verification, and revocation (CRL/OCSP).
- **Phase 73 — HTTPS Request Trace**: Complete integrated trace: DNS resolution -> TCP handshake -> TLS handshake -> HTTP request -> response.

## Block 16: Middleboxes — NAT, PAT & RFC1918 Translation
- **Phase 74 — NAT From First Principles**: IPv4 address depletion; translating private IP addresses to routable public IP addresses.
- **Phase 75 — Private vs. Public IP**: RFC 1918 private subnets (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`), Carrier-Grade NAT (RFC 6598 `100.64.0.0/10`), and why private IPs are not inherently secure.
- **Phase 76 — Source NAT (SNAT)**: Masquerading outbound connections, rewriting source IP/port in the Linux conntrack table.
- **Phase 77 — Destination NAT (DNAT)**: Port forwarding; redirecting external traffic to internal private services.
- **Phase 78 — NAT Limitations**: Inbound reachability hurdles, connection state table exhaustion, STUN/TURN traversal requirements.

## Block 17: Network Security Boundaries — Firewalls, iptables & nftables
- **Phase 79 — Firewalls From First Principles**: Packet filtering based on 5-tuple (`src_ip`, `dst_ip`, `proto`, `src_port`, `dst_port`); default deny policies.
- **Phase 80 — Stateful vs. Stateless Filtering**: Connection tracking (`conntrack`), tracking states (`NEW`, `ESTABLISHED`, `RELATED`, `INVALID`), and stateful return rules.
- **Phase 81 — nftables / Firewall Tooling**: Modern Linux packet filtering tables, chains, hooks (`prerouting`, `input`, `forward`, `output`), and rules.
- **Phase 82 — Network Policies & Security Groups**: Conceptual mapping between Linux firewalls, AWS Security Groups (stateful), NACLs (stateless), and Kubernetes NetworkPolicies.

## Block 18: Application Delivery — Proxies, Reverse Proxies & Load Balancing
- **Phase 83 — Proxy From First Principles**: Intermediary process terminating client connections and initiating separate backend connections.
- **Phase 84 — Forward Proxy**: Client-side proxying, caching, corporate egress control, and the HTTP `CONNECT` tunneling method.
- **Phase 85 — Reverse Proxy**: Server-side abstraction, SSL/TLS termination, request routing, header injection (`X-Forwarded-For`).
- **Phase 86 — Load Balancing**: Distributing requests across backend pools; Round Robin, Weighted Round Robin, and IP Hash.
- **Phase 87 — Layer 4 vs. Layer 7 Load Balancing**: Transport-level TCP stream proxying (AWS NLB) vs. application-aware HTTP routing (AWS ALB).
- **Phase 88 — Health Checks**: Active synthetic probes vs. passive failure detection; circuit breaking unhealthy backends.
- **Phase 89 — Connection Pooling**: Amortizing TCP/TLS handshake overhead between reverse proxies and upstream application servers.
- **Phase 90 — Keepalive at Different Layers**: Distinguishing HTTP persistent connections, TCP keepalive probes (`SO_KEEPALIVE`), and application-level heartbeats.

## Block 19: Practical Linux Networking — Namespaces, veth & Bridges
- **Phase 91 — Network Namespaces**: Operating system network stack virtualization; creating isolated routing tables, interfaces, and socket spaces (`ip netns`).
- **Phase 92 — Virtual Ethernet (veth) Pairs**: Point-to-point virtual network pipes linking namespaces together.
- **Phase 93 — Linux Bridge**: Software L2 switch (`ip link add type bridge`), connecting multiple namespaces into a shared broadcast domain.
- **Phase 94 — Router With Network Namespaces**: Constructing an isolated 3-node routed network (Client <-> Router <-> Server) with static routes.
- **Phase 95 — Build a Tiny Internet**: Multi-network synthetic topology with distinct LANs, intermediate transit network, DNS, and HTTP endpoints.

## Block 20: Packet Inspection & Deep Wire Dissection
- **Phase 96 — tcpdump**: Command-line packet capture flags (`-i`, `-n`, `-nn`, `-s0`, `-vvv`, `-w`), interface selection, and capture buffer management.
- **Phase 97 — Reading Packet Captures**: Berkeley Packet Filter (BPF) syntax; filtering by host, network, port, protocol, and TCP flags (`tcp[tcpflags] & tcp-syn != 0`).
- **Phase 98 — Wireshark Optional Track**: Graphical stream inspection, Protocol Hierarchy Statistics, Follow TCP Stream, and I/O graphs.
- **Phase 99 — Packet Debugging Methodology**: The 4-question packet hypothesis: Did it leave sender? Did it arrive at receiver? Did receiver respond? Did reply return?

## Block 21: Network Performance, Queueing & Traffic Control
- **Phase 100 — Network Performance**: Formalizing bandwidth, goodput, throughput, RTT, jitter, and packet loss rate.
- **Phase 101 — Measuring Latency**: High-resolution latency profiling with ping, curl connect timers, and socket-level timestamps.
- **Phase 102 — Throughput**: Measuring saturating capacity using `iperf3` and custom Python streaming benchmarks across local links.
- **Phase 103 — Packet Loss**: Simulating controlled loss rates using Linux Traffic Control (`tc netem loss`); measuring TCP throughput degradation.
- **Phase 104 — Delay and Jitter**: Simulating variable latency and packet reordering (`tc netem delay 50ms 10ms`); impact on audio/video vs. bulk transfer.
- **Phase 105 — Bandwidth Limits**: Token bucket algorithm simulation; throttling link capacity (`tc qdisc tbf`) and observing bottleneck pacing.
- **Phase 106 — Queueing**: M/M/1 queue simulation; mathematical proof of explosive latency growth as utilization approaches 100%.
- **Phase 107 — Bufferbloat Concept**: Excessive unmanaged buffering in switches/routers causing severe RTT spikes; CoDel and FQ-CoDel solutions.

## Block 22: Reliability, Failure Modes & Distributed Systems Reality
- **Phase 108 — Retries and Timeouts**: The danger of static timeouts; deadline propagation, cascading failure, and client retry storms.
- **Phase 109 — Exponential Backoff**: Mitigating thundering herds; calculating exponential backoff with full jitter simulation.
- **Phase 110 — Idempotency and Network Retries**: The Two Generals Problem; why network unreliability causes duplicated business transactions without idempotency keys.
- **Phase 111 — Partial Failure**: The distributed systems reality: nodes can be healthy while the network drops packets symmetrically or asymmetrically.
- **Phase 112 — Split-Brain Concept**: Network partitioning; cluster quorum loss;CAP theorem trade-offs at the physical network layer.

## Block 23: Hands-On Failure Injection & Broken Networks
- **Phase 113 — DNS Failure Lab**: Diagnosing NXDOMAIN, SERVFAIL, and resolver timeouts in an isolated namespace.
- **Phase 114 — Routing Failure Lab**: Missing default gateway, asymmetric routing drop, and routing loop diagnostics.
- **Phase 115 — Firewall Failure Lab**: Diagnosing silent packet drops vs. administrative TCP RST rejection.
- **Phase 116 — Wrong Port Lab**: Diagnosing port mismatches and validating listening sockets with `ss -tulpn`.
- **Phase 117 — Bind Address Failure**: The classic production trap: service bound to `127.0.0.1` failing remote clients; binding to `0.0.0.0`.
- **Phase 118 — MTU Failure Lab**: Path MTU black hole; large HTTP/TLS payloads dropping silently while ping succeeds.
- **Phase 119 — Broken Network Labs**: 32 comprehensive, symptom-driven debugging scenarios across all layers (symptoms first, solutions separate).
- **Phase 120 — Network Troubleshooting Framework**: The universal 14-step systematic isolation playbook for production incidents.

## Block 24: Capstone Engineering Projects
- **Phase 121 — Project: Raw TCP Chat**: Multi-user client/server chat protocol over raw POSIX sockets.
- **Phase 122 — Project: HTTP Server**: Clean HTTP/1.1 web server from scratch with request routing, header parsing, and Keep-Alive.
- **Phase 123 — Project: DNS-Like Resolver**: Recursive in-memory DNS server handling A-record resolution, caching, and TTL expiry.
- **Phase 124 — Project: Router Simulator**: Trie-based longest prefix match IPv4 forwarding engine with TTL decrement and checksum validation.
- **Phase 125 — Project: Reliable Transport Simulator**: Full Go-Back-N / Selective Repeat protocol over UDP with packet loss, sliding windows, and timeouts.
- **Phase 126 — Project: Reverse Proxy**: Multi-backend HTTP reverse proxy with SSL termination, connection pooling, and header enrichment.
- **Phase 127 — Project: Load Balancer**: High-performance L7 load balancer supporting Round-Robin, Least Connections, and active background health checks.
- **Phase 128 — Project: Tiny Internet**: Complete multi-hop virtual topology with isolated LANs, static routing, NAT gateway, DNS, and web servers.
- **Phase 129 — Project: Production-Like Web Path**: End-to-end multi-tier microservice architecture: Client -> Edge Reverse Proxy -> Load Balancer -> Service A/B -> Redis/DB.

## Block 25: Cloud, Container & System Design Networking
- **Phase 130 — Networking and Docker**: Container network namespaces, Docker bridge (`docker0`), veth pairs, iptables NAT masquerading, and port publishing.
- **Phase 131 — Networking and Kubernetes**: Pod networking model, Container Network Interface (CNI), ClusterIP kube-proxy iptables/IPVS translation, and NodePort.
- **Phase 132 — Networking and AWS**: Mapping physical networking to cloud abstractions: VPCs, CIDR subnets, Route Tables, Internet Gateways, NAT Gateways, Security Groups, and NACLs.
- **Phase 133 — Networking and Databases**: TCP connection cost, connection pooling (PgBouncer), query latency over high-RTT links, and replication lag.
- **Phase 134 — Networking and Redis**: Single-threaded event loop, RESP protocol framing, TCP round-trip latency, and pipelining throughput optimization.
- **Phase 135 — Networking and Kafka**: Sequential disk I/O to network socket transfer via `sendfile` (zero-copy), batching, compression, and network saturation.
- **Phase 136 — Networking and Distributed Systems**: Why network calls are fundamentally different from local procedure calls; latency budgets, jitter, and fallacies of distributed computing.
- **Phase 137 — Networking in System Design**: Network budgeting in architecture interviews: estimating bandwidth, latency constraints, connection concurrency, and failover topologies.
- **Phase 138 — Final Mental Model**: Tracing `curl https://example.com/api` through all 14 layers of reality from process syscall to optical wire and back.
