# 20 Practical Packet Capture Exercises

> **Philosophy**: If you cannot predict what tcpdump will display before sending a packet, you are guessing. Always formulate a hypothesis, record wire frames, and dissect the headers.

## Master Capture Index

| ID | Exercise | Protocol Filter | Core Objective |
| :--- | :--- | :--- | :--- |
| **01** | [ARP Request & Reply](01-arp-resolution/) | `arp` | Resolve local MAC address |
| **02** | [ICMP Echo Request & Reply](02-icmp-echo-ping/) | `icmp` | Verify Layer-3 reachability |
| **03** | [DNS Standard Query & Response](03-dns-a-record-query/) | `udp port 53` | Resolve name to IP |
| **04** | [TCP 3-Way Handshake](04-tcp-three-way-handshake/) | `tcp[tcpflags] & (tcp-syn|tcp-ack) != 0` | Establish TCP connection |
| **05** | [TCP Data Transfer & ACKs](05-tcp-data-transfer-ack/) | `tcp and port 80` | Transmit application stream |
| **06** | [TCP Connection Teardown (FIN-ACK)](06-tcp-four-way-close/) | `tcp[tcpflags] & (tcp-fin|tcp-ack) != 0` | Gracefully terminate connection |
| **07** | [TCP RST (Connection Refused)](07-tcp-rst-connection-refused/) | `tcp[tcpflags] & tcp-rst != 0` | Port closed rejection |
| **08** | [TCP Packet Loss & Retransmission](08-tcp-retransmission/) | `tcp and port 8080` | Recover lost segment |
| **09** | [UDP Datagram Transmission](09-udp-datagram-echo/) | `udp and port 9999` | Send independent datagram |
| **10** | [Plaintext HTTP/1.1 Request/Response](10-http-get-response/) | `tcp port 80` | Exchange application data |
| **11** | [HTTP Persistent Connection Reuse](11-http-keepalive/) | `tcp port 8080` | Reuse TCP handshake |
| **12** | [TLS 1.3 Handshake Metadata](12-tls13-handshake/) | `tcp port 443` | Encrypt connection |
| **13** | [Source NAT (SNAT / Masquerade)](13-snat-translation/) | `ip and port 80` | Translate private client IP |
| **14** | [Destination NAT (DNAT / Port Forwarding)](14-dnat-port-forward/) | `tcp port 8080` | Forward external port to internal service |
| **15** | [Traceroute (ICMP Time Exceeded)](15-traceroute-ttl-exceeded/) | `icmp or udp` | Discover network path hops |
| **16** | [ICMP Destination Unreachable](16-icmp-dest-unreachable/) | `icmp` | Handle routing/firewall drops |
| **17** | [IPv6 Neighbor Discovery (NDP)](17-ipv6-neighbor-solicitation/) | `icmp6` | Resolve IPv6 link-layer address |
| **18** | [Path MTU Discovery (PMTUD)](18-path-mtu-fragmentation/) | `icmp or (ip[6:2] & 0x3fff != 0)` | Detect path MTU boundaries |
| **19** | [Reverse Proxy Two-Legged Transfer](19-reverse-proxy-hop/) | `port 80 or port 8080` | Inspect client vs backend hops |
| **20** | [Persistent Database Connection Pool](20-connection-pool-reuse/) | `tcp port 5432` | Amortize connection setup overhead |
