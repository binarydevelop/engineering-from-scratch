#!/usr/bin/env python3
"""
scripts/generate_packet_captures.py
Generates the 20 packet-capture exercises with predictions, tcpdump filters,
annotated wire dissections, and mastery questions.
"""

import os

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PCAP_DIR = os.path.join(REPO_ROOT, "packet-captures")

EXERCISES = [
    ("01-arp-resolution", "ARP Request & Reply", "arp", "Resolve local MAC address",
     "Frame 1: Broadcast Who has 10.0.1.20? Tell 10.0.1.10\nFrame 2: Unicast 10.0.1.20 is at 52:54:00:22:22:22",
     "Why is the ARP request sent to ff:ff:ff:ff:ff:ff, but the reply is unicast?"),

    ("02-icmp-echo-ping", "ICMP Echo Request & Reply", "icmp", "Verify Layer-3 reachability",
     "Packet 1: IP 10.0.1.10 > 10.0.1.20: ICMP echo request, id 1234, seq 1\nPacket 2: IP 10.0.1.20 > 10.0.1.10: ICMP echo reply, id 1234, seq 1",
     "What field links an ICMP Echo Reply to its corresponding Request?"),

    ("03-dns-a-record-query", "DNS Standard Query & Response", "udp port 53", "Resolve name to IP",
     "Packet 1: IP 10.0.1.10.54321 > 1.1.1.1.53: [udp sum ok] 0x1234+ A? example.com. (29)\nPacket 2: IP 1.1.1.1.53 > 10.0.1.10.54321: 0x1234 1/0/0 example.com. A 93.184.216.34 (45)",
     "How does the client know that a response packet belongs to its specific query?"),

    ("04-tcp-three-way-handshake", "TCP 3-Way Handshake", "tcp[tcpflags] & (tcp-syn|tcp-ack) != 0", "Establish TCP connection",
     "1. Client > Server: Flags [S], seq 1000, win 65495, options [mss 1460,sackOK]\n2. Server > Client: Flags [S.], seq 2000, ack 1001, win 65483\n3. Client > Server: Flags [.], ack 2001, win 65495",
     "Why does the SYN packet consume 1 sequence number even though it carries 0 bytes of payload?"),

    ("05-tcp-data-transfer-ack", "TCP Data Transfer & ACKs", "tcp and port 80", "Transmit application stream",
     "Packet 1: Client > Server: Flags [P.], seq 1001:1051, ack 2001 (50 bytes HTTP GET)\nPacket 2: Server > Client: Flags [.], ack 1051 (ACK acknowledging 50 bytes)",
     "What does the PSH (Push) flag instruct the receiving kernel stack to do?"),

    ("06-tcp-four-way-close", "TCP Connection Teardown (FIN-ACK)", "tcp[tcpflags] & (tcp-fin|tcp-ack) != 0", "Gracefully terminate connection",
     "1. Client > Server: Flags [F.], seq 1051, ack 2001\n2. Server > Client: Flags [.], ack 1052\n3. Server > Client: Flags [F.], seq 2001, ack 1052\n4. Client > Server: Flags [.], ack 2002",
     "Which side enters the TIME_WAIT state, and why?"),

    ("07-tcp-rst-connection-refused", "TCP RST (Connection Refused)", "tcp[tcpflags] & tcp-rst != 0", "Port closed rejection",
     "1. Client > Server: Flags [S], seq 1000, dport 9999\n2. Server > Client: Flags [R.], seq 0, ack 1001, win 0",
     "Why does the kernel return RST with ack=seq+1 instead of silently ignoring the packet?"),

    ("08-tcp-retransmission", "TCP Packet Loss & Retransmission", "tcp and port 8080", "Recover lost segment",
     "1. Client > Server: Flags [P.], seq 1001:1021 (lost in transit)\n2. Client > Server: Flags [P.], seq 1021:1041 (Server generates Dup ACK 1001)\n3. Client > Server: Retransmit seq 1001:1021",
     "How many duplicate ACKs trigger Fast Retransmit before RTO expires?"),

    ("09-udp-datagram-echo", "UDP Datagram Transmission", "udp and port 9999", "Send independent datagram",
     "Packet 1: Client.54321 > Server.9999: UDP, length 12\nPacket 2: Server.9999 > Client.54321: UDP, length 12",
     "What happens to the application when an intermediate router drops a UDP packet?"),

    ("10-http-get-response", "Plaintext HTTP/1.1 Request/Response", "tcp port 80", "Exchange application data",
     "1. Client > Server: GET /index.html HTTP/1.1\\r\\nHost: example.com\n2. Server > Client: HTTP/1.1 200 OK\\r\\nContent-Length: 45\\r\\n\\r\\n<html>...</html>",
     "How does HTTP/1.1 delineate where the headers end and the body begins?"),

    ("11-http-keepalive", "HTTP Persistent Connection Reuse", "tcp port 8080", "Reuse TCP handshake",
     "Request 1 and Request 2 exchange payloads sequentially over the exact same (src_ip, src_port <-> dst_ip, 8080) 4-tuple.",
     "What performance advantage does Keep-Alive provide over opening a new TCP connection?"),

    ("12-tls13-handshake", "TLS 1.3 Handshake Metadata", "tcp port 443", "Encrypt connection",
     "1. Client > Server: ClientHello (Cipher Suites, Supported Groups, Key Share)\n2. Server > Client: ServerHello, ChangeCipherSpec, EncryptedExtensions, Finished",
     "Why does TLS 1.3 require only 1 round-trip time (1-RTT) compared to TLS 1.2's 2-RTT?"),

    ("13-snat-translation", "Source NAT (SNAT / Masquerade)", "ip and port 80", "Translate private client IP",
     "Before NAT: 10.0.1.10:54321 > 93.184.216.34:80\nAfter NAT:  203.0.113.1:61000 > 93.184.216.34:80",
     "What Linux kernel table maintains the mapping between internal and external IP:Port tuples?"),

    ("14-dnat-port-forward", "Destination NAT (DNAT / Port Forwarding)", "tcp port 8080", "Forward external port to internal service",
     "Ingress on Host:  203.0.113.10:8080 > 192.168.1.1:8080\nForwarded to App: 203.0.113.10:8080 > 10.0.2.10:80",
     "Why must DNAT rules be placed in the PREROUTING chain rather than the POSTROUTING chain?"),

    ("15-traceroute-ttl-exceeded", "Traceroute (ICMP Time Exceeded)", "icmp or udp", "Discover network path hops",
     "Packet 1: Probe sent with TTL=1\nPacket 2: Router 1 > Client: ICMP time exceeded in-transit (Type 11 Code 0)",
     "Why do some hops in traceroute output display as asterisks (* * *)?"),

    ("16-icmp-dest-unreachable", "ICMP Destination Unreachable", "icmp", "Handle routing/firewall drops",
     "Router > Client: ICMP 10.0.2.50 unreachable - host unreachable (Type 3 Code 1)",
     "What is the difference between ICMP Code 1 (Host Unreachable) and Code 3 (Port Unreachable)?"),

    ("17-ipv6-neighbor-solicitation", "IPv6 Neighbor Discovery (NDP)", "icmp6", "Resolve IPv6 link-layer address",
     "Packet 1: ICMPv6 neighbor solicitation, who has fe80::2 (Multicast)\nPacket 2: ICMPv6 neighbor advertisement, tgt is fe80::2 (Unicast)",
     "Why did IPv6 eliminate broadcast ARP in favor of multicast Neighbor Solicitation?"),

    ("18-path-mtu-fragmentation", "Path MTU Discovery (PMTUD)", "icmp or (ip[6:2] & 0x3fff != 0)", "Detect path MTU boundaries",
     "Router > Sender: ICMP 10.0.2.20 unreachable - need to frag (mtu 1400) (Type 3 Code 4)",
     "What happens if an upstream enterprise firewall blocks all ICMP Type 3 Code 4 packets?"),

    ("19-reverse-proxy-hop", "Reverse Proxy Two-Legged Transfer", "port 80 or port 8080", "Inspect client vs backend hops",
     "Leg 1: Client > Proxy:80 (GET / HTTP/1.1)\nLeg 2: Proxy:52000 > Backend:8080 (GET / HTTP/1.1\\r\\nX-Forwarded-For: ClientIP)",
     "Why does the backend application server see the reverse proxy's IP address as the socket source?"),

    ("20-connection-pool-reuse", "Persistent Database Connection Pool", "tcp port 5432", "Amortize connection setup overhead",
     "Multiple SQL queries executed over established TCP connection with 0 SYN/FIN packets exchanged.",
     "Why is connection pooling critical for high-throughput relational database workloads?"),
]


def generate_pcaps():
    os.makedirs(PCAP_DIR, exist_ok=True)

    master_readme_lines = [
        "# 20 Practical Packet Capture Exercises",
        "",
        "> **Philosophy**: If you cannot predict what tcpdump will display before sending a packet, you are guessing. Always formulate a hypothesis, record wire frames, and dissect the headers.",
        "",
        "## Master Capture Index",
        "",
        "| ID | Exercise | Protocol Filter | Core Objective |",
        "| :--- | :--- | :--- | :--- |",
    ]

    for dir_name, title, filter_exp, obj, dissection, question in EXERCISES:
        ex_dir = os.path.join(PCAP_DIR, dir_name)
        os.makedirs(ex_dir, exist_ok=True)

        master_readme_lines.append(f"| **{dir_name[:2]}** | [{title}]({dir_name}/) | `{filter_exp}` | {obj} |")

        content = f"""# Packet Capture Exercise: {title}

> **Motto**: Understand it. Predict it. Send it. Capture it. Dissect it.

---

## 1. Objective
{obj}.

## 2. Hypothesis & Packet Prediction
Before running the capture, predict the sequence of frames:
```text
┌───────────────────────┬────────────────────────────────────────────────────────┐
│ Header Layer          │ Predicted Values / Flags                               │
├───────────────────────┼────────────────────────────────────────────────────────┤
│ Layer 2 (Ethernet II) │ Source MAC, Destination MAC, EtherType                 │
│ Layer 3 (IP)          │ Source IP, Destination IP, TTL, Protocol               │
│ Layer 4 (Transport)   │ Source Port, Destination Port, Flags, Seq/Ack          │
│ Layer 7 (Application) │ Command / Payload / Delimiters                         │
└───────────────────────┴────────────────────────────────────────────────────────┘
```

## 3. tcpdump Capture Command
```bash
sudo tcpdump -i <interface> -nn -vvv -s0 "{filter_exp}"
```

## 4. Annotated Wire Dissection
```text
{dissection}
```

## 5. Mastery Reasoning Question
> **Question**: {question}

Document your empirical findings in `outputs/evidence-template.md`.
"""
        with open(os.path.join(ex_dir, "README.md"), "w") as f:
            f.write(content.strip() + "\n")

    with open(os.path.join(PCAP_DIR, "README.md"), "w") as f:
        f.write("\n".join(master_readme_lines) + "\n")

    print(f"Successfully generated all {len(EXERCISES)} packet capture exercises!")


if __name__ == "__main__":
    generate_pcaps()
