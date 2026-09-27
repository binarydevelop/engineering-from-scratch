# Core Architectural Mental Models

> "If you cannot explain the mechanics of a system in terms of memory, queues, tables, and wire state transitions, you do not possess an engineering model of it."

---

## 1. The Kernel Socket Abstraction

A network socket is not a physical wire; it is an **operating system abstraction (a file descriptor)** backed by kernel memory structures:

```text
USER SPACE PROCESS (e.g. Python / curl)
  │
  ├─ fd = socket(AF_INET, SOCK_STREAM, 0)   ──> Returns integer file descriptor (e.g., 3)
  ├─ write(fd, "GET / HTTP/1.1\r\n\r\n")    ──> Syscall transitions to kernel mode
  │
  ▼
KERNEL NETWORK STACK
  ┌────────────────────────────────────────────────────────┐
  │ FILE DESCRIPTOR TABLE: fd 3 ──► struct socket          │
  ├────────────────────────────────────────────────────────┤
  │ STRUCT SOCK: Points to protocol ops (tcp_prot)         │
  ├────────────────────────────────────────────────────────┤
  │ SEND BUFFER (sk_write_queue):                          │
  │ [ sk_buff: "GET /" ] ──► [ sk_buff: "HTTP/1.1\r\n" ]   │
  ├────────────────────────────────────────────────────────┤
  │ RECEIVE BUFFER (sk_receive_queue):                     │
  │ [ sk_buff: "HTTP/1.1 200 OK" ] ──► unread wire data    │
  ├────────────────────────────────────────────────────────┤
  │ TRANSMISSION CONTROL BLOCK (TCB):                      │
  │ 4-Tuple: (192.168.1.10:48291 <-> 93.184.216.34:80)     │
  │ State: ESTABLISHED | snd_una, snd_nxt, rcv_nxt, cwnd   │
  └────────────────────────────────────────────────────────┘
```

When an application calls `write()` on a socket, the data does not immediately fly across the network. It is copied from user space memory into the kernel's **Send Buffer**. The kernel's TCP engine decides when and how many bytes to package into an outgoing `sk_buff` packet based on `cwnd`, receiver window (`rcv_wnd`), and the Nagle algorithm.

---

## 2. Listening Socket vs. Connected Socket

One of the most frequent confusions in network programming is conflating the **server listener** with the **active connection**:

```text
SERVER PROCESS:
  1. listen_fd = socket()
  2. bind(listen_fd, 0.0.0.0:80)
  3. listen(listen_fd, backlog=128)

                       KERNEL SOCKET TABLE
  ┌──────────────────────────────────────────────────────────────────┐
  │ LISTENING SOCKET (Passive Endpoint):                             │
  │ Local: 0.0.0.0:80 | Remote: *:* | State: LISTEN                  │
  │ Queues:                                                          │
  │   - SYN Queue (half-open incoming handshakes)                    │
  │   - Accept Queue (completed handshakes waiting for accept())     │
  └──────────────────────────────┬───────────────────────────────────┘
                                 │
           Client connects ──────┘ (3-Way Handshake completes)
                                 │
  4. conn_fd = accept(listen_fd) ▼
  ┌──────────────────────────────────────────────────────────────────┐
  │ CONNECTED SOCKET (Active Endpoint):                              │
  │ Local: 192.168.1.10:80 | Remote: 203.0.113.5:54321               │
  │ State: ESTABLISHED | Dedicated send/recv buffers                 │
  └──────────────────────────────────────────────────────────────────┘
```

- The **Listening Socket** never sends application data and never receives application payload. Its sole purpose is to receive initial `SYN` packets and complete handshakes.
- Calling `accept()` extracts a completed connection from the Accept Queue and creates a **brand new file descriptor (Connected Socket)** bound to the specific 4-tuple.
- The listening socket remains open on port 80 to accept further clients.

---

## 3. The TCP State Machine (Connection Lifecycle)

```text
                      ┌───────────────┐
                      │    CLOSED     │
                      └───────┬───────┘
                              │ Active Open: send SYN
                              ▼
                      ┌───────────────┐
                      │   SYN_SENT    │
                      └───────┬───────┘
                              │ Receive SYN-ACK; send ACK
                              ▼
                      ┌───────────────┐
                      │  ESTABLISHED  │ ◄─── Full-Duplex Data Transfer
                      └───────┬───────┘
                              │ Close initiated: send FIN
                              ▼
                      ┌───────────────┐
                      │  FIN_WAIT_1   │
                      └───────┬───────┘
                              │ Receive ACK of FIN
                              ▼
                      ┌───────────────┐
                      │  FIN_WAIT_2   │
                      └───────┬───────┘
                              │ Receive FIN from peer; send ACK
                              ▼
                      ┌───────────────┐
                      │   TIME_WAIT   │ ◄─── Waits 2 * MSL (typically 60s)
                      └───────┬───────┘
                              │ Timer expires
                              ▼
                      ┌───────────────┐
                      │    CLOSED     │
                      └───────────────┘
```

### Why TIME_WAIT is Mandatory
1. **Ensure Final ACK Delivery**: If the client's final `ACK` is dropped by the network, the server retransmits its `FIN`. If the client were already `CLOSED`, it would respond with `RST`, making the server report an ungraceful connection abort.
2. **Prevent Stale Packet Collisions**: Old duplicate packets wandering through the Internet must expire before a new connection reusing the same 4-tuple can be accepted.

---

## 4. Switching (Layer 2) vs. Routing (Layer 3)

```text
               SWITCHING (Layer 2)                     ROUTING (Layer 3)
   ┌────────────────────────────────────────┐ ┌────────────────────────────────────────┐
   │ - Operates within single broadcast     │ │ - Connects distinct subnets / broadcast│
   │   domain / local subnet.               │ │   domains.                             │
   │ - Forwarding decision based on MAC.    │ │ - Forwarding decision based on IP.     │
   │ - Consults CAM Table:                  │ │ - Consults Routing Table:              │
   │   MAC Address ──► Switch Port          │ │   Destination Prefix ──► Gateway / NIC │
   │ - Unknown unicast: Flooded to all ports│ │ - Unknown route: Dropped or sent to    │
   │ - Does NOT modify frame headers.       │ │   default gateway (0.0.0.0/0).         │
   │                                        │ │ - REWRITES L2 Ethernet MAC headers     │
   │                                        │ │   and decrements L3 TTL at each hop.   │
   └────────────────────────────────────────┘ └────────────────────────────────────────┘
```

### The Packet Transformation Across a Router

```text
Host A (10.0.1.10) ──► Router (10.0.1.1 / 10.0.2.1) ──► Host B (10.0.2.20)

Segment 1: Host A to Router
┌───────────────────────────────┬───────────────────────────────┬─────────────┐
│ Src MAC: A_MAC                │ Src IP: 10.0.1.10             │ TCP Payload │
│ Dst MAC: ROUTER_IN_MAC        │ Dst IP: 10.0.2.20             │             │
└───────────────────────────────┴───────────────────────────────┴─────────────┘

Router decapsulates L2, decrements TTL by 1, resolves Host B MAC via ARP, and re-encapsulates:

Segment 2: Router to Host B
┌───────────────────────────────┬───────────────────────────────┬─────────────┐
│ Src MAC: ROUTER_OUT_MAC       │ Src IP: 10.0.1.10 (UNCHANGED) │ TCP Payload │
│ Dst MAC: B_MAC                │ Dst IP: 10.0.2.20 (UNCHANGED) │             │
└───────────────────────────────┴───────────────────────────────┴─────────────┘
```
Notice: **IP addresses remain constant end-to-end; MAC addresses change at every router hop!**

---

## 5. Flow Control vs. Congestion Control

| Dimension | Flow Control | Congestion Control |
| :--- | :--- | :--- |
| **Problem Addressed** | Fast sender overwhelming a slow **receiver process** | Fast sender(s) overwhelming intermediate **network routers/links** |
| **Limiting Variable** | Advertised Receive Window (`rcv_wnd`) | Congestion Window (`cwnd`) |
| **Governing Entity** | Receiver tells sender via TCP header field | Sender infers from ACKs, packet loss, or RTT inflation |
| **Transmission Limit** | Effective Window $= \min(\text{cwnd}, \text{rcv_wnd})$ | |

---

## 6. Reverse Proxy vs. Forward Proxy vs. Load Balancer

```text
FORWARD PROXY (Client Agent):
[ Internal Clients ] ──► [ Forward Proxy ] ──► (Internet) ──► [ External Servers ]
* Masks client identity, enforces corporate egress policies, caches web assets.

REVERSE PROXY (Server Gateway):
[ Internet Clients ] ──► [ Reverse Proxy ] ──► [ Internal App Servers ]
* Masks backend architecture, terminates TLS, handles caching, routes paths (`/api`).

LOAD BALANCER:
[ Incoming Traffic ] ──► [ Load Balancer ] ──┬──► [ Backend Instance 1 ]
                                            ├──► [ Backend Instance 2 ]
                                            └──► [ Backend Instance 3 ]
* Distributes traffic across instances using algorithms (Round Robin, Least Conn).
```
