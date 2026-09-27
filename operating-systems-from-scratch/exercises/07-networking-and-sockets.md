# Track 7: Sockets & Network Systems Programming Exercises

> **Motto:** A socket is not a wire; it is a pair of kernel queues (send buffer and receive buffer) tied to a network protocol stack.

All solutions are located in `solutions/exercises/07-networking-and-sockets-solutions.md`.

---

### Exercise 7.1: Anatomy of a TCP Echo Server
Write a TCP echo server in C:
1. Create socket (`socket(AF_INET, SOCK_STREAM, 0)`)
2. Bind to `127.0.0.1:8080` (`bind`)
3. Mark passive listening (`listen`)
4. Accept incoming connection (`accept`)
5. Echo back received bytes and close.

### Exercise 7.2: Connecting Sockets with `connect`
Write a client program that connects to `127.0.0.1:8080`, sends `"Ping"`, receives `"Ping"`, and prints roundtrip elapsed time.

### Exercise 7.3: Understanding Network Byte Order (`htons`, `ntohl`)
Why do x86 and ARM processors store integers in Little-Endian byte order, while network protocols require Big-Endian (Network Byte Order)? Write a program using `htons()` and `ntohs()` to inspect the byte representation of port `8080` in memory.

### Exercise 7.4: Listening Socket vs Connected Socket
Demonstrate that the descriptor returned by `socket()` / `listen()` is NOT the descriptor used to transmit data! Print the file descriptor number returned by `socket()` (e.g. 3) and compare it with the file descriptor returned by `accept()` (e.g. 4).

### Exercise 7.5: The `SO_REUSEADDR` Socket Option
Restart a TCP server immediately after termination without `SO_REUSEADDR`. Observe `bind: Address already in use` due to the TCP `TIME_WAIT` state. Configure `SO_REUSEADDR` and verify that immediate port re-binding succeeds.

### Exercise 7.6: UNIX Domain Sockets (`AF_UNIX`)
Write a local client-server IPC using UNIX Domain Sockets (`AF_UNIX`) bound to a filesystem path `/tmp/os_lab.sock`. Benchmark the throughput compared to TCP `localhost` (`127.0.0.1`). Explain why UNIX sockets are faster (zero TCP checksumming or IP packet headers).

### Exercise 7.7: Inspecting Sockets with `ss` and `lsof`
Run a background server on port 9090. Use `ss -tulpn` and `lsof -i :9090` to inspect:
* Local Address and Port
* Foreign Address
* Socket state (`LISTEN`, `ESTABLISHED`, `TIME_WAIT`)
* Owning Process PID and command name.

### Exercise 7.8: Detecting Remote Connection Disconnect
In a TCP server, how does userspace know when a client cleanly closes its connection? Show that `read()` or `recv()` returns `0` (EOF). What does `read()` returning `-1` with `ECONNRESET` mean?

### Exercise 7.9: The TCP 3-Way Handshake in Syscalls
Map the TCP handshake (SYN, SYN-ACK, ACK) to socket API calls:
* When is SYN sent? (Client calls `connect`)
* When is SYN-ACK returned? (Kernel responds before `accept` is even called!)
* When is connection placed in the accept queue? (After 3rd ACK received by kernel).

### Exercise 7.10: UDP Sockets (`SOCK_DGRAM`)
Write a UDP client and server using `sendto()` and `recvfrom()`. Demonstrate that UDP is connectionless: the server requires no `listen()` or `accept()`, and packet boundaries are strictly preserved.

### Exercise 7.11: Tuning TCP Socket Buffers
Use `getsockopt()` and `setsockopt()` to inspect and modify `SO_RCVBUF` and `SO_SNDBUF`. How does the TCP receive window size affect throughput on high-latency networks?

### Exercise 7.12: Disabling Nagle's Algorithm (`TCP_NODELAY`)
Explain Nagle's algorithm and why small packets are buffered in the kernel. Enable `TCP_NODELAY` via `setsockopt()` and measure the latency reduction for real-time interactive games or database queries.

### Exercise 7.13: Socket Timeouts (`SO_RCVTIMEO`)
Configure a 3-second receive timeout on a connected socket using `SO_RCVTIMEO`. Verify that `read()` unblocks after 3 seconds and sets `errno = EAGAIN` or `EWOULDBLOCK` instead of hanging forever.

### Exercise 7.14: Passing File Descriptors over UNIX Sockets (`SCM_RIGHTS`)
Write two completely independent processes that communicate via a UNIX domain socket. Use `sendmsg()` with an ancillary control message (`SCM_RIGHTS`) to pass an open file descriptor from Process A to Process B!

### Exercise 7.15: TCP Half-Close via `shutdown`
Differentiate `close(fd)` from `shutdown(fd, SHUT_WR)`. Write a client that sends all its data, calls `shutdown(fd, SHUT_WR)` to transmit a FIN packet signaling end of upload, but continues to read response bytes until the server finishes.
