# The Universal 14-Step Network Troubleshooting Framework

> When an incident occurs and "The service is unreachable," **never guess and never change configurations at random**. Follow this deterministic, layer-by-layer isolation sequence.

---

## The 14-Step Diagnostic Ladder

```text
               APPLICATION LAYER (L7)
  [14] ◄── Did the application process return an error status (5xx)?
  [13] ◄── Did the reverse proxy / load balancer reach backend?
  [12] ◄── Did the TLS handshake and certificate validation succeed?
  [11] ◄── Does the application service listen on the expected port?
               TRANSPORT LAYER (L4)
  [10] ◄── Did the client receive a TCP RST (Connection Refused)?
  [09] ◄── Did the TCP 3-way handshake complete (SYN -> SYN-ACK -> ACK)?
  [08] ◄── Did firewall drop the packet (Connection Timed Out)?
               NETWORK LAYER (L3)
  [07] ◄── Does the router forward packets (ip_forward enabled)?
  [06] ◄── Did path MTU drop oversized packets without ICMP error?
  [05] ◄── Which routing table entry handles the destination IP?
  [04] ◄── Is the destination on the local subnet or across a gateway?
               LINK LAYER (L2) & RESOLUTION
  [03] ◄── Did ARP / Neighbor Discovery resolve the next-hop MAC?
  [02] ◄── Is the network interface UP with an assigned IP?
               NAME RESOLUTION
  [01] ◄── What IP did DNS resolve for the hostname?
```

---

## Step-by-Step Diagnostic Execution

### Step 1: DNS Name Resolution
- **Question**: What IP address was returned for the target hostname, and did resolution succeed?
- **Tool**:
  ```bash
  dig +short api.example.com
  getent hosts api.example.com
  ```
- **Failure Indicators**: `NXDOMAIN` (name does not exist), `SERVFAIL` (authoritative nameserver unreachable), empty response.
- **Root Causes**: Misconfigured `/etc/resolv.conf`, expired domain registration, local resolver crash.

### Step 2: Local Interface Status
- **Question**: Is the physical or virtual interface in the `UP` state with a valid IP assigned?
- **Tool**:
  ```bash
  ip link show dev eth0
  ip addr show dev eth0
  ```
- **Failure Indicators**: Interface state `DOWN` or `NO-CARRIER`; missing IP address.
- **Root Causes**: Cable unplugged, DHCP lease expired, driver failure, misnamed interface.

### Step 3: Local Subnet vs. Gateway Boundary
- **Question**: Does the destination IP belong to the local subnet, or must it be sent to a default gateway?
- **Logic**: Compare destination IP and local interface IP under the configured subnet mask (e.g. `10.0.1.50` vs `10.0.1.10/24`). If they share the prefix, delivery is direct. If not, delivery is routed.

### Step 4: Routing Table Selection
- **Question**: Which route in the kernel routing table handles this destination, and what is the next hop?
- **Tool**:
  ```bash
  ip route get <dest_ip>
  ```
- **Failure Indicators**: `RTNETLINK answers: Network is unreachable`.
- **Root Causes**: Missing default route (`default via ...`), bad static route, interface metric priority issue.

### Step 5: Neighbor Resolution (ARP / IPv6 NDP)
- **Question**: Can the kernel resolve the link-layer MAC address of the destination (if local) or the gateway (if remote)?
- **Tool**:
  ```bash
  ip neigh show <target_ip>
  ```
- **Failure Indicators**: State is `FAILED` or entry missing.
- **Root Causes**: Target machine powered off, wrong VLAN, firewall blocking ARP, IP conflict.

### Step 6: Transit Router Forwarding
- **Question**: If a router sits between sender and receiver, is packet forwarding enabled in its kernel?
- **Tool (on intermediate router)**:
  ```bash
  sysctl net.ipv4.ip_forward
  ```
- **Failure Indicators**: Packet arrives on Router interface 1 but never egresses interface 2.
- **Root Causes**: `net.ipv4.ip_forward = 0`, missing reverse route back to sender (asymmetric routing blackhole).

### Step 7: Path MTU & Fragmentation
- **Question**: Is an oversized packet being silently dropped along the path because of an MTU restriction?
- **Tool**:
  ```bash
  ping -M do -s 1472 <dest_ip>
  ```
- **Failure Indicators**: Ping succeeds with default small size (64 bytes) but hangs or drops when packet size is 1500 bytes.
- **Root Causes**: PMTUD black hole (intermediate firewall dropping ICMP Type 3 Code 4 "Fragmentation Needed").

### Step 8: Network Firewall (Stateful Packet Filter)
- **Question**: Is an intermediate firewall or local iptables/nftables chain dropping packets silently?
- **Tool**:
  ```bash
  sudo iptables -L -n -v
  sudo nft list ruleset
  ```
- **Failure Indicators**: `Connection timed out` after SYN retransmissions; iptables drop counters incrementing.

### Step 9: Listening Sockets & Bind Addresses
- **Question**: Is the server process actively listening on the target port, and is it bound to `0.0.0.0` or `127.0.0.1`?
- **Tool (on server)**:
  ```bash
  ss -tulpn | grep :<port>
  ```
- **Failure Indicators**: Output is empty (service not running), or bound strictly to `127.0.0.1:<port>` when external access is needed.

### Step 10: TCP 3-Way Handshake & Resets
- **Question**: Does the client receive a `SYN-ACK` or an immediate `RST`?
- **Tool**:
  ```bash
  sudo tcpdump -i any -nn port <port>
  ```
- **Failure Indicators**:
  - Immediate `RST`: Port closed, nothing listening (`Connection refused`).
  - Consecutive `SYN` retransmits with no reply: Silent packet drop along the path.

### Step 11: TLS Handshake & Certificate Validation
- **Question**: Does the cryptographic TLS handshake complete without cipher mismatch or trust errors?
- **Tool**:
  ```bash
  openssl s_client -connect <host>:<port> -servername <host>
  ```
- **Failure Indicators**: `certificate has expired`, `self signed certificate in certificate chain`, `handshake failure`.

### Step 12: Reverse Proxy & Load Balancer Upstream
- **Question**: Is the reverse proxy able to reach its backend application servers?
- **Failure Indicators**: HTTP `502 Bad Gateway` (proxy connected but backend refused/crashed), `504 Gateway Timeout` (backend failed to respond in time).

### Step 13: Application Request & Response
- **Question**: Does the application process parse the HTTP request headers and execute the business logic?
- **Tool**:
  ```bash
  curl -v -H "Host: example.com" http://<ip>:<port>/health
  ```
- **Failure Indicators**: HTTP `400 Bad Request`, `404 Not Found`, `500 Internal Server Error`.

### Step 14: Socket Resource Exhaustion
- **Question**: Has the host run out of ephemeral source ports or file descriptors?
- **Tool**:
  ```bash
  ss -s
  ulimit -n
  cat /proc/sys/fs/file-nr
  ```
- **Failure Indicators**: `Cannot assign requested address` (ephemeral port exhaustion), `Too many open files`.
