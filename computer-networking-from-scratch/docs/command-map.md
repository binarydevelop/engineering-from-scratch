# Practical Command Map: Diagnostics Organized by Question

> **Rule of Thumb**: Never organize your knowledge around memorizing utility flags. Organize your knowledge around the **exact diagnostic questions you need answered**, then pick the precision tool that inspects that layer of state.

---

## Layer 1 & 2: Physical & Data Link Layer

### QUESTION: What physical and virtual network interfaces exist on this machine?
```bash
ip link show
# Or with statistics:
ip -s link show
```
*What to look for*: Interface state (`UP`, `DOWN`, `LOWER_UP`), MTU, interface flags (`BROADCAST`, `MULTICAST`), hardware MAC address (`link/ether`).

### QUESTION: What is the MAC address of an interface?
```bash
ip link show dev eth0
# Or inspect sysfs directly:
cat /sys/class/net/eth0/address
```

### QUESTION: What is the link speed and duplex mode of my physical NIC?
```bash
ethtool eth0 2>/dev/null || ip link show eth0
```

### QUESTION: What local Layer-2 neighbors (IP -> MAC mappings) does my host know about?
```bash
ip neigh show
```
*What to look for*: State of neighbor cache (`REACHABLE`, `STALE`, `DELAY`, `FAILED`). `FAILED` means ARP resolution timed out.

### QUESTION: How do I manually clear or flush a stale ARP/neighbor entry?
```bash
sudo ip neigh flush dev eth0
# Or delete a specific target:
sudo ip neigh del 192.168.1.50 dev eth0
```

---

## Layer 3: Network Layer (IPv4 / IPv6 Addressing & Routing)

### QUESTION: What IP addresses are assigned to this machine?
```bash
ip -br addr show
# Or detailed:
ip addr show
```
*What to look for*: Prefix length (`/24`, `/16`), scope (`global`, `host`, `link`), IPv4 and IPv6 addresses.

### QUESTION: Where will the kernel send a packet destined for a specific IP address?
```bash
ip route get 1.1.1.1
ip route get 10.0.1.50
```
*What to look for*: Selected route, outgoing interface (`dev`), source IP chosen (`src`), and next-hop gateway (`via`).

### QUESTION: What does my complete routing table look like?
```bash
ip route show
# For IPv6:
ip -6 route show
```
*What to look for*: The default route (`default via <gateway>`), directly attached subnets (`proto kernel scope link`), and route metrics.

### QUESTION: Is IP packet forwarding enabled in the kernel?
```bash
sysctl net.ipv4.ip_forward
# Value 0 = Host only (drops transit packets)
# Value 1 = Router mode (forwards packets between interfaces)
```

### QUESTION: Can I reach the target host at Layer 3 (ICMP Echo)?
```bash
ping -c 4 1.1.1.1
# With explicit interface and packet size:
ping -c 4 -I eth0 -s 1472 192.168.1.1
```
*What to look for*: Packet loss percentage, round-trip time (min/avg/max/mdev).

### QUESTION: Which router hops does my packet traverse to reach a remote destination?
```bash
traceroute -n 1.1.1.1
# Or using ICMP instead of UDP:
traceroute -n -I 1.1.1.1
```
*What to look for*: Each hop's IP and RTT. Asterisks (`* * *`) indicate hops dropping ICMP Time-Exceeded or firewalled gateways.

### QUESTION: What is the maximum path MTU without fragmentation?
```bash
ping -M do -s 1472 -c 2 1.1.1.1
```
*What to look for*: If output says `Frag needed and DF set (mtu = 1492)`, the path MTU is smaller than 1500 bytes.

---

## Layer 4: Transport Layer (TCP, UDP & Sockets)

### QUESTION: Who is listening on this machine, and on which ports and protocols?
```bash
# Sockets: TCP and UDP listening sockets with process IDs
ss -tulpn
```
*Flags explained*:
- `-t`: TCP sockets
- `-u`: UDP sockets
- `-l`: Listening sockets only
- `-p`: Show process using socket (requires root for non-owned processes)
- `-n`: Numeric IP and port numbers (do not resolve service names)

### QUESTION: Is a specific port listening on all interfaces or localhost only?
```bash
ss -tlpn | grep ':8080'
```
*Crucial distinction*:
- `127.0.0.1:8080` -> Bound strictly to loopback! Remote hosts and containers cannot reach it.
- `0.0.0.0:8080` -> Bound to all IPv4 interfaces. Accessible from external networks.
- `[::]:8080` -> Bound to all IPv6 and IPv4 interfaces (if `ipv6only=0`).

### QUESTION: Which active TCP connections are established or in TIME_WAIT?
```bash
ss -tan state established
ss -tan state time-wait
# Or summary of socket counts:
ss -s
```

### QUESTION: Which process owns a specific network socket or open port?
```bash
sudo ss -lpn 'sport = :5432'
# Or using lsof:
sudo lsof -i :5432
```

### QUESTION: What are the send and receive buffer sizes of an active TCP socket?
```bash
ss -t -i 'sport = :443'
```
*What to look for*: `cwnd` (congestion window), `ssthresh`, `rtt`, `rto`, `bytes_sent`, `retrans`.

---

## Layer 7: Application Protocols (DNS & HTTP)

### QUESTION: Does a hostname resolve, which nameserver answered, and what is the TTL?
```bash
dig example.com
# For reverse lookup (PTR):
dig -x 93.184.216.34
# For trace from root servers:
dig +trace example.com
```
*What to look for*: `status: NOERROR`, `ANSWER:`, TTL count, and `SERVER: <ip>#53`.

### QUESTION: Does the OS standard resolver resolve a name (checking /etc/hosts + DNS)?
```bash
getent hosts example.com
```

### QUESTION: What upstream DNS resolvers is my host configured to use?
```bash
cat /etc/resolv.conf
# On systemd-resolved systems:
resolvectl status 2>/dev/null
```

### QUESTION: Is an HTTP endpoint responding, and what are the exact response headers?
```bash
curl -I https://example.com/api
# Or full verbose trace showing DNS, TCP connect, and TLS handshake:
curl -v https://example.com/api
```

### QUESTION: How much time was spent on DNS, TCP connect, TLS handshake, and first byte?
```bash
curl -w "DNS: %{time_namelookup}s | TCP: %{time_connect}s | TLS: %{time_appconnect}s | TTFB: %{time_starttransfer}s | Total: %{time_total}s\n" -o /dev/null -s https://example.com
```

---

## Packet Inspection & Wire Sniffing

### QUESTION: What packets are actually moving across an interface right now?
```bash
# Capture packets on eth0 with numeric hosts and ports
sudo tcpdump -i eth0 -nn
```

### QUESTION: How do I capture traffic matching only a specific host or port?
```bash
sudo tcpdump -i eth0 -nn host 192.168.1.10 and port 80
```

### QUESTION: How do I capture only TCP handshake packets (SYN / SYN-ACK)?
```bash
sudo tcpdump -i eth0 -nn "tcp[tcpflags] & (tcp-syn) != 0"
```

### QUESTION: How do I capture packets to a file for analysis in Wireshark?
```bash
sudo tcpdump -i eth0 -s0 -w /tmp/capture.pcap
```

---

## Network Namespaces & Isolation

### QUESTION: What network namespaces exist on this Linux system?
```bash
ip netns list
```

### QUESTION: How do I execute a command inside a specific network namespace?
```bash
sudo ip netns exec ns-client ip addr show
sudo ip netns exec ns-client ss -tulpn
sudo ip netns exec ns-client curl -v http://10.99.2.10
```

---

## Firewalls & Packet Filtering

### QUESTION: What packet filter rules and NAT tables are active?
```bash
# nftables:
sudo nft list ruleset
# iptables filter table:
sudo iptables -L -n -v
# iptables NAT table:
sudo iptables -t nat -L -n -v
```

### QUESTION: What active connection tracking states exist in the kernel?
```bash
sudo conntrack -L 2>/dev/null || cat /proc/net/nf_conntrack 2>/dev/null
```
