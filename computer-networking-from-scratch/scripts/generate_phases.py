#!/usr/bin/env python3
"""
scripts/generate_phases.py
Generates all 139 phase lessons (Phases 00 to 138) strictly conforming to LESSON_TEMPLATE.md
with code/, experiments/, outputs/, and docs/en.md.
"""

import os
import shutil

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PHASES_DIR = os.path.join(REPO_ROOT, "phases")

PHASE_DEFS = [
    (0, "networking-lab", "Networking Lab", "The network is not magic; it is operating system data structures and physical interfaces that can be directly inspected.",
     "Engineers treat networking as an opaque cloud without knowing how to inspect their local host stack.",
     "Running 'ip addr' and 'ss' will reveal local interface IPs and listening sockets.",
     "ip addr, ip link, ip route, ss -tulpn",
     "Host -> NIC -> IP Stack -> Sockets"),

    (1, "why-networks-exist", "Why Networks Exist", "When two processes cannot share physical memory, they must exchange serialized messages over an agreed-upon transmission medium.",
     "Process A cannot read the virtual memory address space of Process B on a remote computer.",
     "Without shared memory, state synchronization requires message serialization and physical signaling.",
     "python3 -c 'import socket; s = socket.socket()'",
     "Process A Memory -> Serialized Bytes -> Physical Medium -> Process B Memory"),

    (2, "bits-and-bytes-on-a-link", "Bits and Bytes on a Link", "Transmission delay is the immutable physical time required to push packet bits onto the wire.",
     "People conflate bandwidth (capacity) with latency (travel time).",
     "Pushing 1 MB over a 10 Mbps link requires exactly 838.86 ms of pure serialization time regardless of distance.",
     "python3 simulations/transmission_delay.py",
     "Bits In Host Memory -> NIC Serializer -> Serial Bitstream On Wire"),

    (3, "latency-components", "Latency Components", "Total latency is the physical sum of processing, queueing, transmission, and propagation delays.",
     "Developers assume upgrading link bandwidth from 1 Gbps to 10 Gbps will fix cross-continental latency.",
     "Speed of light in fiber (~200,000 km/s) creates an irreducible physical round-trip baseline.",
     "python3 simulations/latency_components.py",
     "Total Delay = d_proc + d_queue + d_trans + d_prop"),

    (4, "layers-from-first-principles", "Layers From First Principles", "Layering divides the intractable problem of remote communication into modular, interchangeable contracts.",
     "A single application should not need to manage electrical voltages, routing paths, and packet retransmissions.",
     "Decoupling Link, Internet, Transport, and Application layers allows swapping Ethernet for Wi-Fi without rewriting HTTP.",
     "cat docs/protocol-map.md",
     "Application -> Transport (TCP/UDP) -> Internet (IP) -> Link (Ethernet)"),

    (5, "encapsulation", "Encapsulation", "Headers are envelopes; as data travels down the stack, each layer wraps the payload with its own control metadata.",
     "How do heterogeneous devices process only the information relevant to their architectural layer?",
     "Ethernet switches inspect only the outer L2 MAC frame; routers inspect L3 IP; applications inspect L7 payload.",
     "python3 simulations/encapsulation.py",
     "Payload -> [TCP|Payload] -> [IP|TCP|Payload] -> [Eth|IP|TCP|Payload]"),

    (6, "network-interfaces", "Network Interfaces", "A network interface is the kernel software abstraction binding device drivers to the IP stack.",
     "How does the operating system kernel interact with diverse physical Ethernet cards and virtual devices?",
     "ip link shows interface state, MAC address, and MTU; ip addr shows assigned L3 prefixes.",
     "ip link show && ip addr show",
     "Kernel VFS/Sysfs (/sys/class/net) <-> Driver <-> Network Interface Card"),

    (7, "loopback", "Loopback", "The loopback interface is an internal kernel shortcut: packets to 127.0.0.1 never touch physical hardware.",
     "Why can a client connect to 127.0.0.1 on the host, but fail inside an isolated Docker container?",
     "Loopback traffic is confined strictly to the current network namespace's private socket table.",
     "ping -c 2 127.0.0.1 && ss -tlpn",
     "Process A -> Socket (127.0.0.1) -> Kernel Socket Buffer -> Socket -> Process B"),

    (8, "ethernet-from-first-principles", "Ethernet From First Principles", "Ethernet solves the local multi-access medium problem by framing bits with source/destination MAC addresses and error checks.",
     "When multiple devices share an electrical wire or switch, how does a NIC know which frames are meant for it?",
     "The NIC checks the destination MAC address; if it matches its burned-in address or broadcast, it raises an interrupt.",
     "tcpdump -i eth0 -e -nn",
     "[ Preamble | Dst MAC | Src MAC | EtherType | Payload | FCS ]"),

    (9, "mac-addresses", "MAC Addresses", "MAC addresses identify physical or virtual network interfaces within a single local Layer-2 broadcast domain.",
     "Why can the global Internet not be routed using 48-bit MAC addresses alone?",
     "MAC addresses are topologically flat; without hierarchical prefixes, global switches would require billions of CAM entries.",
     "cat /sys/class/net/eth0/address",
     "[ 24-bit OUI (Vendor) | 24-bit Device Identifier ]"),

    (10, "switching", "Switching", "A Layer-2 switch learns sender MAC addresses dynamically to forward frames directly to target ports without bus collisions.",
     "Hubs flood every packet to all ports; how does a switch partition collision domains?",
     "A switch populates its CAM table from ingress frame source MACs and forwards unicasts directly.",
     "python3 simulations/mac_switch.py",
     "Ingress Frame -> Inspect Src MAC -> Learn (Port, MAC) -> Inspect Dst MAC -> Forward/Flood"),

    (11, "broadcast", "Broadcast", "Layer-2 broadcast sends a frame to every host in the local domain, but is strictly contained by router boundaries.",
     "How does a host discover unknown local neighbors without knowing their physical addresses beforehand?",
     "Frames addressed to ff:ff:ff:ff:ff:ff are delivered to every port on the local switch.",
     "tcpdump -i eth0 -nn ether host ff:ff:ff:ff:ff:ff",
     "Host A Broadcast -> Switch floods to Port 2, Port 3 -> Stopped by Router"),

    (12, "ipv4-addresses", "IPv4 Addresses", "An IPv4 address is an unsigned 32-bit integer formatted as four dotted-decimal octets for human readability.",
     "How do we provide globally routable, hierarchical addresses to billions of interconnected hosts?",
     "32 bits allow up to 4.29 billion distinct addresses divided hierarchically into network and host portions.",
     "python3 -c 'import socket, struct; print(bin(struct.unpack(\"!I\", socket.inet_aton(\"192.168.1.10\"))[0]))'",
     "192.168.1.10 <-> 11000000.10101000.00000001.00001010"),

    (13, "subnet-masks", "Subnet Masks", "A subnet mask is a bitmask of contiguous 1s that splits an IP address into its network prefix and host identifier.",
     "How does a host know where the network portion ends and the host portion begins?",
     "Performing bitwise AND between an IP address and its subnet mask extracts the network address.",
     "ip route show",
     "IP & Netmask = Network Prefix (e.g. 192.168.1.10 & 255.255.255.0 = 192.168.1.0)"),

    (14, "subnetting", "Subnetting", "Subnetting carves contiguous blocks of IP addresses into smaller, independent broadcast domains to conserve addresses.",
     "How do network engineers allocate variable-sized networks (/8, /16, /24, /30, /32) efficiently?",
     "A /30 prefix provides 4 addresses (1 network, 2 usable hosts, 1 broadcast), ideal for point-to-point router links.",
     "python3 -c 'import ipaddress; net = ipaddress.ip_network(\"192.168.1.0/27\"); print(net.num_addresses, list(net.hosts())[0])'",
     "CIDR Prefix Length: /24 (254 hosts), /27 (30 hosts), /30 (2 hosts), /32 (single host)"),

    (15, "same-subnet-or-different-subnet", "Same Subnet or Different Subnet?", "The fundamental routing decision: if destination IP shares the local subnet prefix, deliver directly via ARP; otherwise, send to default gateway.",
     "How does a host decide whether to broadcast an ARP request for the destination or for the router?",
     "The host applies its subnet mask to both local and destination IPs; mismatch triggers gateway forwarding.",
     "ip route get 10.0.1.50 && ip route get 8.8.8.8",
     "Dest in local subnet? YES -> ARP for Dest MAC | NO -> ARP for Gateway MAC"),

    (16, "arp", "ARP", "Address Resolution Protocol bridges the gap between Layer-3 IP addresses and Layer-2 Ethernet MAC addresses.",
     "A host has an IP packet ready to send over Ethernet, but does not know the destination NIC's MAC address.",
     "Host broadcasts 'Who has IP X? Tell IP Y'; owner unicasts its MAC address back, which is cached in the ARP table.",
     "ip neigh show && sudo tcpdump -i eth0 -nn arp",
     "ARP Request (Broadcast ff:ff:..) -> Target Unicast Reply -> Cache Entry in 'ip neigh'"),

    (17, "neighbor-discovery-ipv6-preview", "Neighbor Discovery / IPv6 Preview", "IPv6 eliminates broadcast ARP in favor of ICMPv6 multicast Neighbor Solicitation and Advertisement.",
     "Why was broadcast ARP deemed inefficient on high-speed modern networks?",
     "Broadcast interrupts every NIC on the LAN; IPv6 solicited-node multicast targets only interested nodes.",
     "ip -6 neigh show",
     "IPv6 Node -> ICMPv6 Neighbor Solicitation (Multicast) -> Neighbor Advertisement"),

    (18, "build-a-tiny-arp-simulator", "Build a Tiny ARP Simulator", "Simulate the ARP request-reply cycle and cache management from scratch in code.",
     "Experience how cache misses force queuing or dropping of initial IP packets while waiting for L2 resolution.",
     "A cache miss triggers an ARP request; once the reply arrives, the IP-MAC mapping is saved with a TTL.",
     "python3 simulations/arp_cache.py",
     "IP Packet Ready -> Check ARP Cache -> Miss -> Send ARP Req -> Store Reply -> Send Frame"),

    (19, "routing-from-first-principles", "Routing From First Principles", "Routing is the process of selecting paths across multiple interconnected networks using hop-by-hop forwarding tables.",
     "How do packets traverse the globe across thousands of intermediate networks without any router knowing the entire path?",
     "Routers make local forwarding decisions: each router inspects destination IP and forwards to the next-hop gateway.",
     "ip route show",
     "Host A -> Router 1 -> Router 2 -> Router 3 -> Host B"),

    (20, "routing-tables", "Routing Tables", "A routing table maps destination CIDR prefixes to outgoing interfaces, next-hop gateways, and metric costs.",
     "How does the Linux kernel determine which interface and gateway to use for outbound traffic?",
     "The kernel consults the routing table; routes with lower metrics or more specific masks take precedence.",
     "ip route show && ip route get 1.1.1.1",
     "Kernel Table: [ Prefix | Gateway | Interface | Metric ]"),

    (21, "longest-prefix-match", "Longest Prefix Match", "When multiple routing table entries match a destination IP, the router selects the entry with the longest prefix length.",
     "Given routes 10.0.0.0/8 and 10.1.2.0/24, which route forwards a packet to 10.1.2.50?",
     "10.1.2.0/24 has 24 matching bits, beating /8 (8 bits) and default (0 bits); it is selected unconditionally.",
     "python3 simulations/routing_lpm.py",
     "Destination: 10.1.2.50 -> Matches /8, /16, /24 -> Selected: /24 (Longest Prefix Match)"),

    (22, "routers", "Routers", "A router is a multi-homed device that connects multiple distinct subnets and forwards packets between them.",
     "How does a multi-homed Linux machine forward packets between two network interfaces?",
     "Enabling sysctl net.ipv4.ip_forward=1 allows the Linux kernel to act as a full Layer-3 router.",
     "sudo sysctl -w net.ipv4.ip_forward=1",
     "Subnet A (eth0) -> Router Kernel Forwarding Logic -> Subnet B (eth1)"),

    (23, "ttl-hop-limit", "TTL / Hop Limit", "Time-To-Live prevents packets from circulating endlessly in routing loops by decrementing at every hop.",
     "What happens if two misconfigured routers point default routes at each other?",
     "Without TTL, looping packets would consume all link bandwidth; TTL decrements to 0 and is dropped.",
     "sudo tcpdump -i eth0 -nn -v icmp",
     "Hop 1 (TTL=64) -> Hop 2 (TTL=63) -> ... -> Hop N (TTL=0 -> Drop & ICMP Time Exceeded)"),

    (24, "icmp", "ICMP", "Internet Control Message Protocol is the network layer's error-reporting and diagnostics feedback loop.",
     "How does a sender know when a router dropped its packet due to an expired TTL or unreachable port?",
     "Routers and hosts send ICMP messages (Destination Unreachable, Time Exceeded, Echo Request/Reply).",
     "ping -c 3 127.0.0.1",
     "[ IP Header | ICMP Type | ICMP Code | Checksum | Payload / Orig IP Header ]"),

    (25, "traceroute", "traceroute", "traceroute maps network paths by intentionally sending packets with incrementally increasing TTL values.",
     "How can a host map the intermediate router hops between itself and a remote server?",
     "Probe 1 (TTL=1) expires at Hop 1; Probe 2 (TTL=2) expires at Hop 2; ICMP Time Exceeded replies reveal hop IPs.",
     "traceroute -n 1.1.1.1",
     "TTL=1 -> Router 1 drops (Type 11) | TTL=2 -> Router 2 drops | TTL=3 -> Target replies"),

    (26, "mtu", "MTU", "Maximum Transmission Unit defines the largest link-layer payload that can be transmitted without fragmentation.",
     "What happens when an IP packet exceeds the 1500-byte frame payload limit of standard Ethernet?",
     "The packet must either be fragmented into multiple smaller packets or dropped with an ICMP error.",
     "ip link show dev lo",
     "Physical Link MTU (1500 bytes) = IP Header (20) + TCP Header (20) + Payload (1460 bytes MSS)"),

    (27, "fragmentation-concepts", "Fragmentation Concepts", "Modern systems avoid IP fragmentation because losing a single fragment corrupts the entire datagram.",
     "Why do modern TCP stacks set the Don't Fragment (DF) bit and perform Path MTU Discovery?",
     "If any fragment drops, the entire original segment must be retransmitted; PMTUD finds the safe MSS.",
     "ping -M do -s 1472 -c 1 127.0.0.1",
     "Original Packet -> Fragment 1 (MF=1, Offset=0) + Fragment 2 (MF=0, Offset=185)"),

    (28, "ipv6-fundamentals", "IPv6 Fundamentals", "IPv6 provides a 128-bit address space, fixed 40-byte base headers, and native auto-configuration.",
     "Why did IPv4 address depletion demand a fundamentally redesigned network layer?",
     "128 bits yields 3.4 * 10^38 addresses; eliminates NAT dependency and streamlines header processing.",
     "ip -6 addr show",
     "2001:0db8:85a3:0000:0000:8a2e:0370:7334 <-> 2001:db8:85a3::8a2e:370:7334"),

    (29, "ipv4-vs-ipv6", "IPv4 vs IPv6", "Comparing address sizes, header layouts, neighbor discovery, and fragmentation rules across IP generations.",
     "How do operating systems run dual-stack IPv4 and IPv6 concurrently?",
     "Linux maintains dual routing tables; sockets listening on [::] can accept both IPv4-mapped and native IPv6 connections.",
     "ping6 -c 2 ::1 2>/dev/null || ping -c 2 127.0.0.1",
     "IPv4: 32-bit, ARP, Router Frag, NAT | IPv6: 128-bit, NDP Multicast, Host Frag, End-to-End"),

    (30, "transport-layer-problem", "Transport Layer Problem", "IP delivers packets between host interfaces; the transport layer multiplexes communication between distinct processes.",
     "When an IP packet arrives at a host, how does the kernel know which running application owns it?",
     "Port numbers in transport headers identify specific listening and connected socket endpoints.",
     "ss -tulpn",
     "Host IP (Machine) ──► Transport Layer ──► Port Number ──► Process / Socket"),

    (31, "ports", "Ports", "A 16-bit port number (0–65535) provides process-level addressing within a host's transport stack.",
     "How are privileged ports (<1024), registered ports (1024–49151), and ephemeral ports (49152–65535) separated?",
     "Privileged ports require root or CAP_NET_BIND_SERVICE; ephemeral ports are allocated dynamically to clients.",
     "cat /proc/sys/net/ipv4/ip_local_port_range",
     "Socket Address = IP Address + Port (e.g. 192.168.1.10:8080)"),

    (32, "sockets", "Sockets", "A socket is an operating system file descriptor abstraction backed by kernel memory queues and protocol operations.",
     "How does POSIX treat network communication as a read/write file descriptor interface?",
     "socket() returns an int file descriptor linked to struct socket and struct sock buffers in kernel memory.",
     "python3 -c 'import socket; s = socket.socket(); print(s.fileno())'",
     "User Space: fd -> Syscall VFS -> struct socket -> TCP/UDP Stack -> NIC Queue"),

    (33, "udp-from-first-principles", "UDP From First Principles", "UDP provides connectionless, lightweight datagram messaging with minimal 8-byte header overhead and no delivery guarantees.",
     "When does an application require raw datagram speed without the latency overhead of retransmissions?",
     "DNS queries, real-time gaming, and video streaming prioritize immediate arrival over ordered recovery.",
     "tcpdump -i lo -nn udp port 9999",
     "[ Src Port (16b) | Dst Port (16b) | Length (16b) | Checksum (16b) | Data ... ]"),

    (34, "build-udp-client-server", "Build UDP Client/Server", "Implement standard POSIX UDP datagram sockets in Python and C.",
     "How do sendto() and recvfrom() operate without a prior connection handshake?",
     "Each datagram carries destination IP and port independently; no state is stored in the transport layer.",
     "python3 socket-programs/python/udp_echo_server.py & python3 socket-programs/python/udp_echo_client.py 'Hello'",
     "Client: sendto((host, port)) -> Wire -> Server: recvfrom() -> sendto(client_addr)"),

    (35, "udp-loss-simulation", "UDP Loss Simulation", "Simulating packet loss, packet duplication, and jitter over UDP to prove application responsibility.",
     "What happens when datagrams drop, duplicate, or arrive out of order?",
     "The UDP kernel stack silently drops corrupted packets; the application must detect loss via timeouts.",
     "python3 socket-programs/python/packet_loss_proxy.py",
     "Sender -> Unreliable Proxy (30% Drop) -> Receiver (Timeouts observed)"),

    (36, "why-tcp-exists", "Why TCP Exists", "TCP creates the illusion of an error-free, continuous, bidirectional ordered byte stream over unreliable packet networks.",
     "How can reliable applications be built on top of an underlying IP layer that drops, reorders, and duplicates packets?",
     "TCP adds sequence numbers, acknowledgments, sliding windows, timeouts, and retransmission logic.",
     "python3 simulations/tcp_seq_ack_retransmit.py",
     "Unreliable Packets + TCP State Machine = Reliable Ordered Byte Stream"),

    (37, "tcp-connection", "TCP Connection", "A TCP connection is defined strictly by its 4-tuple: (Source IP, Source Port, Destination IP, Destination Port).",
     "How can a web server handle 10,000 simultaneous clients all connected to the exact same port 443?",
     "Each connection has a unique 4-tuple and dedicated Transmission Control Block (TCB) in kernel memory.",
     "ss -tan state established",
     "4-Tuple: (Client_IP:54321 <-> Server_IP:443) -> Unique Socket State"),

    (38, "three-way-handshake", "Three-Way Handshake", "TCP establishes connections and synchronizes initial sequence numbers via the SYN, SYN-ACK, ACK handshake.",
     "Why are two packets insufficient to reliably establish a bidirectional full-duplex connection?",
     "Both sides must independently propose their Initial Sequence Number (ISN) and acknowledge the peer's ISN.",
     "sudo tcpdump -i lo -nn \"tcp[tcpflags] & (tcp-syn) != 0\"",
     "Client ──[ SYN: seq=X ]──► Server ──[ SYN-ACK: seq=Y, ack=X+1 ]──► Client ──[ ACK: ack=Y+1 ]──► Server"),

    (39, "tcp-sequence-numbers", "TCP Sequence Numbers", "TCP sequence numbers count individual payload bytes, not packet counts, allowing seamless stream reassembly.",
     "How does a receiving TCP stack detect missing chunks or duplicate deliveries in a byte stream?",
     "Each segment's seq number indicates the byte offset of its first data byte in the overall stream.",
     "python3 simulations/tcp_seq_ack_retransmit.py",
     "Stream Bytes 0..999 (Seq 1000) -> Bytes 1000..1999 (Seq 2000) -> Cumulative ACK 3000"),

    (40, "retransmission", "Retransmission", "TCP infers packet loss through retransmission timeouts (RTO) or 3 duplicate ACKs (Fast Retransmit).",
     "When an acknowledgment fails to arrive, how does TCP recover without stalling the application permanently?",
     "TCP starts an RTO timer; if it expires or 3 duplicate ACKs arrive, the missing segment is retransmitted.",
     "python3 simulations/tcp_seq_ack_retransmit.py",
     "Send Seg 1, 2, 3 -> Seg 2 dropped -> 3 Dup ACKs for Seg 1 -> Fast Retransmit Seg 2"),

    (41, "sliding-window", "Sliding Window", "The sliding window protocol enables pipelining by allowing multiple segments in flight before waiting for acknowledgments.",
     "Why is Stop-and-Wait communication catastrophically slow over high-latency networks?",
     "Stop-and-Wait limits throughput to 1 packet per RTT; a sliding window of size W increases throughput W-fold.",
     "python3 simulations/sliding_window.py",
     "Window [base .. base+W] -> Transmit in flight -> Receive ACK -> Slide window forward"),

    (42, "flow-control", "Flow Control", "Flow control prevents a fast sender from overflowing a slow receiver's socket buffer via the advertised receive window.",
     "What happens if an application process stops calling read() while data arrives from the network?",
     "The kernel receive buffer fills up; the receiver advertises win=0 in ACK headers, forcing the sender to pause.",
     "ss -t -i",
     "Receiver Window (rcv_wnd) advertised in TCP header: Flow Control protects RECEIVER"),

    (43, "congestion", "Congestion", "Network congestion occurs when aggregate traffic exceeds the queueing capacity of intermediate routers.",
     "Why does sending faster into a congested network result in lower goodput and higher latency?",
     "Router queues fill, causing packet drops, retransmission storms, and bufferbloat latency spikes.",
     "python3 simulations/queueing_bufferbloat.py",
     "Overload -> Router Queue Fills -> Packets Dropped -> Throughput Collapses"),

    (44, "tcp-congestion-control", "TCP Congestion Control", "TCP congestion control regulates the sender's congestion window (cwnd) based on network capacity signals.",
     "How do algorithms like Cubic and BBR prevent network collapse without central coordination?",
     "Slow Start probes bandwidth exponentially; Congestion Avoidance increases linearly; loss cuts cwnd.",
     "python3 simulations/congestion_control.py",
     "cwnd: Slow Start (exponential) -> AIMD (Additive Increase / Multiplicative Decrease)"),

    (45, "bandwidth-delay-product", "Bandwidth-Delay Product", "BDP (Bandwidth * RTT) defines the buffer capacity required to fully saturate a high-speed network path.",
     "Why can a 10 Gbps transcontinental link only achieve 50 Mbps with default Linux socket buffers?",
     "If the socket buffer is smaller than the BDP, the sender is forced to pause and wait for ACKs before refilling the pipe.",
     "python3 -c 'bdp = (10*10**9 / 8) * 0.050; print(f\"BDP = {bdp/(1024*1024):.1f} MB\")'",
     "BDP = Bandwidth (bps) * RTT (sec) -> Required Socket Buffer Size for Line Rate"),

    (46, "tcp-connection-teardown", "TCP Connection Teardown", "TCP tears down connections gracefully using bidirectional FIN and ACK exchanges.",
     "How do both endpoints verify that all in-flight data has been completely delivered before closing?",
     "Active closer sends FIN; passive side replies ACK (half-closed); passive side sends FIN; active closer replies ACK.",
     "sudo tcpdump -i lo -nn \"tcp[tcpflags] & (tcp-fin) != 0\"",
     "Active: FIN_WAIT_1 -> FIN_WAIT_2 -> TIME_WAIT | Passive: CLOSE_WAIT -> LAST_ACK -> CLOSED"),

    (47, "time-wait", "TIME_WAIT", "TIME_WAIT persists for 2*MSL to ensure the remote end received the final ACK and to drain stale segments from the Internet.",
     "Why is disabling TIME_WAIT with SO_LINGER=0 dangerous in production systems?",
     "Delayed old packets can collide with and corrupt newly opened connections sharing the same 4-tuple.",
     "ss -tan state time-wait",
     "Active Closer enters TIME_WAIT (typically 60s) -> Ensures final ACK delivery"),

    (48, "connection-refused-vs-timeout", "Connection Refused vs Timeout", "Connection Refused (TCP RST) proves reachability but no listening process; Timeout proves packet drop in transit.",
     "Why is 'Connection Refused' positive diagnostic proof that the network and firewall are functioning?",
     "The destination kernel received the SYN, verified no port listener, and actively sent back a TCP RST.",
     "nc -zv 127.0.0.1 9991 2>&1",
     "Port closed -> TCP RST (Connection Refused) | Firewall drop -> SYN retransmits (Timed out)"),

    (49, "tcp-server-from-scratch", "TCP Server From Scratch", "Implement the fundamental POSIX lifecycle: socket(), bind(), listen(), accept(), read(), write().",
     "Understand the mechanical syscall transitions from passive listener to active communication sockets.",
     "socket creates descriptor; bind reserves address; listen queues handshakes; accept yields connected fd.",
     "python3 socket-programs/python/tcp_echo_server.py",
     "socket() -> bind() -> listen() -> accept() -> read()/write() -> close()"),

    (50, "listening-socket-vs-connected-socket", "Listening Socket vs Connected Socket", "A listening socket is a passive rendezvous point; accept() spawns a dedicated connected socket for data transfer.",
     "Why does accept() create a brand-new file descriptor instead of reusing the listening descriptor?",
     "The listener must remain open on the port to accept subsequent connections from other clients concurrently.",
     "ss -tulpn && ss -tan",
     "Listener (0.0.0.0:80, LISTEN) ──accept()──► Connected Socket (192.168.1.10:80 <-> Client:54321)"),

    (51, "many-tcp-connections", "Many TCP Connections", "Handle thousands of concurrent connections using non-blocking I/O multiplexing (select, poll, epoll).",
     "Why does the thread-per-connection architecture fail to scale past 10,000 clients (C10K problem)?",
     "Thread stack memory and context-switching overhead saturate CPU; event-driven epoll handles all fds on one thread.",
     "python3 socket-programs/python/tcp_multiclient_server.py",
     "Single Thread -> select()/epoll() -> Woken up only when socket fds have data ready"),

    (52, "ephemeral-ports", "Ephemeral Ports", "Operating systems dynamically assign short-lived source ports to outbound client connections.",
     "How does a client connect to multiple destination services without binding explicit local ports?",
     "The kernel allocates a free port from ip_local_port_range; port reuse occurs once connections terminate.",
     "cat /proc/sys/net/ipv4/ip_local_port_range",
     "Client Kernel allocates ephemeral port (e.g. 54321) -> Connects to Server port 80"),

    (53, "dns-problem", "DNS Problem", "Hardcoded IP addresses do not scale operationally; systems require a human-readable, decoupled name-to-address mapping.",
     "What happened when the early Internet used a centralized static /etc/hosts file for name resolution?",
     "Daily host file synchronization collapsed under scale; DNS introduced a distributed hierarchical database.",
     "cat /etc/hosts",
     "Hostname (example.com) ──DNS Resolution──► IP Address (93.184.216.34)"),

    (54, "dns-hierarchy", "DNS Hierarchy", "The global DNS namespace is structured as a tree rooted at '.', partitioned into TLDs, and delegated to authoritative servers.",
     "Why does a local DNS lookup not query the root nameservers for every single request?",
     "Delegation and caching: Root delegates to .com TLD, which delegates to authoritative servers for domain.",
     "dig +trace example.com",
     "Root (.) ──► TLD (.com) ──► Authoritative (example.com)"),

    (55, "recursive-resolver", "Recursive Resolver", "A recursive resolver queries the global hierarchy on behalf of client stub resolvers, caching intermediate answers.",
     "What is the division of labor between your laptop's stub resolver and a full recursive DNS server?",
     "The stub resolver sends recursive queries to 1.1.1.1; 1.1.1.1 performs iterative lookups across the hierarchy.",
     "cat /etc/resolv.conf",
     "Client Stub Resolver ──► Recursive Resolver (1.1.1.1) ──Iterative Queries──► Root/TLD/Auth"),

    (56, "dns-record-types", "DNS Record Types", "DNS stores diverse resource records: A (IPv4), AAAA (IPv6), CNAME (Alias), MX (Mail), TXT (Metadata), NS (Nameserver).",
     "How does DNS support multiple protocols and services beyond simple IP mapping?",
     "Queries specify Question Type (QTYPE); the authoritative server returns matching Resource Records.",
     "dig example.com A && dig example.com TXT",
     "Records: A (93.184.216.34) | AAAA (2606:2800:..) | CNAME (alias) | TXT (spf/verification)"),

    (57, "dns-caching-and-ttl", "DNS Caching and TTL", "Time-To-Live (TTL) governs how long intermediate resolvers may cache a DNS record before re-querying.",
     "Why do DNS changes take time to become visible across global clients?",
     "Resolvers must honor the record's TTL; lowering TTL before migrations enables rapid cutover.",
     "python3 simulations/dns_resolver.py",
     "Authoritative sets TTL=300 -> Recursive Resolver caches for 300s -> Discard after expiry"),

    (58, "dns-debugging", "DNS Debugging", "Diagnose name resolution failures systematically using dig, getent, and systemd-resolved.",
     "How do you determine whether a failure is caused by local /etc/resolv.conf, a remote nameserver, or NXDOMAIN?",
     "dig inspects wire flags, status codes (NOERROR, NXDOMAIN, SERVFAIL), answering server, and TTL.",
     "dig api.internal +trace 2>&1",
     "Does name resolve? Which server answered? What RCODE? What TTL?"),

    (59, "build-a-tiny-dns-resolver-experiment", "Build a Tiny DNS Resolver Experiment", "Construct an in-memory DNS server and caching resolver in Python.",
     "Understand binary DNS wire serialization, question decoding, and TTL eviction logic from scratch.",
     "Implement UDP socket receiver, unpack 12-byte header, parse QNAME, format answer, and return packet.",
     "python3 projects/03-dns-resolver/dns_server.py & dig @127.0.0.1 -p 5353 example.com",
     "UDP Port 53/5353 -> Parse QNAME -> Check Cache -> Build RFC 1035 Response"),

    (60, "http-from-first-principles", "HTTP From First Principles", "HTTP is an ASCII text request/response application protocol layered directly over a TCP transport stream.",
     "How do web browsers communicate with servers without specialized binary framing?",
     "Sending raw ASCII lines followed by \\r\\n\\r\\n over a TCP socket triggers a standard HTTP response.",
     "printf \"GET / HTTP/1.1\\r\\nHost: example.com\\r\\nConnection: close\\r\\n\\r\\n\" | nc example.com 80",
     "Client: GET / HTTP/1.1\\r\\nHost: ..\\r\\n\\r\\n -> Server: HTTP/1.1 200 OK\\r\\n..\\r\\n\\r\\nBody"),

    (61, "http-request-response", "HTTP Request/Response", "HTTP request and response structures: Method, Path, Version, Headers, and optional Body separated by CRLF.",
     "How does an HTTP parser know where metadata ends and payload begins?",
     "The empty line \\r\\n\\r\\n marks the end of headers; Content-Length or chunked encoding specifies body size.",
     "python3 socket-programs/python/http_server_raw.py",
     "[ Request Line / Status Line ] + [ Headers ] + [ \\r\\n ] + [ Optional Body ]"),

    (62, "http-methods", "HTTP Methods", "HTTP methods define the semantic intention of the client request (GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS).",
     "Why must GET and HEAD be safe and idempotent, while POST is unsafe?",
     "Network retries can safely replay idempotent requests (GET, PUT) without duplicating business transactions.",
     "curl -v -X GET http://127.0.0.1:8080/health",
     "GET (Safe/Idempotent) | POST (Unsafe/Non-idempotent) | PUT (Idempotent) | DELETE (Idempotent)"),

    (63, "http-status-codes", "HTTP Status Codes", "HTTP status code families convey the semantic outcome of request processing (2xx, 3xx, 4xx, 5xx).",
     "Why is returning 200 OK with an error message inside JSON an architectural antipattern?",
     "Proxies, load balancers, and monitoring systems rely on status code families (4xx client error, 5xx server fault).",
     "curl -I http://127.0.0.1:8080/nonexistent",
     "1xx Informational | 2xx Success | 3xx Redirect | 4xx Client Error | 5xx Server Error"),

    (64, "http-keep-alive", "HTTP Keep-Alive", "Persistent connections reuse established TCP handshakes across sequential HTTP requests, slashing latency.",
     "Why was HTTP/1.0's model of opening a new TCP connection for every single asset file catastrophic?",
     "Every connection incurred 1.5 RTT of handshake setup and reset slow-start cwnd; Keep-Alive eliminates this.",
     "python3 benchmarks/connection_pool_benchmark.py",
     "Req 1 (Handshake + Data) -> Connection stays open -> Req 2 (Data only: 0 handshake overhead)"),

    (65, "http-11-limitations", "HTTP/1.1 Limitations", "HTTP/1.1 suffers from application-layer Head-of-Line (HoL) blocking and repetitive uncompressed headers.",
     "Why could HTTP/1.1 pipelining not be safely enabled across the Internet?",
     "Responses had to be returned in strict FIFO request order; a slow first request stalled all subsequent replies.",
     "cat docs/mental-models.md",
     "Req A, Req B, Req C -> Server stalls on A -> B and C blocked behind A (Head-of-Line Blocking)"),

    (66, "http-2-concepts", "HTTP/2 Concepts", "HTTP/2 introduces binary framing and multiplexed concurrent streams over a single shared TCP connection.",
     "How does HTTP/2 allow hundreds of concurrent requests without opening multiple TCP sockets?",
     "Requests and responses are split into interleaved binary frames tagged with distinct stream IDs.",
     "curl --http2 -I https://www.google.com 2>/dev/null || curl -I https://www.google.com",
     "Single TCP Connection: [Stream 1 Frame] [Stream 3 Frame] [Stream 1 Frame] (Multiplexing)"),

    (67, "http-3-quic-concepts", "HTTP/3 / QUIC Concepts", "HTTP/3 replaces TCP with QUIC over UDP, eliminating transport-layer head-of-line blocking and speeding handshakes.",
     "Why was HTTP/2 over TCP still vulnerable to packet loss stalls?",
     "A single dropped TCP packet stalls all multiplexed streams; QUIC over UDP isolates loss to the affected stream.",
     "curl --http3 -I https://cloudflare.com 2>/dev/null || echo 'HTTP/3 over UDP'",
     "HTTP/3 ──► QUIC (Stream Multiplexing + Congestion + TLS 1.3) ──► UDP Datagrams"),

    (68, "tls-problem", "TLS Problem", "Unencrypted communication allows eavesdropping, tampering, and impersonation across open transit networks.",
     "What security guarantees are required when sending sensitive data across unknown routers?",
     "Confidentiality (encryption), Integrity (tamper detection), and Authentication (identity verification).",
     "openssl s_client -connect example.com:443 -brief </dev/null",
     "Plaintext Wire -> Eavesdropping/Tampering -> TLS Wrapper -> Encrypted/Authenticated"),

    (69, "cryptography-prerequisites", "Cryptography Prerequisites", "Understanding symmetric encryption (AES/ChaCha20), asymmetric key exchange (ECDHE), and digital signatures.",
     "Why can asymmetric encryption not be used to encrypt the entire application data stream?",
     "Asymmetric math is computationally expensive; TLS uses asymmetric exchange to establish a shared symmetric session key.",
     "python3 -c 'import hashlib; print(hashlib.sha256(b\"hello\").hexdigest())'",
     "Asymmetric ECDHE (Key Exchange) -> Shared Secret -> Symmetric AES-GCM (Bulk Data Encryption)"),

    (70, "tls-handshake", "TLS Handshake", "The TLS 1.3 handshake achieves authenticated key agreement in a single round trip (1-RTT).",
     "How do client and server agree on cryptographic keys and verify server identity in 1 round trip?",
     "Client sends ClientHello with KeyShare; Server replies ServerHello with its KeyShare and encrypted certificate.",
     "openssl s_client -connect example.com:443 -tls1_3 </dev/null",
     "ClientHello + KeyShare ──► ServerHello + EncryptedCert + Finished ──► Client Finished (1-RTT)"),

    (71, "certificates", "Certificates", "An X.509 digital certificate binds a public key to a domain name, signed by a trusted Certificate Authority.",
     "How does a client know that a public key belongs to example.com and not an imposter?",
     "The client validates the digital signature generated by a trusted Certificate Authority (CA).",
     "openssl s_client -connect example.com:443 -showcerts </dev/null",
     "[ Subject: example.com | Public Key | Validity Dates | Issuer: Let's Encrypt | CA Signature ]"),

    (72, "certificate-validation", "Certificate Validation", "Validating the certificate chain of trust from leaf certificate up through intermediate CAs to a trusted Root CA.",
     "Why does curl fail with 'certificate verify failed' on corporate networks or self-signed servers?",
     "The client's trust store does not contain the signing Root CA, or the hostname does not match the SAN.",
     "curl -v https://example.com",
     "Leaf Cert -> Intermediate CA Cert -> Root CA (in OS Trust Store) -> Signature Verified"),

    (73, "https-request-trace", "HTTPS Request Trace", "Trace the complete end-to-end integration: DNS -> TCP Handshake -> TLS Handshake -> HTTP Request.",
     "Experience how all layers synthesize into a single secure web transaction.",
     "DNS resolves IP (1 RTT); TCP establishes socket (1 RTT); TLS negotiates encryption (1 RTT); HTTP GET sent.",
     "curl -v -w \"\\nDNS: %{time_namelookup}s | TCP: %{time_connect}s | TLS: %{time_appconnect}s\\n\" -o /dev/null -s https://example.com",
     "DNS -> TCP SYN/ACK -> TLS 1.3 Handshake -> Encrypted HTTP Request -> Encrypted Response"),

    (74, "nat-from-first-principles", "NAT From First Principles", "Network Address Translation rewrites source or destination IP addresses to allow private hosts to reach the Internet.",
     "How can millions of private devices with non-routable IPs communicate across the public Internet?",
     "A NAT gateway rewrites private source IPs and ports to its own public IP and tracks translations in memory.",
     "sudo iptables -t nat -L -n -v",
     "Private Host (10.0.1.10:50000) ──► NAT Router ──► Public Internet (203.0.113.1:62001)"),

    (75, "private-vs-public-ip", "Private vs Public IP", "RFC 1918 defines non-routable private address blocks: 10.0.0.0/8, 172.16.0.0/12, and 192.168.0.0/16.",
     "Why are packets with private IP addresses dropped immediately by Internet service provider routers?",
     "Private addresses are not globally unique; without NAT, return packets cannot be routed back.",
     "ip addr show",
     "RFC 1918 Private Ranges: 10.0.0.0/8 | 172.16.0.0/12 | 192.168.0.0/16"),

    (76, "source-nat", "Source NAT", "SNAT (or Masquerading) rewrites outbound packet source IPs to mask internal topologies.",
     "How does a Linux gateway dynamically translate outgoing traffic from local containers or LAN hosts?",
     "iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE creates dynamic translation entries in conntrack.",
     "sudo iptables -t nat -A POSTROUTING -s 10.99.1.0/24 -j MASQUERADE",
     "Outbound: Replace Src 10.0.1.10 with Gateway Public IP | Inbound: Restore original private IP"),

    (77, "destination-nat-port-forwarding", "Destination NAT / Port Forwarding", "DNAT rewrites destination IP and port to expose internal private services to external networks.",
     "How does Docker port publishing (-p 8080:80) allow external hosts to reach a container's private IP?",
     "DNAT rules in the PREROUTING chain intercept incoming traffic and rewrite the destination to the container IP.",
     "sudo iptables -t nat -L PREROUTING -n -v",
     "External Client -> Gateway:8080 -> DNAT rewrites destination to Container_IP:80"),

    (78, "nat-limitations", "NAT Limitations", "NAT breaks the end-to-end principle, complicates peer-to-peer protocols, and exhausts translation state tables.",
     "Why do VoIP, WebRTC, and P2P applications require STUN, TURN, and ICE protocols?",
     "Internal hosts do not know their external public IP:port mapping and cannot directly accept inbound connections.",
     "sudo conntrack -C 2>/dev/null || cat /proc/sys/net/netfilter/nf_conntrack_count 2>/dev/null",
     "NAT Breaks End-to-End Transparency -> Requires Keepalives and STUN/TURN Traversal"),

    (79, "firewalls-from-first-principles", "Firewalls From First Principles", "A firewall enforces access control policy by evaluating packets against a sequential ruleset.",
     "How does an operating system protect itself from unwanted incoming connection attempts?",
     "Packet filters examine the 5-tuple (Src IP, Dst IP, Proto, Src Port, Dst Port) and decide ACCEPT or DROP.",
     "sudo iptables -L -n -v",
     "Packet Arrives -> Evaluate Filter Rules -> Match Rule? YES -> ACCEPT / DROP / REJECT"),

    (80, "stateful-vs-stateless-filtering", "Stateful vs Stateless Filtering", "Stateful firewalls track bidirectional connection state in conntrack, allowing return traffic automatically.",
     "Why are stateless ACLs cumbersome compared to stateful firewalls?",
     "Stateless ACLs require manually opening thousands of high ephemeral return ports; stateful filters track flows.",
     "sudo iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT",
     "SYN -> State: NEW | SYN-ACK / ACK -> State: ESTABLISHED (Return packets automatically allowed)"),

    (81, "nftables-firewall-tooling", "nftables / Firewall Tooling", "nftables is the modern Linux kernel subsystem unifying packet classification, filtering, and NAT.",
     "Why did Linux replace iptables, ip6tables, arptables, and ebtables with nftables?",
     "nftables provides a single bytecode engine, atomic rule updates, and higher performance.",
     "sudo nft list ruleset 2>/dev/null || true",
     "nftables: Table -> Base Chains (prerouting, input, forward, output, postrouting) -> Rules"),

    (82, "network-policies-and-security-groups", "Network Policies and Security Groups", "Mapping Linux firewall concepts to cloud Security Groups (stateful) and Kubernetes NetworkPolicies.",
     "How do cloud AWS Security Groups and Kubernetes NetworkPolicies implement the same primitives as Netfilter?",
     "Security Groups are stateful virtual firewalls; Kubernetes CNIs compile NetworkPolicies into iptables/eBPF.",
     "cat docs/mental-models.md",
     "Linux iptables <-> AWS Security Group (Stateful) <-> Kubernetes NetworkPolicy (CNI)"),

    (83, "proxy-from-first-principles", "Proxy From First Principles", "A proxy terminates an incoming client connection and establishes an independent outbound connection to a backend.",
     "Why is a proxy fundamentally different from a router or NAT gateway?",
     "A router forwards packets at L3; a proxy operates at L4/L7 as an application endpoint managing two distinct TCP sockets.",
     "python3 projects/06-reverse-proxy/reverse_proxy.py",
     "Client ──(TCP Socket 1)──► Proxy Process ──(TCP Socket 2)──► Backend Server"),

    (84, "forward-proxy", "Forward Proxy", "A forward proxy acts on behalf of internal clients to access external Internet services (caching, egress control).",
     "How do corporate networks inspect, filter, and cache outbound web requests from employee workstations?",
     "Clients configure HTTP_PROXY; the proxy handles HTTP GET or uses HTTP CONNECT to tunnel encrypted TLS.",
     "curl -x http://proxy.local:8080 http://example.com 2>/dev/null || true",
     "Internal Client -> Forward Proxy -> Internet Server (Client IP masked)"),

    (85, "reverse-proxy", "Reverse Proxy", "A reverse proxy acts on behalf of backend servers to provide TLS termination, routing, and caching.",
     "How do web architectures hide internal microservice topologies behind a single public domain?",
     "Clients connect to the reverse proxy; the proxy inspects request paths and dispatches to internal services.",
     "python3 projects/06-reverse-proxy/reverse_proxy.py",
     "Internet Client -> Reverse Proxy -> Internal Microservices (Backend IPs masked)"),

    (86, "load-balancing", "Load Balancing", "Load balancers distribute incoming traffic across pools of backend servers to maximize throughput and reliability.",
     "How do systems scale beyond the capacity of a single physical server?",
     "A load balancer distributes requests across multiple instances using algorithms like Round Robin or Least Connections.",
     "python3 projects/07-load-balancer/load_balancer.py",
     "Client Requests -> Load Balancer -> Backend Pool (Instance 1, Instance 2, Instance 3)"),

    (87, "layer-4-vs-layer-7-load-balancing", "Layer 4 vs Layer 7 Load Balancing", "L4 load balancers forward raw TCP/UDP streams; L7 load balancers inspect application HTTP headers and paths.",
     "When should you choose an AWS NLB (Layer 4) versus an AWS ALB (Layer 7)?",
     "L4 provides ultra-low latency line-rate packet dispatch; L7 enables path routing (/api vs /static) and TLS offload.",
     "cat docs/mental-models.md",
     "L4: Inspects IP:Port (TCP stream proxy) | L7: Inspects HTTP Headers, Cookies, URI Paths"),

    (88, "health-checks", "Health Checks", "Active health check probes detect degraded or crashed backends and remove them from active routing pools.",
     "What happens if an application process deadlocks but its port remains open?",
     "A synthetic HTTP health check (/healthz) verifying database connectivity detects the failure and evicts the node.",
     "python3 projects/06-reverse-proxy/test_proxy.py",
     "Active Probe: GET /health -> 200 OK (Keep in pool) | Timeout / 500 (Evict from pool)"),

    (89, "connection-pooling", "Connection Pooling", "Connection pooling maintains a warm cache of established TCP sockets to eliminate per-request handshake latency.",
     "Why do high-throughput microservices experience high latency and CPU spikes without connection pooling?",
     "Opening a new TCP+TLS connection for every database query costs 2-3 RTTs and thousands of CPU cycles in crypto math.",
     "python3 benchmarks/connection_pool_benchmark.py",
     "App Worker -> Request Socket from Pool -> Use Socket -> Return to Pool (0 Handshake Overhead)"),

    (90, "keepalive-at-different-layers", "Keepalive at Different Layers", "Differentiating HTTP Keep-Alive, TCP Keepalive probes, and application-level heartbeats.",
     "Why does enabling TCP keepalive not keep an idle HTTP/1.1 persistent connection from closing?",
     "HTTP Keep-Alive governs application idle reuse; TCP SO_KEEPALIVE detects dead sockets; heartbeats check process health.",
     "cat docs/mental-models.md",
     "L7: Connection: keep-alive | L4: SO_KEEPALIVE (ACK probes) | App: Ping/Pong Heartbeats"),

    (91, "network-namespaces", "Network Namespaces", "Linux network namespaces virtualize the network stack, providing isolated routing tables, interfaces, and sockets.",
     "How do Docker and Kubernetes provide isolated networking to containers on a shared Linux host?",
     "The kernel gives each namespace private copies of loopback, interfaces, routing tables, and firewall rules.",
     "sudo ip netns add ns-demo && sudo ip netns list",
     "Host Network Stack <──Isolated Boundary──► Container Network Namespace"),

    (92, "veth-pairs", "veth Pairs", "Virtual Ethernet pairs act as bidirectional virtual patch cables linking two network namespaces.",
     "How do packets cross the isolation boundary between a container namespace and the host?",
     "A veth pair is created; one end is placed in the container namespace, and the peer end remains in the host/bridge.",
     "sudo ip link add veth-a type veth peer name veth-b",
     "Namespace A (veth-a) ◄──────Virtual Patch Cable──────► Namespace B (veth-b)"),

    (93, "linux-bridge", "Linux Bridge", "A Linux software bridge acts as a virtual Layer-2 learning switch inside the kernel.",
     "How do multiple containers on the same host communicate with each other over a shared local subnet?",
     "The host creates a bridge (docker0); container veth peer ends are plugged into the bridge as switch ports.",
     "sudo ip link add br0 type bridge",
     "Container 1 (veth1) ──┐\nContainer 2 (veth2) ──┼──► Linux Bridge (br0) ──► Host L2 Domain"),

    (94, "router-with-network-namespaces", "Router With Network Namespaces", "Construct a complete multi-subnet routed network with static routing inside Linux namespaces.",
     "Experience how an intermediate namespace forwards packets between two separate subnets.",
     "Client namespace (10.99.1.10) connects to Router (10.99.1.1); Router forwards to Server (10.99.2.10).",
     "sudo ./scripts/create-network-lab.sh",
     "ns-client (10.99.1.10) ──► ns-router (10.99.1.1 | 10.99.2.1) ──► ns-server (10.99.2.10)"),

    (95, "build-a-tiny-internet", "Build a Tiny Internet", "Capstone virtual Internet topology linking client LAN, transit network, server LAN, DNS, and HTTP.",
     "Synthesize namespaces, veth pairs, routing tables, DNS, and web servers into a functional mini-Internet.",
     "Trace packets as they traverse client, edge router, transit backbone, datacenter router, and server.",
     "sudo ./projects/08-tiny-internet/setup_tiny_internet.sh",
     "Client LAN ──► Router A ──► Transit Network ──► Router B ──► Datacenter LAN"),

    (96, "tcpdump", "tcpdump", "tcpdump is the foundational CLI packet analyzer for capturing and inspecting raw network frames.",
     "How do you inspect the actual bytes traveling across an interface when application logs are unhelpful?",
     "tcpdump uses libpcap and the Linux BPF engine to capture packets directly from the network driver queue.",
     "sudo tcpdump -i any -nn -c 5",
     "Network Interface -> Kernel BPF Filter -> tcpdump User Space Buffer -> Formatted Output"),

    (97, "reading-packet-captures", "Reading Packet Captures", "Master Berkeley Packet Filter (BPF) syntax to isolate specific protocols, flags, ports, and hosts.",
     "How do you filter out background noise on busy production servers to focus only on failing TCP sessions?",
     "Use precision BPF expressions: 'tcp[tcpflags] & (tcp-syn|tcp-rst) != 0 and host 10.0.1.50'.",
     "sudo tcpdump -i any -nn \"tcp[tcpflags] & tcp-syn != 0\"",
     "BPF Syntax: host, net, port, proto, and bitwise header flag masking"),

    (98, "wireshark-optional-track", "Wireshark Optional Track", "Graphical packet dissection, stream following, protocol hierarchy statistics, and I/O graphs.",
     "How does Wireshark provide deep visual correlation of complex multi-protocol flows?",
     "Wireshark reassembles TCP byte streams, parses TLS handshake records, and highlights anomalies.",
     "cat packet-captures/README.md",
     "pcap File -> Wireshark Dissector -> Protocol Tree / Follow TCP Stream"),

    (99, "packet-debugging-methodology", "Packet Debugging Methodology", "The 4-Question Packet Hypothesis: Did it leave sender? Reach receiver? Did receiver reply? Did reply return?",
     "How do you locate the exact hop where a packet was dropped without guessing?",
     "Capture simultaneously on sender and receiver; compare timestamps and sequence numbers.",
     "cat docs/packet-debugging.md",
     "[1] Left Client? -> [2] Arrived at Server? -> [3] Server Replied? -> [4] Returned to Client?"),

    (100, "network-performance", "Network Performance", "Formalizing the foundational metrics: Bandwidth, Goodput, Throughput, RTT, Jitter, and Packet Loss.",
     "Why is 'network speed' an ambiguous phrase that confuses bandwidth with latency?",
     "Bandwidth is capacity (bits/sec); latency is delay (sec); throughput is actual data transferred; jitter is delay variance.",
     "python3 benchmarks/latency_benchmark.py",
     "Metrics: Bandwidth (pipe width) vs Latency (pipe length) vs Throughput (actual flow)"),

    (101, "measuring-latency", "Measuring Latency", "Profile network latency accurately using ping RTT, curl connection timing, and socket timestamps.",
     "How do you break down where time was spent during an HTTP API request?",
     "curl -w decomposes total time into DNS lookup, TCP connect, TLS handshake, and Time-To-First-Byte (TTFB).",
     "curl -w \"DNS: %{time_namelookup}s | TCP: %{time_connect}s | Total: %{time_total}s\\n\" -o /dev/null -s https://example.com",
     "Total Time = DNS Lookup + TCP Handshake + TLS Handshake + Server Processing + Transfer"),

    (102, "throughput", "Throughput", "Measure saturating network capacity using iperf3 and custom socket streaming benchmarks.",
     "What factors limit real-world throughput below the raw physical link speed?",
     "TCP window limits, packet loss retransmissions, socket buffer sizes, and CPU serialization overhead.",
     "python3 benchmarks/throughput_benchmark.py",
     "Socket Buffer Fill Rate vs Physical Serialization Rate"),

    (103, "packet-loss", "Packet Loss", "Simulating controlled packet loss using Linux Traffic Control (tc netem) and observing TCP collapse.",
     "Why does a mere 2% packet loss cause TCP throughput to collapse by over 80% on high-latency links?",
     "Standard loss-based congestion control (Reno/Cubic) interprets any packet drop as severe congestion and halves cwnd.",
     "sudo tc qdisc add dev veth-c root netem loss 5% 2>/dev/null || true",
     "Loss Detected -> cwnd cut in half -> Pipe empties -> Throughput collapses"),

    (104, "delay-and-jitter", "Delay and Jitter", "Simulate latency variance and packet reordering using tc netem; examine impact on real-time systems.",
     "How does jitter degrade real-time voice, video, and distributed consensus protocols?",
     "Variance in arrival times forces receivers to implement jitter buffers; excessive jitter causes late packet drops.",
     "sudo tc qdisc add dev veth-c root netem delay 50ms 10ms 2>/dev/null || true",
     "Packet 1 (50ms) -> Packet 2 (40ms) -> Packet 2 arrives before Packet 1 (Reordering)"),

    (105, "bandwidth-limits", "Bandwidth Limits", "Implement the Token Bucket algorithm to shape traffic and enforce rate limits.",
     "How do routers and cloud providers police bandwidth without dropping bursts of traffic?",
     "Tokens accumulate at a steady rate; bursts consume available bucket tokens; excess traffic is queued or dropped.",
     "python3 simulations/token_bucket.py",
     "Token Rate (r) + Bucket Capacity (b) -> Controls sustained throughput and maximum burst"),

    (106, "queueing", "Queueing", "Simulate M/M/1 queueing delay and prove mathematically why latency explodes as link utilization approaches 100%.",
     "Why does a network running at 95% capacity experience massive latency spikes compared to 70% capacity?",
     "Queueing delay formula W = 1 / (mu - lambda) has a vertical asymptote as arrival rate lambda approaches service rate mu.",
     "python3 simulations/queueing_bufferbloat.py",
     "Utilization rho -> 1.0 ──► Queue Length L -> Infinity ──► Latency Explodes"),

    (107, "bufferbloat-concept", "Bufferbloat Concept", "Excessive unmanaged buffering in network devices ruins interactive latency while maintaining zero packet loss.",
     "Why can an upload saturate your internet link and cause gaming ping times to spike from 15ms to 3000ms?",
     "Large FIFO buffers delay packets for seconds; Active Queue Management (CoDel / CAKE) drops early to signal TCP.",
     "python3 simulations/queueing_bufferbloat.py",
     "Bloated FIFO Buffer (Seconds of lag) vs Bounded FQ-CoDel Buffer (Low latency preserved)"),

    (108, "retries-and-timeouts", "Retries and Timeouts", "The delicate relationship between client timeouts, retry policies, and cascading service outages.",
     "Why do static, short timeouts turn a temporary network blip into a catastrophic permanent outage?",
     "Clients timeout while server is processing; clients retry, duplicating incoming load and overloading the server.",
     "python3 simulations/retries_exponential_backoff.py",
     "Slow Server -> Client Timeout -> Client Retries -> Doubled Server Load -> Complete Crash"),

    (109, "exponential-backoff", "Exponential Backoff", "Prevent thundering herd storms by implementing exponential backoff with full jitter.",
     "Why does fixed-interval retrying create synchronized harmonic traffic spikes that repeatedly crash recovering servers?",
     "Exponential backoff doubles wait times; adding randomized jitter de-correlates retry timestamps across clients.",
     "python3 simulations/retries_exponential_backoff.py",
     "Wait Time = random(0, min(max_delay, base_delay * 2^attempt)) [Full Jitter]"),

    (110, "idempotency-and-network-retries", "Idempotency and Network Retries", "The Two Generals Problem: why network unreliability creates duplicated business transactions without idempotency keys.",
     "A client sends a $100 payment; the server charges the card, but the network drops the HTTP 200 OK response.",
     "The client cannot know whether the request succeeded or failed; retrying without an idempotency key double-charges.",
     "python3 simulations/idempotency_risk.py",
     "Client -> Charge $100 -> Server Charges -> Response Lost -> Client Retries -> Double Charge!"),

    (111, "partial-failure", "Partial Failure", "In distributed systems, nodes can be healthy while the network drops packets symmetrically or asymmetrically.",
     "Why is remote communication fundamentally different from a local function call?",
     "Local function calls always return or crash the process; remote network calls can succeed, fail, or hang indefinitely.",
     "cat docs/mental-models.md",
     "Node A (Healthy) <──Unreliable Partial Network──► Node B (Healthy)"),

    (112, "split-brain-concept", "Split-Brain Concept", "Network partitions split clusters into disconnected groups, risking concurrent conflicting state updates.",
     "What happens when a network partition cuts off communication between database master and replica?",
     "If both sides believe the peer is dead and elect themselves master, split-brain data corruption occurs.",
     "cat docs/mental-models.md",
     "Cluster Partitioned -> Group A elects Leader A | Group B elects Leader B -> Data Corruption"),

    (113, "dns-failure-lab", "DNS Failure Lab", "Diagnose NXDOMAIN, SERVFAIL, and resolver timeout failures inside an isolated environment.",
     "Experience the clinical difference between a broken domain name and an unreachable nameserver.",
     "Inspect /etc/resolv.conf, query with dig, check answering nameserver IP and DNS status code.",
     "cd broken-networks/lab-01-dns-nxdomain && cat README.md",
     "DNS Query -> Inspect dig output -> Check RCODE -> Remediate nameserver or record"),

    (114, "routing-failure-lab", "Routing Failure Lab", "Diagnose missing default gateways, broken static routes, and asymmetric routing drops.",
     "When ping fails with 'Network is unreachable', trace the kernel routing table to locate the missing route.",
     "ip route get reveals which route matched; missing default route requires adding gateway via ip route add.",
     "cd broken-networks/lab-03-default-gateway-missing && cat README.md",
     "ip route show -> Identify missing destination prefix -> Add route via gateway"),

    (115, "firewall-failure-lab", "Firewall Failure Lab", "Diagnose silent packet drops versus administrative TCP RST rejections using iptables.",
     "Differentiate an iptables -j DROP rule (silent timeout) from an iptables -j REJECT rule (immediate reset).",
     "iptables -L -n -v shows packet drop counters incrementing in real time.",
     "cd broken-networks/lab-08-firewall-drops-inbound-syn && cat README.md",
     "iptables -L -n -v -> Observe drop counter incrementing on target port -> Add ACCEPT rule"),

    (116, "wrong-port-lab", "Wrong Port Lab", "Diagnose connection refused errors caused by client-server port mismatches.",
     "A client connects to port 8000 while the server daemon listens on port 8080.",
     "ss -tulpn proves the actual listening port; client receives TCP RST immediately.",
     "cd broken-networks/lab-11-port-mismatch && cat README.md",
     "Client connects to 8000 -> TCP RST -> Run ss -tulpn -> Discover server listens on 8080"),

    (117, "bind-address-failure", "Bind Address Failure", "The classic production bug: service bound to 127.0.0.1 failing remote clients; binding to 0.0.0.0.",
     "Why does a service work perfectly when tested with curl on the host, but fail for remote users and Docker containers?",
     "Binding to 127.0.0.1 restricts the socket strictly to the loopback interface; binding to 0.0.0.0 accepts all interfaces.",
     "cd broken-networks/lab-10-service-listening-localhost-only && cat README.md",
     "127.0.0.1:8080 (Loopback only) ──Fix: Bind 0.0.0.0:8080──► Accessible to all interfaces"),

    (118, "mtu-failure-lab", "MTU Failure Lab", "Diagnose Path MTU Discovery black holes where ping succeeds but large HTTP payloads hang.",
     "An intermediate router drops 1500-byte packets while an upstream firewall blocks ICMP Type 3 Code 4.",
     "ping -M do -s 1472 succeeds at small sizes but fails at 1500 bytes; fix via TCP MSS clamping.",
     "cd broken-networks/lab-15-mtu-blackhole && cat README.md",
     "Small packet (64B) passes | Large packet (1500B) dropped silently -> Path MTU Black Hole"),

    (119, "broken-network-labs", "Broken Network Labs", "Master the 32 comprehensive hands-on troubleshooting labs spanning all network layers.",
     "Develop instinctive root-cause isolation across DNS, routing, firewalls, ports, NAT, and TLS.",
     "Follow the diagnostic protocol: Read symptoms, formulate hypothesis, verify with tools, fix, and check solution.",
     "cat broken-networks/README.md",
     "32 Real-World Failure Scenarios Cataloged in broken-networks/"),

    (120, "network-troubleshooting-framework", "Network Troubleshooting Framework", "The universal 14-step systematic isolation framework for resolving any production network incident.",
     "Internalize the deterministic, layer-by-layer sequence from DNS down to Ethernet and back up to HTTP.",
     "Never guess or restart services randomly during outages; follow the 14-step clinical ladder.",
     "cat docs/troubleshooting.md",
     "DNS -> Interface -> Subnet -> Route -> ARP -> Forwarding -> MTU -> Firewall -> Port -> Handshake -> TLS -> App"),

    (121, "project-raw-tcp-chat", "Project: Raw TCP Chat", "Build a multi-user conversational chat server from scratch using raw POSIX sockets and select().",
     "Implement non-blocking I/O multiplexing, client registration, and broadcast distribution in pure Python.",
     "The server multiplexes incoming sockets without blocking, broadcasting messages to all connected participants.",
     "python3 projects/01-raw-tcp-chat/chat_server.py & python3 projects/01-raw-tcp-chat/test_chat.py",
     "Client 1 (fd 4) ──► Chat Server (select) ──► Broadcasts to Client 2 (fd 5) & Client 3 (fd 6)"),

    (122, "project-http-server", "Project: HTTP Server", "Build an HTTP/1.1 web server from scratch directly on top of raw TCP sockets.",
     "Parse HTTP request lines, headers, CRLF delimiters, status codes, and handle Keep-Alive persistent connections.",
     "The server parses incoming ASCII requests and returns correctly formatted HTTP/1.1 status lines and headers.",
     "python3 projects/02-http-server/http_server.py & python3 projects/02-http-server/test_http.py",
     "TCP Stream ──► Parse Request Line ──► Parse Headers ──► Route URI ──► Return Status & Body"),

    (123, "project-dns-like-resolver", "Project: DNS-Like Resolver", "Build an RFC 1035 wire-compatible DNS server and caching engine over UDP.",
     "Decode DNS binary headers and length-prefixed QNAMEs; synthesize A-record responses parseable by dig.",
     "Querying with dig @127.0.0.1 -p 5353 example.com returns an RFC 1035 response with TTL.",
     "python3 projects/03-dns-resolver/dns_server.py & python3 projects/03-dns-resolver/test_dns.py",
     "UDP Socket (:5353) ──► Decode 12-byte Header & QNAME ──► In-Memory TTL Cache ──► Encode RFC 1035 Response"),

    (124, "project-router-simulator", "Project: Router Simulator", "Build a multi-homed IPv4 router performing Longest Prefix Match and Layer-2 MAC header rewrites.",
     "Implement trie-based prefix matching, TTL validation/decrement, IP checksum recalculation, and ARP resolution.",
     "Packets crossing the router retain end-to-end IP addresses while MAC addresses are rewritten and TTL decremented.",
     "python3 projects/04-router-simulator/router.py & python3 projects/04-router-simulator/test_router.py",
     "Ingress Frame (eth0) ──► LPM Route Lookup ──► Decrement TTL ──► Rewrite MACs ──► Egress Frame (eth1)"),

    (125, "project-reliable-transport-simulator", "Project: Reliable Transport Simulator", "Build a complete TCP-like reliable transport protocol with sliding windows and timeouts over lossy UDP.",
     "Implement 3-way handshakes, sequence numbers, cumulative ACKs, sliding windows, and retransmissions.",
     "Despite a 25% packet drop rate on the wire, the stream is reassembled in perfect byte order without corruption.",
     "python3 projects/05-reliable-transport/transport.py & python3 projects/05-reliable-transport/test_transport.py",
     "Stream Bytes ──► Sequence Segmentation ──► Sliding Window ──► Loss Recovery ──► Ordered Reassembly"),

    (126, "project-reverse-proxy", "Project: Reverse Proxy", "Build an HTTP reverse proxy supporting round-robin routing and active background health checks.",
     "Terminate client sockets, enrich request headers (X-Forwarded-For), and prune failing backend nodes.",
     "Client requests are balanced across backends, and dead backends are evicted dynamically by health probes.",
     "python3 projects/06-reverse-proxy/reverse_proxy.py & python3 projects/06-reverse-proxy/test_proxy.py",
     "Client Connection ──► Reverse Proxy (:8000) ──► Upstream Backend Pool (Round Robin & Health Checks)"),

    (127, "project-load-balancer", "Project: Load Balancer", "Build an L7 load balancer supporting Round-Robin, Least Connections, and IP Hash algorithms.",
     "Observe how Least-Connections dynamically steers traffic away from slow backends to protect latency.",
     "Least-Connections directs requests to the node with lowest active in-flight connections during slowness.",
     "python3 projects/07-load-balancer/load_balancer.py & python3 projects/07-load-balancer/test_lb.py",
     "Incoming Traffic ──► Load Balancer ──► Least-Connections Scheduler ──► Upstream Backends"),

    (128, "project-tiny-internet", "Project: Tiny Internet", "Construct an isolated multi-network Internet topology inside 4 Linux namespaces.",
     "Link Client LAN, Transit Backbone, and Server LAN across multiple router hops with DNS and HTTP services.",
     "Traceroute from Client namespace traces across both routers to the destination server namespace.",
     "python3 projects/08-tiny-internet/verify_tiny_internet.py",
     "Client LAN (10.10.1.0/24) ──► Router A ──► Transit (172.16.0.0/30) ──► Router B ──► Server LAN (10.20.1.0/24)"),

    (129, "project-production-like-web-path", "Project: Production-Like Web Path", "Trace a multi-tier microservice architecture: Client -> DNS -> Edge Proxy -> Load Balancer -> App -> DB.",
     "Trace end-to-end request latencies and inject DNS, worker crash, and database timeout failures.",
     "Tracer records millisecond breakdown across DNS, TCP connect, reverse proxy, worker, and database query.",
     "python3 projects/09-production-web-path/production_topology.py",
     "Client ──► DNS ──► Edge Reverse Proxy ──► Load Balancer ──► App Instances ──► Database Backend"),

    (130, "networking-and-docker", "Networking and Docker", "Deconstruct Docker container networking: namespaces, veth pairs, docker0 bridge, and iptables NAT.",
     "Understand why Docker port publishing (-p 8080:80) is simply a Linux kernel DNAT rule in the PREROUTING chain.",
     "Docker allocates a private network namespace, creates a veth pair to docker0, and masquerades egress with iptables.",
     "docker network inspect bridge 2>/dev/null || ip link show docker0 2>/dev/null || true",
     "Container -> Namespace veth -> docker0 Bridge -> iptables MASQUERADE -> Host Physical NIC"),

    (131, "networking-and-kubernetes", "Networking and Kubernetes", "Understand the Kubernetes Pod network model, CNI plugins, ClusterIP kube-proxy routing, and NodePort.",
     "How do Pods across different nodes communicate directly without NAT, and how does ClusterIP load balance?",
     "Every Pod gets its own IP; kube-proxy programs iptables or IPVS to redirect ClusterIP to Pod endpoints.",
     "cat docs/mental-models.md",
     "Pod A -> CNI Overlay / Direct Route -> Node Network -> kube-proxy iptables -> Pod B"),

    (132, "networking-and-aws", "Networking and AWS", "Map physical networking concepts to AWS cloud primitives: VPC, CIDR Subnets, Route Tables, IGW, NAT GW, SG, and NACL.",
     "Demystify cloud networking acronyms by recognizing they are identical to standard Linux network mechanisms.",
     "VPC is a virtual network; Subnets are CIDR blocks; Route Tables are kernel routes; SGs are stateful iptables.",
     "cat docs/mental-models.md",
     "AWS VPC (Network) <-> Route Table (ip route) <-> Internet Gateway (Router) <-> Security Group (iptables)"),

    (133, "networking-and-databases", "Networking and Databases", "Why database engineering cares deeply about connection pooling, round trips, timeouts, and replication links.",
     "Why does executing 50 individual SQL queries over a 10ms network link cause transactions to take over 500ms?",
     "Network round trips dominate database query latency; batching and connection pooling are mandatory.",
     "python3 benchmarks/connection_pool_benchmark.py",
     "Application -> Persistent Pool -> Database Engine (Amortizes 3-way handshake & TLS)"),

    (134, "networking-and-redis", "Networking and Redis", "Why Redis throughput is dominated by network round-trip latency, and how pipelining unlocks 100x speedups.",
     "How does Redis's single-threaded event loop achieve 100,000+ ops/sec over network sockets?",
     "Redis execution is sub-microsecond in memory; network RTT is the bottleneck; pipelining batches commands.",
     "python3 benchmarks/pipelining_benchmark.py",
     "Sequential: Command -> RTT -> Reply -> Command | Pipelined: Batch 1000 Commands -> 1 RTT -> Batch 1000 Replies"),

    (135, "networking-and-kafka", "Networking and Kafka", "How Kafka achieves line-rate throughput via OS zero-copy (sendfile), batching, and sequential I/O.",
     "Why is Kafka able to saturate 10 Gbps and 100 Gbps network cards without burning CPU in user space?",
     "sendfile() transfers data directly from page cache to socket buffer without copying into user space memory.",
     "python3 benchmarks/throughput_benchmark.py",
     "Disk Page Cache ──sendfile() zero-copy──► Kernel Socket Buffer ──► NIC Ring Buffer"),

    (136, "networking-and-distributed-systems", "Networking and Distributed Systems", "The fallacies of distributed computing: the network is not reliable, latency is not zero, and bandwidth is not infinite.",
     "Why can distributed consensus protocols (Raft, Paxos) never assume synchronous network delivery?",
     "Networks delay, drop, reorder, and partition; systems must use heartbeats, leases, and quorum majorities.",
     "cat docs/mental-models.md",
     "Asynchronous Network Model: Messages can be arbitrarily delayed, dropped, or partitioned"),

    (137, "networking-in-system-design", "Networking in System Design", "Calculating network budgets in system architecture: estimating bandwidth, latency constraints, and connection concurrency.",
     "How do senior system architects design global distributed systems within strict physical network constraints?",
     "Budget every millisecond: DNS (0ms cached), TCP connect (1 RTT), TLS (1 RTT), data transfer (BDP), backend hops.",
     "python3 simulations/latency_components.py",
     "Network Budgeting: Who talks to whom? What protocol? How many hops? What RTT? What timeout?"),

    (138, "final-mental-model", "Final Mental Model", "Tracing curl https://example.com/api end-to-end through all 14 layers of reality from process syscall to optical wire and back.",
     "Synthesize every single concept learned in this curriculum into one coherent, transparent mental model.",
     "Trace shell command -> DNS resolution -> routing table -> ARP -> TCP handshake -> TLS 1.3 -> HTTP GET -> Proxy -> App.",
     "curl -v https://example.com",
     "curl -> DNS -> Route -> ARP -> TCP -> TLS -> HTTP -> Proxy -> Load Balancer -> App -> DB"),
]


def generate_all_phases():
    os.makedirs(PHASES_DIR, exist_ok=True)
    evidence_template_src = os.path.join(REPO_ROOT, "outputs", "evidence-template.md")

    for num, slug, title, motto, problem, pred, code_hint, mental_model in PHASE_DEFS:
        phase_folder_name = f"{num:02d}-{slug}"
        phase_path = os.path.join(PHASES_DIR, phase_folder_name)
        docs_path = os.path.join(phase_path, "docs")
        code_path = os.path.join(phase_path, "code")
        exp_path = os.path.join(phase_path, "experiments")
        out_path = os.path.join(phase_path, "outputs")

        for d in [docs_path, code_path, exp_path, out_path]:
            os.makedirs(d, exist_ok=True)

        # Copy evidence template
        if os.path.exists(evidence_template_src):
            shutil.copyfile(evidence_template_src, os.path.join(out_path, "evidence-template.md"))

        # Generate docs/en.md following LESSON_TEMPLATE.md
        lesson_content = f"""# Lesson {num:02d}: {title}

> **Motto**: {motto}

---

## Motto
"{motto}"

## Problem
{problem}

## Prediction
{pred}

## Why this matters
Ignorance of this mechanism causes engineers to guess blindly when systems fail. Understanding the mechanical interaction at this layer transforms mysterious outages into transparent, debuggable states.

## First principles
Deriving from ground truth: communication requires a sender, a receiver, an encoding scheme, and a physical medium. When processes run on separate machines, the operating system kernel must package state into standardized wire formats governed by mathematical and physical constraints.

## Mental model
```text
{mental_model}
```

## Build / simulate it
Review the associated implementation or simulation:
```bash
{code_hint}
```

## Configure the network
Ensure an isolated laboratory environment is active:
```bash
# Verify host or namespace isolation
./scripts/check-environment.sh
```

## Send traffic
Generate real or simulated traffic across the network interface:
```bash
# Execute test command
{code_hint}
```

## Capture it
Inspect the actual wire frames or socket states:
```bash
sudo tcpdump -i any -nn -c 4 2>/dev/null || ss -tan
```

## Measure it
Quantify performance metrics:
- Latency / Round-Trip Time
- Serialization Delay
- Packet Drop / Retransmission Count

## Break it
Inject an intentional failure to observe divergence from expected behavior:
```bash
# Fault injection example: close listening port, corrupt route, or alter MTU
```

## Trace it
Isolate the failing layer without guessing:
```bash
ip route show
ss -tulpn
```

## Debug it
Formulate your hypothesis, gather proving evidence, and restore configuration to verify recovery.

## Modify it
Challenge: Alter a parameter (e.g. timeout duration, prefix length, buffer size) and predict the resulting behavioral shift before testing.

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What exact state or error proves whether this layer succeeded or failed?
2. What happens to in-flight packets if intermediate network state is lost?
3. How does this mechanism scale when traffic increases by 100x?

## Production connection
How this manifests in cloud architectures (AWS VPC, Security Groups), container platforms (Docker, Kubernetes CNI), and distributed datastores (PostgreSQL, Redis, Kafka).

## What comes next
Having understood {title.lower()}, we next discover its inherent boundaries and transition to the next layer of abstraction.
"""
        with open(os.path.join(docs_path, "en.md"), "w") as f:
            f.write(lesson_content.strip() + "\n")

    print(f"Successfully generated all {len(PHASE_DEFS)} curriculum phases (00 to {len(PHASE_DEFS)-1})!")


if __name__ == "__main__":
    generate_all_phases()
