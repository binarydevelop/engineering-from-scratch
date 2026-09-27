# Packet-Level Debugging Methodology

> "Logs tell you what an application thinks happened. Wire packets tell you what actually happened."

---

## 1. The 4-Question Packet Hypothesis

Whenever any network connection stalls, times out, or fails unpredictably, do not speculate. Perform simultaneous packet captures on sender and receiver (or intermediate hops) and answer these four questions in order:

```text
       SENDER                                          RECEIVER
┌──────────────────┐                            ┌──────────────────┐
│ [1] Did packet   │                            │ [2] Did packet   │
│ leave interface? ├────────────► ─────────────►│ reach interface? │
└──────────────────┘                            └────────┬─────────┘
                                                         │
                                                Process evaluates
                                                         │
┌──────────────────┐                            ┌────────▼─────────┐
│ [4] Did reply    │                            │ [3] Did receiver │
│ return?          │◄─────────── ◄──────────────┤ reply?           │
└──────────────────┘                            └──────────────────┘
```

| Result | Diagnosis | What to Check |
| :--- | :--- | :--- |
| **Fails at [1]** | Packet never left sender. | Local routing table (`ip route get`), local firewall (`iptables -L`), interface DOWN, ARP resolution failed. |
| **Succeeds at [1], fails at [2]** | Packet dropped in transit. | Upstream router missing route, MTU drop, intermediate cloud security group/NACL drop, network partition. |
| **Succeeds at [2], fails at [3]** | Receiver dropped or ignored packet. | Receiver firewall, service not listening on port, application backlog full, loopback-only bind address. |
| **Succeeds at [3], fails at [4]** | Return path broken. | Asymmetric routing drop, receiver missing reverse default gateway, stateful firewall tracking timeout. |

---

## 2. Essential tcpdump Flags & Discipline

```bash
sudo tcpdump -i <interface> -nn -s0 -vvv -l
```
- `-i <interface>`: Selects interface (`eth0`, `veth-client`, `lo`, or `any`).
- `-nn`: Do not resolve hostnames (prevents recursive DNS latency) and do not resolve port numbers (shows `80` instead of `http`).
- `-s0`: Capture the entire packet payload (snaplen 0 = unlimited).
- `-vvv`: Verbose protocol decoding (shows TTL, IP ID, TCP options, window scaling).
- `-l`: Line-buffered output (essential when piping to `grep` or `tee`).

---

## 3. High-Value Berkeley Packet Filter (BPF) Expressions

```bash
# Capture traffic for a specific host
tcpdump -i eth0 -nn host 192.168.1.50

# Capture only TCP SYN packets (Handshake initiation)
tcpdump -i eth0 -nn "tcp[tcpflags] & (tcp-syn) != 0 and tcp[tcpflags] & (tcp-ack) == 0"

# Capture TCP RST packets (Connection Refused / Aborts)
tcpdump -i eth0 -nn "tcp[tcpflags] & (tcp-rst) != 0"

# Capture DNS queries and responses (UDP port 53)
tcpdump -i eth0 -nn udp port 53

# Capture ARP requests and replies
tcpdump -i eth0 -nn arp

# Capture ICMP error messages (excluding Echo Request/Reply)
tcpdump -i eth0 -nn "icmp and icmp[0] != 8 and icmp[0] != 0"

# Capture packets matching specific port range
tcpdump -i eth0 -nn portrange 8000-8080
```

---

## 4. Reading tcpdump Output: Wire Signatures

### Wire Signature 1: Normal TCP 3-Way Handshake
```text
12:00:01.100 IP 10.0.1.10.54321 > 10.0.2.20.80: Flags [S], seq 1000, win 65495, options [mss 1460,sackOK,TS val 1234 ecr 0], length 0
12:00:01.102 IP 10.0.2.20.80 > 10.0.1.10.54321: Flags [S.], seq 2000, ack 1001, win 65483, options [mss 1460,sackOK,TS val 5678 ecr 1234], length 0
12:00:01.102 IP 10.0.1.10.54321 > 10.0.2.20.80: Flags [.], ack 2001, win 65495, options [TS val 1235 ecr 5678], length 0
```
- Line 1: Client sends `Flags [S]` (SYN) with Initial Sequence Number 1000.
- Line 2: Server responds with `Flags [S.]` (SYN-ACK) with ISN 2000 and ACKs 1001.
- Line 3: Client sends `Flags [.]` (ACK) acknowledging 2001. Handshake is established.

### Wire Signature 2: Closed Port (`Connection Refused`)
```text
12:00:01.100 IP 10.0.1.10.54321 > 10.0.2.20.9000: Flags [S], seq 1000, length 0
12:00:01.101 IP 10.0.2.20.9000 > 10.0.1.10.54321: Flags [R.], seq 0, ack 1001, win 0, length 0
```
- Client sends SYN to port 9000.
- Destination kernel sends `Flags [R.]` (RST-ACK) with sequence 0, immediate reject.

### Wire Signature 3: Silent Drop / Firewall Black Hole (`Connection Timed Out`)
```text
12:00:01.000 IP 10.0.1.10.54321 > 10.0.2.20.80: Flags [S], seq 1000, length 0
12:00:02.010 IP 10.0.1.10.54321 > 10.0.2.20.80: Flags [S], seq 1000, length 0 (retransmit after 1s)
12:00:04.030 IP 10.0.1.10.54321 > 10.0.2.20.80: Flags [S], seq 1000, length 0 (retransmit after 2s)
12:00:08.070 IP 10.0.1.10.54321 > 10.0.2.20.80: Flags [S], seq 1000, length 0 (retransmit after 4s)
```
- Client sends SYN. No reply is received.
- Linux kernel TCP engine doubles RTO (exponential backoff) and retransmits SYN.
- After timeout limit (e.g. 130s), application raises `ETIMEDOUT`.

### Wire Signature 4: Path MTU Black Hole
```text
12:00:01.100 IP 10.0.1.10.54321 > 10.0.2.20.443: Flags [P.], seq 1:1461, ack 1, length 1460
12:00:01.105 IP 10.0.1.1 > 10.0.1.10: ICMP 10.0.2.20 unreachable - need to frag (mtu 1400), length 36
```
- Sender transmits 1460-byte payload with DF (Don't Fragment) bit set.
- Intermediate router (10.0.1.1) cannot forward without fragmenting, so it drops the packet and generates ICMP Type 3 Code 4.
- If a firewall drops this ICMP packet, the sender hangs indefinitely (Path MTU Black Hole).
