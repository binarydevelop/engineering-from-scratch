# Comprehensive Networking Glossary

> Precise, rigorous definitions of core networking primitives, protocols, abstractions, and mechanisms.

---

### A
- **ACK (Acknowledgment)**: A control flag and field in the TCP header indicating that the sender has successfully received bytes up to the specified acknowledgment sequence number.
- **Address Resolution Protocol (ARP)**: An RFC 826 protocol used on IPv4 networks to dynamically map a 32-bit Internet Protocol (IP) address to a 48-bit media access control (MAC) link-layer address.
- **Autonomous System (AS)**: A collection of connected Internet Protocol routing prefixes under the control of one or more network operators on behalf of a single administrative entity that presents a common routing policy to the Internet.

### B
- **Bandwidth**: The maximum rate of data transfer across a given path, measured in bits per second (bps, Mbps, Gbps).
- **Bandwidth-Delay Product (BDP)**: The product of a data link's capacity (bandwidth) and its round-trip time (RTT). Represents the maximum amount of data "in flight" needed to fully saturate the pipe.
- **BGP (Border Gateway Protocol)**: The standardized exterior gateway protocol designed to exchange routing and reachability information among autonomous systems on the Internet (RFC 4271).
- **Bridge**: A Layer-2 hardware or software device that connects multiple network segments, filtering and forwarding frames based on MAC addresses.
- **Broadcast Domain**: A logical division of a computer network in which all nodes can reach each other by broadcast at the data link layer. Terminated by routers.
- **Bufferbloat**: High latency and packet jitter in packet-switched networks caused by excess buffering of packets in network switches, routers, and host network stacks.

### C
- **CIDR (Classless Inter-Domain Routing)**: A method for allocating IP addresses and routing IP packets that replaced class-based allocation, allowing flexible subnet prefixes specified by prefix length (e.g. `/24`).
- **CAM Table (Content Addressable Memory)**: The table inside an Ethernet switch mapping learned MAC addresses to physical or virtual switch ports.
- **Checksum**: A fixed-size redundancy check value computed over header or payload bytes to detect transmission corruption.
- **CNI (Container Network Interface)**: A Cloud Native Computing Foundation specification and set of libraries for configuring network interfaces in Linux containers.
- **Congestion Window (cwnd)**: A TCP state variable maintained by the sender that limits the amount of data the sender can transmit into the network before receiving an acknowledgment.
- **Connection Tracking (conntrack)**: The kernel subsystem (part of Netfilter) that tracks the state of active network connections (NAT, stateful firewalls).

### D
- **Datagram**: An independent, self-contained packet of information sent over the network with no guarantees of delivery, arrival time, or order (e.g. UDP, IP).
- **Default Gateway**: The node (typically a router) on a computer network that the host network stack uses when no specific route matches the destination IP address.
- **DNAT (Destination NAT)**: Rewriting the destination IP address and/or port number of an incoming packet before routing it to an internal service.
- **DNS (Domain Name System)**: A hierarchical, distributed database that translates human-readable hostnames into numeric IP addresses (RFC 1034/1035).

### E
- **Encapsulation**: The process of packaging data inside protocol headers and trailers as it moves down the network stack (Data -> Segment -> Packet -> Frame).
- **Ephemeral Port**: A short-lived transport protocol port automatically allocated by the IP stack from a predefined range (e.g., 32768–60999 in Linux) for outbound client connections.
- **Ethernet**: A family of wired computer networking technologies commonly used in local area networks (LANs), standardized as IEEE 802.3.
- **EtherType**: A two-octet field in an Ethernet frame used to indicate which protocol is encapsulated in the payload (e.g., `0x0800` for IPv4, `0x86DD` for IPv6, `0x0806` for ARP).

### F
- **Fast Retransmit**: A TCP enhancement that retransmits a lost segment upon receiving three duplicate ACKs without waiting for the retransmission timer (RTO) to expire.
- **File Descriptor (FD)**: An unsigned integer index used by the operating system kernel to identify open file tables, including network sockets.
- **Flow Control**: A mechanism (such as TCP advertised receive window) that ensures a sender does not transmit data faster than the receiving process can process and buffer it.
- **Fragmentation**: The process of breaking an IP packet into smaller packets if its size exceeds the Maximum Transmission Unit (MTU) of the outgoing link.

### H
- **Hop Limit**: An 8-bit field in the IPv6 header that replaces IPv4's Time-To-Live (TTL); decremented by 1 at each router hop to prevent infinite loops.
- **HTTP (Hypertext Transfer Protocol)**: An application-layer protocol for distributed, collaborative, hypermedia information systems (RFC 9112).
- **HTTPS**: HTTP communication secured using Transport Layer Security (TLS).

### I
- **ICMP (Internet Control Message Protocol)**: A network-layer protocol used by network devices to send error messages and operational information (RFC 792).
- **Idempotency**: A property of an operation whereby it can be applied multiple times without changing the result beyond the initial application (e.g. HTTP GET, PUT, DELETE).
- **IP Address**: A numerical label assigned to each device connected to a computer network that uses the Internet Protocol for communication.

### L
- **Link-Local Address**: An IP address intended only for communications within the local network segment. In IPv6, prefixes under `fe80::/10`.
- **Listening Socket**: A passive TCP socket created via `listen()` that waits for incoming connection requests.
- **Load Balancer**: A device or software reverse proxy that distributes network or application traffic across multiple backend servers.
- **Longest Prefix Match (LPM)**: The routing algorithm used by routers and host stacks to select the most specific route entry (the one with the largest subnet mask) that matches a destination IP.
- **Loopback**: A pseudo-network interface (`lo`) enabling a client to communicate with a server on the same host machine without transmitting data across external physical links.

### M
- **MAC Address**: Media Access Control address; a unique 48-bit identifier assigned to a network interface controller for communications on a data link network segment.
- **Maximum Transmission Unit (MTU)**: The largest packet size, in bytes, that a network link can transmit without fragmentation. Standard Ethernet MTU is 1500 bytes.
- **Maximum Segment Size (MSS)**: The largest amount of data, in bytes, that a computer can receive in a single TCP segment (MTU minus IP and TCP header overhead).

### N
- **Network Namespace (`netns`)**: A Linux kernel virtualization feature that provides an isolated copy of the network stack, including routing tables, interfaces, firewall chains, and sockets.
- **Netfilter**: A framework inside the Linux kernel that provides hooks for packet filtering, network address translation, and port translation.
- **nftables**: The modern successor to iptables, ip6tables, arptables, and ebtables in the Linux kernel.

### P
- **Path MTU Discovery (PMTUD)**: A standardized technique (RFC 1191/8201) for determining the maximum transmission unit size on the network path between two IP hosts without fragmentation.
- **Port**: A 16-bit numerical identifier in transport layer protocols (TCP, UDP) used to distinguish between different services running on the same host.
- **Proxy**: An intermediary server that acts as an agent on behalf of clients or servers to facilitate network requests.

### Q
- **Queueing Delay**: The time a packet spends waiting in network device queues or operating system socket buffers before transmission or processing.
- **QUIC**: A general-purpose transport layer network protocol designed by Google and standardized in RFC 9000, running on top of UDP with integrated TLS 1.3 encryption.

### R
- **Round-Trip Time (RTT)**: The duration, in milliseconds, it takes for a data packet to be sent from source to destination plus the time it takes for an acknowledgment of that packet to be received at the source.
- **Routing Table**: A data structure stored in a router or networked computer that lists the routes to particular network destinations and associated metrics.

### S
- **Sliding Window**: A flow control and reliability algorithm where the sender can transmit multiple segments before receiving an acknowledgment, sliding the valid window forward as ACKs arrive.
- **SNAT (Source NAT)**: Modifying the source IP address and/or source port of an outbound packet to mask the identity of the internal origin host.
- **Socket**: An operating system abstraction representing an endpoint for communication between processes across a computer network.
- **Subnet Mask**: A 32-bit number that divides an IPv4 address into network address and host address components via bitwise AND.
- **SYN (Synchronize)**: The initial TCP control flag sent during the three-way handshake to establish a connection and synchronize initial sequence numbers.

### T
- **TCP (Transmission Control Protocol)**: A connection-oriented, reliable, ordered, byte-stream transport protocol (RFC 9293).
- **Time-to-Live (TTL)**: An 8-bit field in IPv4 packets decremented by 1 at each router hop; packet is discarded with an ICMP Time Exceeded message if it reaches 0.
- **TIME_WAIT**: A TCP socket state entered by the endpoint that actively closed the connection, waiting for $2 \times \text{MSL}$ to ensure the remote end received the final ACK.
- **TLS (Transport Layer Security)**: A cryptographic protocol designed to provide end-to-end communication security over a computer network (RFC 8446).

### U
- **UDP (User Datagram Protocol)**: A simple connectionless transport protocol offering minimal packet transmission service without reliability guarantees (RFC 768).

### V
- **Virtual Ethernet (`veth`)**: A Linux virtual network device configured in pairs; packets transmitted into one end are instantly received at the other end.
