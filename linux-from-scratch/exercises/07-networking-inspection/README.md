# Exercise Set 07: Network Inspection & Sockets

### Ex 7.1: Network Interface Status
Using `ip link`, check the status of all network interfaces on the system. Which interface represents the loopback device?

### Ex 7.2: IP and Subnet Mask Inspection
Using `ip addr`, determine the IP address and CIDR prefix length (e.g. `/24`) of your primary network interface.

### Ex 7.3: Default Gateway and Routing Table
Inspect the kernel routing table using `ip route`. Which line defines the default gateway used for internet traffic?

### Ex 7.4: Listening TCP Ports with ss
Run `ss -lntp`. Explain the meaning of `State`, `Recv-Q`, `Send-Q`, `Local Address:Port`, and `Process`.

### Ex 7.5: The Localhost Binding Trap
Start a Python HTTP server bound to `127.0.0.1:8080`. Start another bound to `0.0.0.0:9090`. Explain why another computer on the local network can connect to port `9090` but receives `Connection Refused` on port `8080`.

### Ex 7.6: Testing Port Reachability with Netcat
Use `nc -zv <host> <port>` to test if a remote TCP port is open and listening without sending full application-layer payloads.

### Ex 7.7: Verbose HTTP Inspection with Curl
Use `curl -Iv https://example.com`. Identify in the output: DNS resolution time, TCP handshake, TLS handshake, and HTTP response headers.

### Ex 7.8: Tracing DNS Resolution with Dig
Use `dig +trace example.com` to observe the recursive DNS resolution process from the 13 root nameservers down to the authoritative nameserver.

### Ex 7.9: The /etc/hosts Override
Add a temporary test entry to `/etc/hosts`: `127.0.0.1 test.internal`. Verify that `ping test.internal` and `curl test.internal` resolve to localhost.

### Ex 7.10: Capturing Packets with tcpdump
Use `tcpdump -i lo -nn port 8080` to capture raw packets while sending an HTTP request across localhost. Identify the TCP 3-way handshake flags (SYN, SYN-ACK, ACK).

### Ex 7.11: Identifying Socket Owning Processes
Given port `5432`, find the exact PID and process name listening on that port using two different utilities (`ss` and `lsof`).

### Ex 7.12: Testing UDP vs TCP Connectivity
Explain why `ping` (ICMP) can succeed even if an application running on TCP port 443 is down, and vice versa.
