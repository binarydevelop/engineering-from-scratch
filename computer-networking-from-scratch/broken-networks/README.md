# 32 Broken-Network Troubleshooting Labs

> **Philosophy**: Real network engineering expertise is forged in broken systems. When a network fails, symptoms manifest first (timeouts, resets, errors), while the root cause remains hidden.

This directory contains **32 hands-on failure scenarios** spanning every layer of the network stack.  
**Rule**: Read the symptoms first, formulate a hypothesis, use diagnostic tools to collect proof, and only then consult `solution.md`.

---

## Master Symptom Index

| Lab | Scenario | Failing Layer | User-Observed Symptom | Primary Diagnostic Tool |
| :--- | :--- | :--- | :--- | :--- |
| **01** | [DNS NXDOMAIN](lab-01-dns-nxdomain/) | L7 (DNS) | `curl: (6) Could not resolve host: api.prod.internal` | `dig` |
| **02** | [Unreachable Nameserver](lab-02-dns-wrong-nameserver/) | L7 / L3 | `connection timed out; no servers could be reached` | `cat /etc/resolv.conf` |
| **03** | [Default Gateway Missing](lab-03-default-gateway-missing/) | L3 (Routing) | `RTNETLINK answers: Network is unreachable` | `ip route show` |
| **04** | [Mismatched Subnet Mask](lab-04-wrong-subnet-mask/) | L3 / L2 | Asymmetric ARP failure; A pings B, but B cannot ping A | `ip addr show` |
| **05** | [Stale ARP Cache Entry](lab-05-arp-cache-poisoning-or-stale/) | L2 (Neighbor Table) | Host unreachable despite valid route and link UP | `ip neigh show` |
| **06** | [IP Forwarding Disabled](lab-06-ip-forwarding-disabled/) | L3 (Router) | Packets arrive at router ingress but never egress | `sysctl net.ipv4.ip_forward` |
| **07** | [Asymmetric Routing Drop](lab-07-asymmetric-routing-drop/) | L3 / L4 (Firewall) | Client sends SYN, server replies via different path, firewall drops | `tcpdump` |
| **08** | [Firewall Drops Inbound SYN](lab-08-firewall-drops-inbound-syn/) | L4 / L3 (Filter) | `Connection timed out` after SYN retransmissions | `iptables -L -n -v` |
| **09** | [Firewall Drops SYN-ACK](lab-09-firewall-drops-syn-ack/) | L4 (Filter) | Client times out; server socket left in `SYN_RECV` | `tcpdump` on both sides |
| **10** | [Service Bound to Localhost](lab-10-service-listening-localhost-only/) | L4 (Socket Bind) | Container or remote host gets `Connection refused` | `ss -tulpn` |
| **11** | [Port Mismatch](lab-11-port-mismatch/) | L4 (Transport) | Client connects to 8000, server listens 8080 (`Connection refused`) | `ss -tlpn` |
| **12** | [Process Crashed / Down](lab-12-process-crashed-connection-refused/) | L7 / L4 | Server daemon dead; immediate TCP RST received | `ps aux` / `systemctl` |
| **13** | [Ephemeral Port Exhaustion](lab-13-ephemeral-port-exhaustion/) | L4 (Socket Table) | `Cannot assign requested address (EADDRNOTAVAIL)` | `ss -s` |
| **14** | [TIME_WAIT Socket Buildup](lab-14-time-wait-buildup/) | L4 (TCP State) | Thousands of sockets stuck in `TIME_WAIT` | `ss -tan state time-wait` |
| **15** | [Path MTU Black Hole](lab-15-mtu-blackhole/) | L3 (MTU / ICMP) | Small ping packets succeed, but large HTTP/TLS payloads hang | `ping -M do -s 1472` |
| **16** | [Reverse Proxy 502 Bad Gateway](lab-16-reverse-proxy-502-bad-gateway/) | L7 (Reverse Proxy) | `HTTP/1.1 502 Bad Gateway` returned to browser | Proxy error logs |
| **17** | [Reverse Proxy 504 Gateway Timeout](lab-17-reverse-proxy-504-gateway-timeout/) | L7 (Reverse Proxy) | `HTTP/1.1 504 Gateway Timeout` after 60s | Upstream APM traces |
| **18** | [Unhealthy Load Balancer Backend](lab-18-load-balancer-unhealthy-backend/) | L7 (Load Balancing) | 50% of requests intermittently fail with 502 | LB access log / metrics |
| **19** | [SNAT Port Exhaustion](lab-19-snat-exhaustion/) | L3 / L4 (Conntrack) | Outbound connections fail during traffic spikes | `conntrack -C` |
| **20** | [DNAT Port Forwarding Mismatch](lab-20-dnat-wrong-internal-port/) | L3 / L4 (NAT) | Traffic hits host port 8080 but never reaches internal app | `iptables -t nat -L` |
| **21** | [TLS Hostname Mismatch](lab-21-tls-certificate-hostname-mismatch/) | L5/6 (TLS) | `SSL: CERTIFICATE_VERIFY_FAILED: certificate is not valid for domain` | `openssl s_client` |
| **22** | [TLS Expired Certificate](lab-22-tls-expired-certificate/) | L5/6 (TLS) | `certificate has expired` | `openssl x509 -enddate` |
| **23** | [Untrusted Certificate Authority](lab-23-tls-untrusted-ca/) | L5/6 (PKI) | `self signed certificate in certificate chain` | `curl -v` |
| **24** | [Duplicate IP Address](lab-24-duplicate-ip-address/) | L3 / L2 (ARP Conflict) | Severe packet loss, MAC flapping on switch | `arping` / `ip neigh` |
| **25** | [Half-Open Idle Connection Drop](lab-25-half-open-connection-drop/) | L4 (Conntrack) | Connection hangs after 5 minutes of idle silence | `ss -t -i` |
| **26** | [Packet Loss Throughput Collapse](lab-26-tc-packet-loss-cascade/) | L4 (TCP Congestion) | 100 Mbps link collapses to 2 Mbps under 10% packet loss | `iperf3` / `tc` |
| **27** | [Bufferbloat Latency Inflation](lab-27-bufferbloat-tail-drop/) | L3 / L4 (Queueing) | Ping RTT spikes from 5ms to 2500ms during large upload | `ping` under load |
| **28** | [Stale Client DNS Caching](lab-28-dns-caching-stale-ip/) | L7 (DNS) | Client sends traffic to old IP hours after DNS migration | `dig` vs client log |
| **29** | [Connection Pool Leak](lab-29-connection-pool-leak/) | L4 / L7 (Sockets) | Process hits `Too many open files` limit | `lsof -p <pid> \| wc -l` |
| **30** | [Split-Brain Network Partition](lab-30-split-brain-partition/) | L3 (Partition) | Database nodes in two racks both elect themselves primary | `ping` / network routes |
| **31** | [Keepalive Timeout Race](lab-31-keepalive-timeout-race/) | L7 / L4 (Keep-Alive) | Intermittent `ECONNRESET` / 502 on idle reused connections | `tcpdump` |
| **32** | [HTTP Missing Host Header](lab-32-http-missing-host-header/) | L7 (HTTP/1.1) | `HTTP/1.1 400 Bad Request` on valid IP endpoint | `curl -v` / `nc` |

---

## How to Solve a Broken Lab

1. Navigate to the scenario directory (e.g., `cd broken-networks/lab-10-service-listening-localhost-only`).
2. Read `README.md` to review the observed symptom.
3. Formulate your hypothesis.
4. Run diagnostic commands to gather empirical proof.
5. Apply your fix and re-test.
6. Verify your reasoning against `solution.md`.
