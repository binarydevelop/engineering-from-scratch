# Master Engineering Curriculum: 180-Day Exhaustive Day-by-Day Schedule & Checklist

> **Mission**: Master the entire software, distributed systems, storage, cloud platform, and modern AI engineering stack through uncompromising, first-principles implementation.  
> **Commitment**: Intensive (~4–5 hours/day, 25–30 hours/week, 6 Months / 180 Days)  
> **Repository Index**: [`engineering-from-scratch`](https://github.com/binarydevelop/engineering-from-scratch) (Local: `/Users/tushar/desktop/private/repos`)  
> **Git Identity**: `Tushar <binarydevelop@gmail.com>`

---

## 📅 The 180-Day Master Milestone Map

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ 180-DAY INTENSIVE ARCHITECT PATHWAY                                                    │
├─────────┬───────────────────────────────┬──────────────────────────────┬───────────────┤
│ Period  │ Domain Focus                  │ Primary Repositories         │ Day Range     │
├─────────┼───────────────────────────────┼──────────────────────────────┼───────────────┤
│ Month 1 │ Machine Foundations & OS      │ operating-systems, linux     │ Days 001–030  │
│ Month 2 │ Protocols & Craftsmanship     │ networking, java, lld        │ Days 031–060  │
│ Month 3 │ Backend & Storage Internals   │ backend-engineering (1-205)  │ Days 061–090  │
│ Month 4 │ Persistence, Cache & Streams  │ sql, redis, kafka, elastic   │ Days 091–120  │
│ Month 5 │ OLAP, Data & Cloud Platforms  │ olap, data-eng, docker, k8s  │ Days 121–150  │
│ Month 6 │ Distributed Systems, SRE & AI │ system-design, sre, ai-sys   │ Days 151–180  │
└─────────┴───────────────────────────────┴──────────────────────────────┴───────────────┘
```

---

## 🛠️ The Daily 4-Hour Execution Ritual

Every single day is divided into four disciplined execution blocks:
1. **Block 1 (45 mins) — Concept Deconstruction:** Read the phase `docs/` and diagram memory layouts, protocol state machines, or data structures on paper.
2. **Block 2 (105 mins) — From-Scratch Implementation:** Open `code/` and write the core mechanisms without copy-pasting solutions.
3. **Block 3 (60 mins) — Failure Injection & Broken Lab:** Debug the associated broken system or reproduce edge cases under concurrency.
4. **Block 4 (30 mins) — Test Verification & Git Commit:** Run `pytest` / `make` / `mvn test`, ensure 100% green pass, commit, and push.

---

# MONTH 1: Machine Foundations, Kernel Physics & Systems Realities (Days 001 – 030)

### Week 1: Hardware Abstractions, Memory & Assembly
- [ ] **Day 001** | [`operating-systems`](file:///Users/tushar/desktop/private/repos/operating-systems-from-scratch) | Phase 00–03: Environment setup, bits, bytes, registers, and assembly mechanics.  
  *Task:* Write raw assembly routine demonstrating caller vs callee-saved registers.  
  *Verify:* `make -C operating-systems-from-scratch/phases/03-assembly test`
- [ ] **Day 002** | [`operating-systems`](file:///Users/tushar/desktop/private/repos/operating-systems-from-scratch) | Phase 04–08: Virtual memory, page tables, multi-level paging, and TLB hit/miss physics.  
  *Task:* Calculate address translation math for 4-level x86_64 paging tables.  
  *Verify:* Run page table walking simulation.
- [ ] **Day 003** | [`operating-systems`](file:///Users/tushar/desktop/private/repos/operating-systems-from-scratch) | Phase 09–13: Stack frames, buffer overflows, calling conventions, and heap mechanics.  
  *Task:* Inspect stack growth and frame pointer linkage with GDB.
- [ ] **Day 004** | [`operating-systems`](file:///Users/tushar/desktop/private/repos/operating-systems-from-scratch) | Phase 14–18: System calls, trap tables, user-space to kernel-space context switching.  
  *Task:* Trace `write()` syscall down to kernel trap vector.
- [ ] **Day 005** | [`operating-systems`](file:///Users/tushar/desktop/private/repos/operating-systems-from-scratch) | Project 06: Custom Memory Allocator (`malloc` & `free`).  
  *Task:* Implement free-list memory allocator with boundary tags and chunk coalescing.  
  *Verify:* `make -C operating-systems-from-scratch/projects/06-custom-allocator-malloc`
- [ ] **Day 006** | [`operating-systems`](file:///Users/tushar/desktop/private/repos/operating-systems-from-scratch) | Phase 19–25: Process scheduling algorithms: FIFO, Round-Robin, Priority, and CFS.  
  *Task:* Simulate Completely Fair Scheduler (CFS) red-black tree with virtual runtime.
- [ ] **Day 007** | [`operating-systems`](file:///Users/tushar/desktop/private/repos/operating-systems-from-scratch) | Phase 26–32: Inter-Process Communication (IPC): Pipes, FIFOs, UNIX domain sockets.  
  *Task:* Benchmark throughput of UNIX domain sockets vs TCP loopback sockets.

### Week 2: Concurrency Primitives, Signals & File Systems
- [ ] **Day 008** | [`operating-systems`](file:///Users/tushar/desktop/private/repos/operating-systems-from-scratch) | Phase 33–40: Threading, race conditions, mutexes, semaphores, and spinlocks.  
  *Task:* Implement a user-space spinlock using atomic Compare-And-Swap (CAS).
- [ ] **Day 009** | [`operating-systems`](file:///Users/tushar/desktop/private/repos/operating-systems-from-scratch) | Phase 41–48: Condition variables, deadlocks, Coffman conditions, and dining philosophers.  
  *Task:* Write deadlock-free resource ordering protocol.
- [ ] **Day 010** | [`operating-systems`](file:///Users/tushar/desktop/private/repos/operating-systems-from-scratch) | Project 01: Build a Unix Shell (`tiny-shell`).  
  *Task:* Implement command execution, fork/execve, job control, signals, and pipes (`|`).  
  *Verify:* Run test suite in `operating-systems-from-scratch/projects/01-tiny-shell`.
- [ ] **Day 011** | [`operating-systems`](file:///Users/tushar/desktop/private/repos/operating-systems-from-scratch) | Phase 49–58: File system inodes, directory entries, block groups, and superblock.  
  *Task:* Traverse raw inode metadata structure in pure C.
- [ ] **Day 012** | [`operating-systems`](file:///Users/tushar/desktop/private/repos/operating-systems-from-scratch) | Project 04: Ext2 File System Reader.  
  *Task:* Parse ext2 superblock and read root directory `/` directly from disk image.  
  *Verify:* `make -C operating-systems-from-scratch/projects/04-ext2-reader`.
- [ ] **Day 013** | [`operating-systems`](file:///Users/tushar/desktop/private/repos/operating-systems-from-scratch) | Phase 59–70: Page cache, buffer cache, dirty pages, and `fsync` flush semantics.  
  *Task:* Demonstrate dirty page accumulation and writeback latency.
- [ ] **Day 014** | [`operating-systems`](file:///Users/tushar/desktop/private/repos/operating-systems-from-scratch) | Capstone Synthesis: Review all OS projects (Shell, Allocator, Ext2 Reader).  
  *Task:* Run all benchmark suites in `operating-systems-from-scratch/benchmarks/`.

### Week 3: Linux Kernel Realities & Process Subsystems
- [ ] **Day 015** | [`linux-from-scratch`](file:///Users/tushar/desktop/private/repos/linux-from-scratch) | Phases 00–15: Linux architecture, `/proc` file system, process state flags.  
  *Task:* Parse `/proc/[pid]/stat`, `status`, and `maps` programmatically.  
  *Verify:* Solve Broken Labs 01–03 in `linux-from-scratch/broken-systems/`.
- [ ] **Day 016** | [`linux-from-scratch`](file:///Users/tushar/desktop/private/repos/linux-from-scratch) | Phases 16–30: Linux Signals, SIGTERM graceful shutdown, SIGKILL, signal masking.  
  *Task:* Build daemon handling SIGTERM with in-flight worker draining.  
  *Verify:* Solve Broken Labs 04–06.
- [ ] **Day 017** | [`linux-from-scratch`](file:///Users/tushar/desktop/private/repos/linux-from-scratch) | Phases 31–45: File descriptors, limits (`ulimit`), file table entries, inode locking.  
  *Task:* Reproduce and resolve "Too many open files" socket descriptor exhaustion.  
  *Verify:* Solve Broken Labs 07–09.
- [ ] **Day 018** | [`linux-from-scratch`](file:///Users/tushar/desktop/private/repos/linux-from-scratch) | Phases 46–60: Linux Namespaces: PID, Mount, Network, IPC, UTS, and User.  
  *Task:* Create an isolated process container using raw `unshare` syscalls.  
  *Verify:* Solve Broken Labs 10–12.
- [ ] **Day 019** | [`linux-from-scratch`](file:///Users/tushar/desktop/private/repos/linux-from-scratch) | Phases 61–75: Control Groups (cgroups v2): Memory limits, OOM killer, CPU shares.  
  *Task:* Apply 100MB memory limit to a runaway process and inspect `cgroup.events` OOM kill.  
  *Verify:* Solve Broken Labs 13–15.
- [ ] **Day 020** | [`linux-from-scratch`](file:///Users/tushar/desktop/private/repos/linux-from-scratch) | Project 02: Build a Container Runtime from Scratch in Bash/C.  
  *Task:* Combine chroot, pivot_root, namespaces, and cgroups into container CLI.  
  *Verify:* Run `linux-from-scratch/projects/02-container-runtime/test.sh`.
- [ ] **Day 021** | [`linux-from-scratch`](file:///Users/tushar/desktop/private/repos/linux-from-scratch) | Phases 76–90: System I/O models: Blocking, Non-blocking, I/O multiplexing (`select`, `poll`).  
  *Task:* Trace `strace -c` overhead difference between polling and blocking calls.

### Week 4: Epoll, eBPF & Kernel Performance Tracing
- [ ] **Day 022** | [`linux-from-scratch`](file:///Users/tushar/desktop/private/repos/linux-from-scratch) | Phases 91–105: Edge-triggered vs Level-triggered `epoll` architecture.  
  *Task:* Implement an epoll event notification loop handling 10,000 idle connections.  
  *Verify:* Solve Broken Labs 16–18.
- [ ] **Day 023** | [`linux-from-scratch`](file:///Users/tushar/desktop/private/repos/linux-from-scratch) | Phases 106–115: Linux Memory Management: Anonymous memory, page cache, swapiness.  
  *Task:* Demonstrate major vs minor page faults under memory pressure.  
  *Verify:* Solve Broken Labs 19–22.
- [ ] **Day 024** | [`linux-from-scratch`](file:///Users/tushar/desktop/private/repos/linux-from-scratch) | Phases 116–125: Linux Networking Stack: Socket buffers, TCP backlog queue, SYN flood.  
  *Task:* Tune `somaxconn`, `tcp_max_syn_backlog`, and inspect TCP drop counters.  
  *Verify:* Solve Broken Labs 23–26.
- [ ] **Day 025** | [`linux-from-scratch`](file:///Users/tushar/desktop/private/repos/linux-from-scratch) | Phases 126–136: Performance profiling with `perf`, `strace`, and eBPF tracing probes.  
  *Task:* Write an eBPF tracepoint probe counting disk read latency percentiles.  
  *Verify:* Solve Broken Labs 27–32.
- [ ] **Day 026** | [`linux-from-scratch`](file:///Users/tushar/desktop/private/repos/linux-from-scratch) | Project 03: Linux System Monitor TUI.  
  *Task:* Build terminal dashboard showing CPU per core, cgroup memory, disk I/O, and net.  
  *Verify:* Run `linux-from-scratch/projects/03-system-monitor/`.
- [ ] **Day 027** | [`linux-from-scratch`](file:///Users/tushar/desktop/private/repos/linux-from-scratch) | Complete Broken Systems Marathon: Labs 01 to 32 comprehensive review.
- [ ] **Day 028** | [`docker-from-scratch`](file:///Users/tushar/desktop/private/repos/docker-from-scratch) | Phases 01–15: Docker architecture, images, layer caching, and storage drivers.  
  *Task:* Deconstruct tarball layers and build union mount filesystem manually.
- [ ] **Day 029** | [`docker-from-scratch`](file:///Users/tushar/desktop/private/repos/docker-from-scratch) | Phases 16–31: Bridge networks, port mapping via iptables, container debugging.  
  *Task:* Trace iptables NAT rules forwarding host 8080 to container 80.  
  *Verify:* Run `docker-from-scratch/projects/capstone-system-lab/`.
- [ ] **Day 030** | **Milestone 1 Synthesis**: Review OS, Linux, and Docker fundamentals; push all code updates to GitHub.

---

# MONTH 2: Networking Protocols, Language Internals & Low-Level Design (Days 031 – 060)

### Week 5: Computer Networking & Sockets from Scratch
- [ ] **Day 031** | [`computer-networking`](file:///Users/tushar/desktop/private/repos/computer-networking-from-scratch) | Phases 00–15: Ethernet frames, MAC addresses, ARP protocol, raw sockets.  
  *Task:* Write a raw packet sniffer parsing Ethernet and ARP headers.  
  *Verify:* Run `computer-networking-from-scratch/phases/04-ethernet/`.
- [ ] **Day 032** | [`computer-networking`](file:///Users/tushar/desktop/private/repos/computer-networking-from-scratch) | Phases 16–30: IPv4 packet headers, subnetting, CIDR, TTL, and MTU fragmentation.  
  *Task:* Implement IPv4 packet checksum calculation and verification.
- [ ] **Day 033** | [`computer-networking`](file:///Users/tushar/desktop/private/repos/computer-networking-from-scratch) | Phases 31–45: UDP protocol, datagram delivery, socket buffers, and packet loss.  
  *Task:* Build reliable UDP client using Stop-and-Wait ACK packets.
- [ ] **Day 034** | [`computer-networking`](file:///Users/tushar/desktop/private/repos/computer-networking-from-scratch) | Phases 46–60: TCP Header structure, 3-way handshake (SYN, SYN-ACK, ACK), teardown.  
  *Task:* Trace exact TCP state transitions: CLOSED -> LISTEN -> SYN_RCVD -> ESTABLISHED.
- [ ] **Day 035** | [`computer-networking`](file:///Users/tushar/desktop/private/repos/computer-networking-from-scratch) | Phases 61–75: TCP Sequence and Acknowledgment numbering, sliding window flow control.  
  *Task:* Build sliding window packet buffer simulator tracking in-flight un-acked bytes.
- [ ] **Day 036** | [`computer-networking`](file:///Users/tushar/desktop/private/repos/computer-networking-from-scratch) | Phases 76–90: TCP Congestion Control: Slow Start, Congestion Avoidance, AIMD, Reno vs Cubic.  
  *Task:* Graph congestion window (`cwnd`) curve under synthetic packet drop.
- [ ] **Day 037** | [`computer-networking`](file:///Users/tushar/desktop/private/repos/computer-networking-from-scratch) | Project 04 & 05: TCP State Machine & Multi-Room Epoll Chat Server.  
  *Task:* Pure socket implementation of non-blocking TCP chat server.  
  *Verify:* `python computer-networking-from-scratch/projects/121-project-raw-tcp-chat/server.py`.

### Week 6: DNS, TLS, HTTP Wire Protocol & WebSockets
- [ ] **Day 038** | [`computer-networking`](file:///Users/tushar/desktop/private/repos/computer-networking-from-scratch) | Phases 91–105: DNS protocol: Queries, record types (A, AAAA, CNAME, MX), recursive resolution.  
  *Task:* Build a UDP DNS client from scratch formatting raw wire query packets.  
  *Verify:* Query `8.8.8.8` for `example.com` and parse IP from DNS answers.
- [ ] **Day 039** | [`computer-networking`](file:///Users/tushar/desktop/private/repos/computer-networking-from-scratch) | Phases 106–120: TLS 1.3 handshake: ClientHello, Key Exchange, Certificates, Symmetric session.  
  *Task:* Trace encrypted TLS record frames with Wireshark/tcpdump.
- [ ] **Day 040** | [`computer-networking`](file:///Users/tushar/desktop/private/repos/computer-networking-from-scratch) | Phases 121–130: HTTP/1.1 Wire protocol parsing: CRLF framing, headers, chunked transfer encoding.  
  *Task:* Parse raw socket byte streams into HTTP request objects without web frameworks.
- [ ] **Day 041** | [`computer-networking`](file:///Users/tushar/desktop/private/repos/computer-networking-from-scratch) | Phases 131–139: WebSockets handshake (`Upgrade: websocket`) and binary frame masking.  
  *Task:* Implement WebSocket frame XOR masking and unmasking.
- [ ] **Day 042** | [`computer-networking`](file:///Users/tushar/desktop/private/repos/computer-networking-from-scratch) | Project 07: Reverse Proxy & L4 Load Balancer.  
  *Task:* Build TCP proxy distributing connections across 3 backend servers.  
  *Verify:* Run test suite in `computer-networking-from-scratch/projects/`.
- [ ] **Day 043** | [`java-from-scratch`](file:///Users/tushar/desktop/private/repos/java-from-scratch) | Phases 01–25: Java 21+ memory model, Heap vs Stack, JIT compilation, GC generational hypothesis.  
  *Task:* Inspect bytecode with `javap -c` and profile object allocations.
- [ ] **Day 044** | [`java-from-scratch`](file:///Users/tushar/desktop/private/repos/java-from-scratch) | Phases 26–50: Concurrency in Java: `volatile`, `synchronized`, CAS (`AtomicInteger`), memory barriers.  
  *Task:* Build lock-free concurrent queue using `AtomicReference`.  
  *Verify:* `mvn test -Dtest=LockFreeQueueTest`.

### Week 7: JVM Internals, Virtual Threads & Low-Level Design
- [ ] **Day 045** | [`java-from-scratch`](file:///Users/tushar/desktop/private/repos/java-from-scratch) | Phases 51–75: Java ExecutorService, thread pools, ForkJoinPool, and Project Loom Virtual Threads.  
  *Task:* Benchmark 100,000 virtual threads handling I/O vs 200 platform threads.
- [ ] **Day 046** | [`java-from-scratch`](file:///Users/tushar/desktop/private/repos/java-from-scratch) | Phases 76–110: Garbage collection algorithms: G1, ZGC, generational ZGC pause times.  
  *Task:* Analyze GC log flags (`-Xlog:gc*`) under heavy allocation pressure.
- [ ] **Day 047** | [`java-from-scratch`](file:///Users/tushar/desktop/private/repos/java-from-scratch) | Projects 01–05: High-throughput thread pool & Concurrent Cache.  
  *Task:* Implement fixed-size bounded worker thread pool with rejection policies.  
  *Verify:* `mvn -C java-from-scratch test`.
- [ ] **Day 048** | [`low-level-design`](file:///Users/tushar/desktop/private/repos/low-level-design-from-scratch) | Phases 01–25: SOLID Principles from first principles: Single Responsibility, Open-Closed, Liskov.  
  *Task:* Refactor a rigid 500-line monolithic class into decoupled, testable components.
- [ ] **Day 049** | [`low-level-design`](file:///Users/tushar/desktop/private/repos/low-level-design-from-scratch) | Phases 26–50: Creational & Structural Patterns: Factory, Builder, Decorator, Adapter, Proxy.  
  *Task:* Build dynamic logging and metrics proxy wrapper around service interface.
- [ ] **Day 050** | [`low-level-design`](file:///Users/tushar/desktop/private/repos/low-level-design-from-scratch) | Phases 51–75: Behavioral Patterns: Strategy, Observer, State, Command, Template Method.  
  *Task:* Implement an order state machine enforcing valid transitions: NEW -> PAID -> SHIPPED.
- [ ] **Day 051** | [`low-level-design`](file:///Users/tushar/desktop/private/repos/low-level-design-from-scratch) | Project 01–05: Parking Lot & Rate Limiter LLD.  
  *Task:* Complete full object-oriented model with concurrency locks for Parking Lot.  
  *Verify:* `mvn -C low-level-design-from-scratch test`.

### Week 8: Advanced LLD Refactoring Katas & Production Models
- [ ] **Day 052** | [`low-level-design`](file:///Users/tushar/desktop/private/repos/low-level-design-from-scratch) | Project 06–10: Elevator System & Splitwise Expense Sharing.  
  *Task:* Model multi-elevator dispatch algorithm (SCAN / LOOK) and exact currency split graph.
- [ ] **Day 053** | [`low-level-design`](file:///Users/tushar/desktop/private/repos/low-level-design-from-scratch) | Project 11–15: In-Memory Key-Value Store & Distributed Cache LLD.  
  *Task:* Implement LRU / LFU cache eviction policies with $O(1)$ get and put operations.
- [ ] **Day 054** | [`low-level-design`](file:///Users/tushar/desktop/private/repos/low-level-design-from-scratch) | Project 16–20: Movie Ticket Booking System (BookMyShow) LLD.  
  *Task:* Design seat lock expiration with optimistic locking and thread-safe reservation.
- [ ] **Day 055** | [`low-level-design`](file:///Users/tushar/desktop/private/repos/low-level-design-from-scratch) | Project 21–24: Task Scheduler (Cron/Quartz) LLD.  
  *Task:* PriorityQueue-based timer thread executing recurrent jobs.
- [ ] **Day 056** | [`low-level-design`](file:///Users/tushar/desktop/private/repos/low-level-design-from-scratch) | Refactoring Labs Marathon: Solve refactoring katas in `low-level-design-from-scratch/katas/`.
- [ ] **Day 057** | Clean Code & Concurrency Review: Run all 34 LLD tests and all 700 Java tests.
- [ ] **Day 058** | Systems Integration Lab: Connect Java socket client to Linux epoll chat server.
- [ ] **Day 059** | Architectural Synthesis: Map design patterns to operating system abstractions.
- [ ] **Day 060** | **Milestone 2 Synthesis**: Commit all networking, Java, and LLD implementations to GitHub.

---

# MONTH 3: Exhaustive Backend Engineering & Distributed Mechanics (Days 061 – 090)

### Week 9: Sockets to Frameworks, Routing & State
- [ ] **Day 061** | [`backend-engineering`](file:///Users/tushar/desktop/private/repos/backend-engineering-from-scratch) | Phases 00–15: TCP server, minimal HTTP server, request lifecycle, headers, query params.  
  *Task:* Write HTTP server parsing raw string requests into route handlers.  
  *Verify:* `pytest backend-engineering-from-scratch/phases/02-build-a-tcp-server/tests/`.
- [ ] **Day 062** | [`backend-engineering`](file:///Users/tushar/desktop/private/repos/backend-engineering-from-scratch) | Phases 16–30: Connection pooling, transactions, atomicity, and rollback mechanics.  
  *Task:* Build connection pool with maximum active limits and timeout queue.  
  *Verify:* `pytest backend-engineering-from-scratch/phases/20-connection-pooling/tests/`.
- [ ] **Day 063** | [`backend-engineering`](file:///Users/tushar/desktop/private/repos/backend-engineering-from-scratch) | Phases 31–45: Middleware chains, onion-layer dispatch, authentication context injection.  
  *Task:* Build composable middleware pipeline (Timing, Auth, RequestID).  
  *Verify:* Solve Broken Labs 01–03 in `backend-engineering-from-scratch/broken-systems/`.
- [ ] **Day 064** | [`backend-engineering`](file:///Users/tushar/desktop/private/repos/backend-engineering-from-scratch) | Phases 46–60: Caching strategies: Cache-Aside, Write-Through, Write-Behind, dogpiling.  
  *Task:* Implement cache stampede mutex lock preventing database collapse.  
  *Verify:* Solve Broken Labs 04–07.
- [ ] **Day 065** | [`backend-engineering`](file:///Users/tushar/desktop/private/repos/backend-engineering-from-scratch) | Phases 61–75: Resilience patterns: Timeouts, exponential backoff, jitter, circuit breakers.  
  *Task:* Implement 3-state Circuit Breaker (CLOSED -> OPEN -> HALF_OPEN).  
  *Verify:* `pytest backend-engineering-from-scratch/phases/67-circuit-breaker/tests/`.
- [ ] **Day 066** | [`backend-engineering`](file:///Users/tushar/desktop/private/repos/backend-engineering-from-scratch) | Phases 76–90: Concurrency models: Sync vs Threaded vs Async, event loop blocking.  
  *Task:* Demonstrate event loop stall caused by synchronous file read inside async route.  
  *Verify:* Solve Broken Lab 11 (blocking call in event loop).
- [ ] **Day 067** | [`backend-engineering`](file:///Users/tushar/desktop/private/repos/backend-engineering-from-scratch) | Project 01 & 02: URL Shortener & Todo Task API.  
  *Task:* Implement high-throughput URL shortener with Base62 encoding and Redis cache.  
  *Verify:* `pytest backend-engineering-from-scratch/projects/01-url-shortener/tests/`.

### Week 10: Asynchronous Jobs, Outbox Pattern & Security
- [ ] **Day 068** | [`backend-engineering`](file:///Users/tushar/desktop/private/repos/backend-engineering-from-scratch) | Phases 91–105: Background workers, durable queues, consumer ack/nack, dead-letter queues.  
  *Task:* Implement job queue with retry counts and dead-letter queue escalation.  
  *Verify:* Solve Broken Lab 05 (worker lag unbounded queue).
- [ ] **Day 069** | [`backend-engineering`](file:///Users/tushar/desktop/private/repos/backend-engineering-from-scratch) | Phases 106–120: Transactional Outbox Pattern & Event Publishing.  
  *Task:* Atomically insert order row and outbox message in same SQL transaction; write poller.  
  *Verify:* Solve Broken Lab 23 (dual-write inconsistency).
- [ ] **Day 070** | [`backend-engineering`](file:///Users/tushar/desktop/private/repos/backend-engineering-from-scratch) | Phases 121–135: Idempotency keys, distributed deduplication, idempotency header validation.  
  *Task:* Build idempotency middleware caching responses by `Idempotency-Key` header.  
  *Verify:* Solve Broken Lab 06 (duplicate jobs missing idempotency).
- [ ] **Day 071** | [`backend-engineering`](file:///Users/tushar/desktop/private/repos/backend-engineering-from-scratch) | Phases 136–150: Backend Security: SQL injection, CORS headers, CSRF tokens, JWT validation.  
  *Task:* Trace SQL injection escape mechanics and verify constant-time JWT signature verification.  
  *Verify:* Solve Broken Labs 13–16.
- [ ] **Day 072** | [`backend-engineering`](file:///Users/tushar/desktop/private/repos/backend-engineering-from-scratch) | Phases 151–165: Rate limiting algorithms: Token Bucket, Leaky Bucket, Sliding Window.  
  *Task:* Implement sliding window log rate limiter in Redis Lua script.  
  *Verify:* Solve Broken Lab 25.
- [ ] **Day 073** | [`backend-engineering`](file:///Users/tushar/desktop/private/repos/backend-engineering-from-scratch) | Phases 166–180: Observability: RED metrics (Rate, Errors, Duration), OpenTelemetry context.  
  *Task:* Propagate W3C `traceparent` header across HTTP client calls.  
  *Verify:* `pytest backend-engineering-from-scratch/phases/93-tracing/tests/`.
- [ ] **Day 074** | [`backend-engineering`](file:///Users/tushar/desktop/private/repos/backend-engineering-from-scratch) | Projects 04 & 09: E-Commerce Backend & Webhook Delivery Platform.  
  *Task:* Build webhook delivery platform with HMAC signing, retries, and backoff.  
  *Verify:* `pytest backend-engineering-from-scratch/projects/09-webhook-delivery-platform/tests/`.

### Week 11: Capstone Backends & Failure Injections
- [ ] **Day 075** | [`backend-engineering`](file:///Users/tushar/desktop/private/repos/backend-engineering-from-scratch) | Phases 181–189: Capstone 1: Production Modular Monolith.  
  *Task:* Unify Auth, Catalog, Orders, Notifications, and Outbox in clean layered architecture.  
  *Verify:* `pytest backend-engineering-from-scratch/apps/01_modular_monolith/tests/`.
- [ ] **Day 076** | [`backend-engineering`](file:///Users/tushar/desktop/private/repos/backend-engineering-from-scratch) | Capstone 2: Failure-Driven Backend.  
  *Task:* Inject database latency, cache crashes, and thread exhaustion into Capstone 1.  
  *Verify:* `pytest backend-engineering-from-scratch/apps/02_failure_driven_backend/tests/`.
- [ ] **Day 077** | [`backend-engineering`](file:///Users/tushar/desktop/private/repos/backend-engineering-from-scratch) | Capstone 3: Extract One Service (Notification Microservice).  
  *Task:* Decouple notification worker into standalone service communicating via HTTP events.  
  *Verify:* `pytest backend-engineering-from-scratch/apps/03_extracted_notification_service/tests/`.
- [ ] **Day 078** | [`backend-engineering`](file:///Users/tushar/desktop/private/repos/backend-engineering-from-scratch) | Capstone 4: Production Readiness Review (PRR).  
  *Task:* Audit Capstone 1 against 50-point production checklist (graceful shutdown, probes).  
  *Verify:* `pytest backend-engineering-from-scratch/apps/04_production_readiness_review/tests/`.
- [ ] **Day 079** | [`backend-engineering`](file:///Users/tushar/desktop/private/repos/backend-engineering-from-scratch) | Broken Systems Marathon 1: Solve and document Broken Labs 17–24.
- [ ] **Day 080** | [`backend-engineering`](file:///Users/tushar/desktop/private/repos/backend-engineering-from-scratch) | Broken Systems Marathon 2: Solve and document Broken Labs 25–32.
- [ ] **Day 081** | Full Backend Test Suite Audit: Verify all 841 standard backend tests pass cleanly.

### Week 12: Advanced Distributed Systems, Consensus, Storage & Security (Part 20)
- [ ] **Day 082** | [`backend-engineering`](file:///Users/tushar/desktop/private/repos/backend-engineering-from-scratch) | Phase 190 & 191: Consensus Safety, Quorum Math & Raft Leader Election.  
  *Task:* Implement Raft role transitions, randomized election timeouts, and RequestVote RPC.  
  *Verify:* `pytest backend-engineering-from-scratch/phases/190-consensus-safety-and-quorum-math/tests/` and `191`.
- [ ] **Day 083** | [`backend-engineering`](file:///Users/tushar/desktop/private/repos/backend-engineering-from-scratch) | Phase 192 & 193: Raft Log Replication & Two-Phase Commit / Sagas.  
  *Task:* Implement AppendEntries consistency checks, log matching, and 2PC coordinator.  
  *Verify:* `pytest backend-engineering-from-scratch/phases/192-raft-log-replication-and-commit-index/tests/` and `193`.
- [ ] **Day 084** | [`backend-engineering`](file:///Users/tushar/desktop/private/repos/backend-engineering-from-scratch) | Phase 194 & 195: Protobuf Wire Format & HTTP/2 Stream Multiplexing.  
  *Task:* Implement LEB128 Varint/ZigZag bit encoding and 9-byte HTTP/2 frame headers.  
  *Verify:* `pytest backend-engineering-from-scratch/phases/194-protobuf-wire-format-and-varints/tests/` and `195`.
- [ ] **Day 085** | [`backend-engineering`](file:///Users/tushar/desktop/private/repos/backend-engineering-from-scratch) | Phase 196 & 197: gRPC Client Stub, Deadlines & Client-Side Load Balancing.  
  *Task:* Parse `grpc-timeout` headers, cancel contexts, and implement Round-Robin balancer.  
  *Verify:* `pytest backend-engineering-from-scratch/phases/196-grpc-client-stub-and-deadlines/tests/` and `197`.
- [ ] **Day 086** | [`backend-engineering`](file:///Users/tushar/desktop/private/repos/backend-engineering-from-scratch) | Phase 198 & 199: Storage Engine WAL & LSM-Tree MemTable/SSTables.  
  *Task:* Binary WAL with CRC32 checksums and immutable SSTable flushing with sparse index.  
  *Verify:* `pytest backend-engineering-from-scratch/phases/198-storage-engine-write-ahead-log/tests/` and `199`.
- [ ] **Day 087** | [`backend-engineering`](file:///Users/tushar/desktop/private/repos/backend-engineering-from-scratch) | Phase 200 & 201: LSM Leveled Compaction & B+ Tree Buffer Pool Manager.  
  *Task:* Implement 2-pointer SSTable merge with tombstone GC, and LRU page buffer pool.  
  *Verify:* `pytest backend-engineering-from-scratch/phases/200-lsm-leveled-compaction/tests/` and `201`.
- [ ] **Day 088** | [`backend-engineering`](file:///Users/tushar/desktop/private/repos/backend-engineering-from-scratch) | Phase 202 & 203: HMAC Constant-Time Hashing & AES-GCM AEAD Encryption.  
  *Task:* Implement constant-time MAC verification and AEAD encryption envelope.  
  *Verify:* `pytest backend-engineering-from-scratch/phases/202-cryptographic-hashing-and-hmac/tests/` and `203`.
- [ ] **Day 089** | [`backend-engineering`](file:///Users/tushar/desktop/private/repos/backend-engineering-from-scratch) | Phase 204 & 205: TLS 1.3 Handshake, mTLS & Zero-Trust PASETO Tokens.  
  *Task:* Implement Mutual TLS certificate chain validation and PASETO v4 token generator.  
  *Verify:* `pytest backend-engineering-from-scratch/phases/204-tls-handshake-and-mtls-verification/tests/` and `205`.
- [ ] **Day 090** | **Milestone 3 Synthesis**: Run full `backend-engineering` test suite (**905 passed**); push all updates to GitHub.

---

# MONTH 4: The Persistence, Cache & Distributed Streaming Tier (Days 091 – 120)

### Week 13: Relational Storage Engines & SQL Optimization
- [ ] **Day 091** | [`database-and-sql`](file:///Users/tushar/desktop/private/repos/database-and-sql-from-scratch) | Phases 00–15: Relational algebra, tuple storage, page headers, row pointer slots.  
  *Task:* Inspect binary slotted-page structure in database storage engine.
- [ ] **Day 092** | [`database-and-sql`](file:///Users/tushar/desktop/private/repos/database-and-sql-from-scratch) | Phases 16–30: B+ Tree indexing: Search, range scans, page splits, and fill factor.  
  *Task:* Trace binary search through internal index pages down to leaf nodes.
- [ ] **Day 093** | [`database-and-sql`](file:///Users/tushar/desktop/private/repos/database-and-sql-from-scratch) | Phases 31–45: Query execution plans: Sequential scan vs Index scan vs Bitmap scan.  
  *Task:* Analyze `EXPLAIN (ANALYZE, BUFFERS)` output for complex query joins.
- [ ] **Day 094** | [`database-and-sql`](file:///Users/tushar/desktop/private/repos/database-and-sql-from-scratch) | Phases 46–60: Join algorithms: Nested Loop, Hash Join, Merge Join.  
  *Task:* Benchmark Hash Join vs Nested Loop join under increasing table cardinalities.
- [ ] **Day 095** | [`database-and-sql`](file:///Users/tushar/desktop/private/repos/database-and-sql-from-scratch) | Phases 61–75: ACID Transactions, WAL, checkpointing, and ARIES recovery algorithm.  
  *Task:* Simulate crash recovery: Analysis, Redo, and Undo passes over WAL.
- [ ] **Day 096** | [`database-and-sql`](file:///Users/tushar/desktop/private/repos/database-and-sql-from-scratch) | Phases 76–90: Concurrency control: 2PL (Two-Phase Locking), Deadlocks, MVCC, Visibility maps.  
  *Task:* Demonstrate non-repeatable read vs phantom read vs write skew anomalies.
- [ ] **Day 097** | [`database-and-sql`](file:///Users/tushar/desktop/private/repos/database-and-sql-from-scratch) | Project 02: Build a B+ Tree Engine from Scratch.  
  *Task:* Implement node insertion, key redistribution, and node splitting in pure Python/C.  
  *Verify:* Run test suite in `database-and-sql-from-scratch/projects/02-b-plus-tree-engine/`.

### Week 14: Redis Internals & In-Memory Data Structures
- [ ] **Day 098** | [`redis-from-scratch`](file:///Users/tushar/desktop/private/repos/redis-from-scratch) | Phases 00–12: Redis architecture, single-threaded event loop, SDS (Simple Dynamic Strings).  
  *Task:* Implement SDS in C with preallocated buffer capacity and $O(1)$ length lookups.
- [ ] **Day 099** | [`redis-from-scratch`](file:///Users/tushar/desktop/private/repos/redis-from-scratch) | Phases 13–24: Hash tables, progressive rehashing, ziplists, and skiplist indexing.  
  *Task:* Simulate dual-table progressive rehashing moving 10 buckets per lookup.
- [ ] **Day 100** | [`redis-from-scratch`](file:///Users/tushar/desktop/private/repos/redis-from-scratch) | Phases 25–35: RESP (REdis Serialization Protocol) parser: Strings, Arrays, Integers, Errors.  
  *Task:* Build pure Python parser reading raw RESP byte streams from TCP sockets.  
  *Verify:* `python redis-from-scratch/projects/01-resp-protocol-server/server.py`.
- [ ] **Day 101** | [`redis-from-scratch`](file:///Users/tushar/desktop/private/repos/redis-from-scratch) | Phases 36–45: Memory eviction: Approximate LRU, LFU, maxmemory limits, TTL expiration.  
  *Task:* Implement 24-bit LRU clock sampling algorithm.
- [ ] **Day 102** | [`redis-from-scratch`](file:///Users/tushar/desktop/private/repos/redis-from-scratch) | Phases 46–51: Persistence (RDB fork copy-on-write, AOF rewrite) & Redlock distributed locks.  
  *Task:* Implement distributed lock with random token verification and TTL safety margin.  
  *Verify:* Run tests in `redis-from-scratch/projects/03-distributed-lock-manager/`.
- [ ] **Day 103** | [`redis-from-scratch`](file:///Users/tushar/desktop/private/repos/redis-from-scratch) | Project 02: Build an In-Memory RESP Redis Clone.  
  *Task:* Implement `GET`, `SET`, `DEL`, `EXPIRE`, and `MSET` over TCP sockets.
- [ ] **Day 104** | [`redis-from-scratch`](file:///Users/tushar/desktop/private/repos/redis-from-scratch) | Redis Benchmarking: Profile RPS and latency using `redis-benchmark`.

### Week 15: Apache Kafka & Distributed Log Architecture
- [ ] **Day 105** | [`kafka-from-scratch`](file:///Users/tushar/desktop/private/repos/kafka-from-scratch) | Phases 00–15: The Log as the universal abstraction: append-only commits, segment files.  
  *Task:* Implement binary segment file manager with `.index` and `.log` rolling.  
  *Verify:* Run `kafka-from-scratch/projects/01-append-only-commit-log/`.
- [ ] **Day 106** | [`kafka-from-scratch`](file:///Users/tushar/desktop/private/repos/kafka-from-scratch) | Phases 16–30: Zero-copy I/O: Linux `sendfile` syscall, OS page cache, network socket transfer.  
  *Task:* Benchmark user-space read/write loop vs kernel-space zero-copy sendfile.
- [ ] **Day 107** | [`kafka-from-scratch`](file:///Users/tushar/desktop/private/repos/kafka-from-scratch) | Phases 31–45: Producer internals: RecordBatch, compression (Snappy, Zstd), `acks=all`, idempotence.  
  *Task:* Build producer buffer batching records by partition with linger.ms timers.
- [ ] **Day 108** | [`kafka-from-scratch`](file:///Users/tushar/desktop/private/repos/kafka-from-scratch) | Phases 46–55: Consumer groups, partition assignment strategies (Range, RoundRobin, Sticky).  
  *Task:* Implement consumer group coordinator rebalance state machine.
- [ ] **Day 109** | [`kafka-from-scratch`](file:///Users/tushar/desktop/private/repos/kafka-from-scratch) | Phases 56–68: Exactly-Once Semantics (EOS), transactional producer, KRaft metadata quorum.  
  *Task:* Simulate two-phase commit transaction coordinator marking records with commit markers.  
  *Verify:* Run `kafka-from-scratch/tests/test_kafka.py`.
- [ ] **Day 110** | [`kafka-from-scratch`](file:///Users/tushar/desktop/private/repos/kafka-from-scratch) | Project 02: Build a Partitioned Message Broker from Scratch.  
  *Task:* Support multi-partition publish/subscribe over TCP.
- [ ] **Day 111** | Failure Drills: Simulate leader partition failure and ISR (In-Sync Replicas) promotion.

### Week 16: Elasticsearch, Inverted Indexes & NoSQL
- [ ] **Day 112** | [`elasticsearch`](file:///Users/tushar/desktop/private/repos/elasticsearch-from-scratch) | Phases 00–20: Information retrieval: tokenization, stop-words, stemmers, inverted index.  
  *Task:* Build in-memory inverted index mapping terms to document IDs and positions.  
  *Verify:* `python elasticsearch-from-scratch/projects/01-inverted-index/`.
- [ ] **Day 113** | [`elasticsearch`](file:///Users/tushar/desktop/private/repos/elasticsearch-from-scratch) | Phases 21–40: Postings lists, variable-byte compression, Roaring Bitmaps.  
  *Task:* Implement Roaring Bitmap compression for dense and sparse posting lists.
- [ ] **Day 114** | [`elasticsearch`](file:///Users/tushar/desktop/private/repos/elasticsearch-from-scratch) | Phases 41–60: BM25 Ranking Algorithm: Term frequency saturation, document length penalty.  
  *Task:* Implement BM25 scoring formula and rank query results.  
  *Verify:* Run `elasticsearch-from-scratch/projects/02-bm25-ranking/`.
- [ ] **Day 115** | [`elasticsearch`](file:///Users/tushar/desktop/private/repos/elasticsearch-from-scratch) | Phases 61–75: Lucene immutable segments, merge policy, query coordinator.  
  *Task:* Demonstrate background segment merge re-indexing deleted documents.
- [ ] **Day 116** | [`elasticsearch`](file:///Users/tushar/desktop/private/repos/elasticsearch-from-scratch) | Phases 76–88: Sharding, primary/replica routing, distributed aggregations.  
  *Task:* Implement scatter-gather query coordinator merging top-N results from 3 shards.
- [ ] **Day 117** | [`nosql-databases`](file:///Users/tushar/desktop/private/repos/nosql-databases-and-query-languages-from-scratch) | Document & Key-Value Engines: MongoDB BSON vs DynamoDB partition keys.  
  *Task:* Model high-cardinality partition keys to prevent hot partition throttling.
- [ ] **Day 118** | [`nosql-databases`](file:///Users/tushar/desktop/private/repos/nosql-databases-and-query-languages-from-scratch) | Wide-Column & Graph Engines: Cassandra CQL partitions vs Neo4j graph traversals.  
  *Task:* Implement BFS graph traversal query in pure Python.
- [ ] **Day 119** | Polyglot Persistence Lab: Integrate SQL, Redis, and Kafka in unified event stream.
- [ ] **Day 120** | **Milestone 4 Synthesis**: Run database, Redis, Kafka, and Elasticsearch test suites; commit to GitHub.

---

# MONTH 5: Analytical Storage, Big Data Pipelines & Cloud Infrastructure (Days 121 – 150)

### Week 17: OLAP Databases & Vectorized Query Engines
- [ ] **Day 121** | [`olap-databases`](file:///Users/tushar/desktop/private/repos/olap-databases-and-analytical-querying-from-scratch) | Phases 00–25: Row vs Columnar storage: Parquet layout, footers, dictionary encoding.  
  *Task:* Parse raw Parquet footer metadata and read single column without touching others.  
  *Verify:* Solve Broken Lab 01 in `olap-databases.../broken-systems/`.
- [ ] **Day 122** | [`olap-databases`](file:///Users/tushar/desktop/private/repos/olap-databases-and-analytical-querying-from-scratch) | Phases 26–50: Vectorized execution: Processing vectors of 1024 values in CPU L1/L2 cache.  
  *Task:* Benchmark scalar row-at-a-time loop vs SIMD-style vectorized array filter.
- [ ] **Day 123** | [`olap-databases`](file:///Users/tushar/desktop/private/repos/olap-databases-and-analytical-querying-from-scratch) | Phases 51–80: ClickHouse MergeTree engine: Sparse primary index, marks, data parts.  
  *Task:* Trace binary search across index marks to skip 95% of data granules.
- [ ] **Day 124** | [`olap-databases`](file:///Users/tushar/desktop/private/repos/olap-databases-and-analytical-querying-from-scratch) | Phases 81–120: Compression algorithms: LZ4, ZSTD, Delta encoding, Gorilla floating point.  
  *Task:* Implement Gorilla XOR delta-of-deltas compression for time-series timestamps.
- [ ] **Day 125** | [`olap-databases`](file:///Users/tushar/desktop/private/repos/olap-databases-and-analytical-querying-from-scratch) | Phases 121–160: Partition pruning, projections, materialized views, real-time ingestion.  
  *Task:* Build materialized view aggregating 10 million events into minute buckets.
- [ ] **Day 126** | [`olap-databases`](file:///Users/tushar/desktop/private/repos/olap-databases-and-analytical-querying-from-scratch) | Project 01 & 02: Build a Columnar File Format & Vectorized Filter Engine.  
  *Task:* Implement column-oriented scanner executing `SELECT sum(amount) WHERE age > 30`.  
  *Verify:* Run test suite in `olap-databases.../projects/`.
- [ ] **Day 127** | [`olap-databases`](file:///Users/tushar/desktop/private/repos/olap-databases-and-analytical-querying-from-scratch) | Broken Labs Marathon: Solve 10 broken labs in `olap-databases/broken-systems/`.

### Week 18: Data Engineering, Spark & dbt Transformations
- [ ] **Day 128** | [`data-engineering`](file:///Users/tushar/desktop/private/repos/data-engineering-from-scratch) | Phases 00–25: Batch vs Streaming, Bronze/Silver/Gold medallion architecture, schema evolution.  
  *Task:* Build ingestion pipeline validating JSON schema against strict contract.  
  *Verify:* `pytest data-engineering-from-scratch/exercises/01-files-and-formats/`.
- [ ] **Day 129** | [`data-engineering`](file:///Users/tushar/desktop/private/repos/data-engineering-from-scratch) | Phases 26–50: Apache Spark internals: Catalyst query optimizer, physical execution plans.  
  *Task:* Analyze Spark explain plan identifying wide vs narrow transformations.
- [ ] **Day 130** | [`data-engineering`](file:///Users/tushar/desktop/private/repos/data-engineering-from-scratch) | Phases 51–75: Spark Shuffling: Hash partitioners, shuffle spill to disk, broadcast joins.  
  *Task:* Resolve shuffle skew using salting techniques.  
  *Verify:* Solve Broken Lab 08 in `data-engineering/broken-systems/`.
- [ ] **Day 131** | [`data-engineering`](file:///Users/tushar/desktop/private/repos/data-engineering-from-scratch) | Phases 76–105: dbt (Data Build Tool): Ephemeral, view, table, and incremental models.  
  *Task:* Write idempotent incremental dbt model handling out-of-order data.  
  *Verify:* `pytest data-engineering-from-scratch/exercises/05-dbt-transformations/`.
- [ ] **Day 132** | [`data-engineering`](file:///Users/tushar/desktop/private/repos/data-engineering-from-scratch) | Phases 106–135: Change Data Capture (CDC): Debezium WAL decoding, Kafka Connect.  
  *Task:* Stream PostgreSQL WAL changes into Kafka topic and materialize in DuckDB.
- [ ] **Day 133** | [`data-engineering`](file:///Users/tushar/desktop/private/repos/data-engineering-from-scratch) | Phases 136–165: Streaming aggregations: Tumbling windows, sliding windows, watermarking.  
  *Task:* Implement 1-minute tumbling window aggregating clickstream events with 5s watermark.  
  *Verify:* `pytest data-engineering-from-scratch/exercises/10-streaming-systems/`.
- [ ] **Day 134** | [`data-engineering`](file:///Users/tushar/desktop/private/repos/data-engineering-from-scratch) | Broken Labs Marathon: Solve 15 broken data labs in `data-engineering-from-scratch/`.

### Week 19: Kubernetes Orchestration & Control Planes
- [ ] **Day 135** | [`kubernetes-from-scratch`](file:///Users/tushar/desktop/private/repos/kubernetes-from-scratch) | Phases 00–20: Kubernetes architecture: API Server, etcd distributed consensus, Kubelet.  
  *Task:* Inspect etcd key-value paths storing pod specifications.
- [ ] **Day 136** | [`kubernetes-from-scratch`](file:///Users/tushar/desktop/private/repos/kubernetes-from-scratch) | Phases 21–40: Declarative state & The Reconciliation Loop: Desired state vs Observed state.  
  *Task:* Write a mini control loop in Python observing and reconciling container count.
- [ ] **Day 137** | [`kubernetes-from-scratch`](file:///Users/tushar/desktop/private/repos/kubernetes-from-scratch) | Phases 41–60: Pod Lifecycle: InitContainers, sidecars, liveness, readiness, startup probes.  
  *Task:* Configure liveness probe and diagnose probe death loop.
- [ ] **Day 138** | [`kubernetes-from-scratch`](file:///Users/tushar/desktop/private/repos/kubernetes-from-scratch) | Phases 61–80: Service Discovery & Cluster Networking: ClusterIP, kube-proxy iptables/IPVS.  
  *Task:* Trace iptables packet mangling directing ClusterIP traffic to pod endpoints.
- [ ] **Day 139** | [`kubernetes-from-scratch`](file:///Users/tushar/desktop/private/repos/kubernetes-from-scratch) | Phases 81–100: Resource Management: Requests, limits, CFS throttling, PodDisruptionBudgets (PDB).  
  *Task:* Configure PDB and simulate zero-downtime node drain.
- [ ] **Day 140** | [`kubernetes-from-scratch`](file:///Users/tushar/desktop/private/repos/kubernetes-from-scratch) | Phases 101–121: Horizontal Pod Autoscaler (HPA) & Custom Resource Definitions (CRDs).  
  *Task:* Write custom controller watching a `DatabaseBackup` CRD.  
  *Verify:* Run scripts in `kubernetes-from-scratch/manifests/`.
- [ ] **Day 141** | Kubernetes Cluster Lab: Deploy multi-service microservice stack with ingress routing.

### Week 20: Cloud Systems & AWS Architectures
- [ ] **Day 142** | [`aws-from-scratch`](file:///Users/tushar/desktop/private/repos/aws-from-scratch) | Phases 00–04: VPC Networking, subnets, route tables, Internet Gateway, NAT Gateways.  
  *Task:* Diagram multi-AZ isolated tier architecture with private subnet database access.
- [ ] **Day 143** | [`aws-from-scratch`](file:///Users/tushar/desktop/private/repos/aws-from-scratch) | Phases 05–08: IAM Security Perimeters, least privilege policies, assume-role STS tokens.  
  *Task:* Write strict IAM policy granting S3 access scoped to dynamic tenant prefix.
- [ ] **Day 144** | [`aws-from-scratch`](file:///Users/tushar/desktop/private/repos/aws-from-scratch) | Phases 09–13: S3 consistency models, CloudFront CDN edge caching, and Lambda execution.  
  *Task:* Trace cache invalidation mechanics and S3 strong consistency invariants.
- [ ] **Day 145** | [`aws-from-scratch`](file:///Users/tushar/desktop/private/repos/aws-from-scratch) | Project 02: High-Availability Web Application Architecture.  
  *Task:* Design multi-AZ auto-scaling web application with ALB, RDS read replica, and Redis.
- [ ] **Day 146** | [`aws-from-scratch`](file:///Users/tushar/desktop/private/repos/aws-from-scratch) | Project 07: Tiny Cloud Simulator.  
  *Task:* Run local cloud resource simulation in Python.  
  *Verify:* Run `aws-from-scratch/projects/project-07-tiny-cloud-simulator/`.
- [ ] **Day 147** | Multi-Region Active-Active Cloud Design: Tradeoffs between latency and cross-region sync.
- [ ] **Day 148** | Cloud Cost Optimization Lab: Modeling compute, egress bandwidth, and storage costs.
- [ ] **Day 149** | End-to-End Infrastructure Integration: Docker -> K8s -> AWS topology review.
- [ ] **Day 150** | **Milestone 5 Synthesis**: Run all OLAP, data engineering, and K8s validation scripts; commit to GitHub.

---

# MONTH 6: Distributed Architecture, Production SRE, AI Systems & Staff Leadership (Days 151 – 180)

### Week 21: System Design from First Principles (201 Phases & 899 Tests)
- [ ] **Day 151** | [`system-design`](file:///Users/tushar/desktop/private/repos/system-design-from-scratch) | Phases 00–25: Back-of-the-envelope estimation: Latency numbers every programmer should know.  
  *Task:* Calculate QPS, storage, IOPS, and network egress for 50M DAU photo sharing service.  
  *Verify:* `pytest system-design-from-scratch/calculations/`.
- [ ] **Day 152** | [`system-design`](file:///Users/tushar/desktop/private/repos/system-design-from-scratch) | Phases 26–50: Sharding & Partitioning: Range-based, Hash-based, and Consistent Hashing rings.  
  *Task:* Implement Consistent Hash Ring with virtual nodes and rebalancing calculation.  
  *Verify:* `pytest system-design-from-scratch/simulations/test_simulations.py -k consistent_hash`.
- [ ] **Day 153** | [`system-design`](file:///Users/tushar/desktop/private/repos/system-design-from-scratch) | Phases 51–75: Distributed Consensus & Coordination: Leader election, heartbeat detection.  
  *Task:* Simulate leader election with network partition split-brain detection.  
  *Verify:* `pytest system-design-from-scratch/simulations/test_simulations.py -k leader_election`.
- [ ] **Day 154** | [`system-design`](file:///Users/tushar/desktop/private/repos/system-design-from-scratch) | Phases 76–100: Distributed Time & Ordering: Lamport Clocks, Vector Clocks, TrueTime.  
  *Task:* Implement Vector Clock conflict detection resolving concurrent writes.  
  *Verify:* `pytest system-design-from-scratch/simulations/test_simulations.py -k vector_clocks`.
- [ ] **Day 155** | [`system-design`](file:///Users/tushar/desktop/private/repos/system-design-from-scratch) | Capstones 01–03: Scalable URL Shortener, Event-Driven Orders, Real-Time Chat.  
  *Task:* Execute full capstone test suites validating end-to-end distributed flows.  
  *Verify:* `pytest system-design-from-scratch/projects/01-scalable-url-shortener/`.
- [ ] **Day 156** | [`system-design`](file:///Users/tushar/desktop/private/repos/system-design-from-scratch) | Capstones 04–07: Distributed Cache, Distributed Queue, Tiny KV Store (Quorum), Social Feed.  
  *Task:* Run quorum write/read ($R + W > N$) consistency simulation.  
  *Verify:* `pytest system-design-from-scratch/projects/06-tiny-distributed-kv-store/`.
- [ ] **Day 157** | [`system-design`](file:///Users/tushar/desktop/private/repos/system-design-from-scratch) | Broken Systems Marathon: Solve all 32 broken system labs in `system-design-from-scratch/`.  
  *Verify:* Run full test suite: **899 passed**.

### Week 22: Production SRE, OpenTelemetry & Platform Engineering
- [ ] **Day 158** | [`production-sre`](file:///Users/tushar/desktop/private/repos/production-sre-observability-platform-engineering-from-scratch) | Phases 00–30: Production foundations, Little's Law, OTel SDK, W3C traceparent propagation.  
  *Task:* Verify Project 01 (Telemetry Middleware) and Project 02 (Collector Pipeline).  
  *Verify:* `pytest production-sre-.../projects/project-01-instrument-backend-service/`.
- [ ] **Day 159** | [`production-sre`](file:///Users/tushar/desktop/private/repos/production-sre-observability-platform-engineering-from-scratch) | Phases 31–72: Prometheus TSDB, PromQL queries, Alertmanager routing, inhibition rules.  
  *Task:* Verify Project 03 (RED/USE Dashboards) and Project 05 (Alerting Engine).  
  *Verify:* `pytest production-sre-.../projects/project-05-production-alerting-engine/`.
- [ ] **Day 160** | [`production-sre`](file:///Users/tushar/desktop/private/repos/production-sre-observability-platform-engineering-from-scratch) | Phases 73–100: Multi-Window Multi-Burn-Rate SLO alerts, incident triage, and postmortems.  
  *Task:* Run Project 04 (SLO Platform Lite) and Project 06 (Incident Simulator).  
  *Verify:* `pytest production-sre-.../projects/project-04-slo-platform-lite/`.
- [ ] **Day 161** | [`production-sre`](file:///Users/tushar/desktop/private/repos/production-sre-observability-platform-engineering-from-scratch) | Phases 101–165: Capacity planning, Little's Law sizing, PRR linter, chaos engineering.  
  *Task:* Run Project 07 (Capacity Planner) and Project 08 (PRR Linter CLI).  
  *Verify:* `pytest production-sre-.../projects/project-07-capacity-planner/`.
- [ ] **Day 162** | [`production-sre`](file:///Users/tushar/desktop/private/repos/production-sre-observability-platform-engineering-from-scratch) | Phases 166–208: Platform Engineering: Service Bootstrapper, IDP `service.yaml`, Service Catalog.  
  *Task:* Run Project 09 (Bootstrapper), Project 10 (IDP), Project 11 (Catalog), Project 12 (Golden Path).  
  *Verify:* `pytest production-sre-.../projects/project-12-end-to-end-golden-path/`.
- [ ] **Day 163** | [`production-sre`](file:///Users/tushar/desktop/private/repos/production-sre-observability-platform-engineering-from-scratch) | Capstones 1–7: Resilient Service, SRE Challenge, Major Outage War Room review.  
  *Task:* Review postmortem templates in `production-sre-.../capstones/`.
- [ ] **Day 164** | [`production-sre`](file:///Users/tushar/desktop/private/repos/production-sre-observability-platform-engineering-from-scratch) | Broken Production Labs Marathon: Run all 42 broken labs.  
  *Verify:* Run `./.venv/bin/pytest` in `production-sre-...` (**109 passed**).

### Week 23: Modern AI Engineering & AI Systems Infrastructure
- [ ] **Day 165** | [`ai-engineering`](file:///Users/tushar/desktop/private/repos/ai-engineering-from-scratch) | Phases 00–05: Tensors, matrix multiplications, backpropagation, and neural network core.  
  *Task:* Implement autograd backward pass for linear layer from scratch in Python.  
  *Verify:* `pytest ai-engineering-from-scratch/tests/`.
- [ ] **Day 166** | [`ai-engineering`](file:///Users/tushar/desktop/private/repos/ai-engineering-from-scratch) | Phases 06–10: Attention mechanisms, scaled dot-product attention, Transformer decoder.  
  *Task:* Write multi-head attention forward pass calculating $Q \cdot K^T / \sqrt{d_k}$.
- [ ] **Day 167** | [`ai-engineering`](file:///Users/tushar/desktop/private/repos/ai-engineering-from-scratch) | Phases 11–16: Production RAG: Chunking, dense embeddings, vector retrieval, reranking.  
  *Task:* Build end-to-end RAG pipeline with reciprocal rank fusion.
- [ ] **Day 168** | [`ai-systems`](file:///Users/tushar/desktop/private/repos/ai-systems-from-scratch) | Parts 01–03: Computation graphs, IR passes, constant folding, Triton GPU kernels.  
  *Task:* Implement computation graph constant folding optimization pass.  
  *Verify:* `pytest ai-systems-from-scratch/compiler-labs/`.
- [ ] **Day 169** | [`ai-systems`](file:///Users/tushar/desktop/private/repos/ai-systems-from-scratch) | Parts 04–06: LLM Inference Optimization: KV Cache, continuous batching, prefix caching.  
  *Task:* Implement PagedAttention block allocation simulator tracking memory fragmentation.  
  *Verify:* `pytest ai-systems-from-scratch/inference/`.
- [ ] **Day 170** | [`ai-systems`](file:///Users/tushar/desktop/private/repos/ai-systems-from-scratch) | Parts 07–10: Quantization (INT8, FP4) & Speculative Decoding simulation.  
  *Task:* Run speculative decoding simulation measuring speedup vs draft model acceptance rate.  
  *Verify:* Run `ai-systems-from-scratch/inference/test_inference.py`.
- [ ] **Day 171** | [`ai-systems`](file:///Users/tushar/desktop/private/repos/ai-systems-from-scratch) | Projects & Capstones: Mini Compiler, Inference Scheduler, Evaluator Harness.  
  *Verify:* Run `./.venv/bin/pytest` in `ai-systems-from-scratch/` (**44 passed**).

### Week 24: Staff Engineering, Technical Strategy & Final Synthesis
- [ ] **Day 172** | [`staff-engineering`](file:///Users/tushar/desktop/private/repos/staff-engineering-and-product-mindset-from-scratch) | Phases 00–25: Staff archetypes (Tech Lead, Architect, Solver, Right Hand), leverage vs execution.  
  *Task:* Map your engineering leadership focus across the 4 archetypes.
- [ ] **Day 173** | [`staff-engineering`](file:///Users/tushar/desktop/private/repos/staff-engineering-and-product-mindset-from-scratch) | Phases 26–60: Writing transformative RFCs (Request for Comments) & Architecture Decision Records.  
  *Task:* Draft RFC 01: "Global Database Sharding & Shard Migration Strategy for 10x Scale".
- [ ] **Day 174** | [`staff-engineering`](file:///Users/tushar/desktop/private/repos/staff-engineering-and-product-mindset-from-scratch) | Phases 61–100: Technical Debt valuation: How to prioritize refactoring using financial framing.  
  *Task:* Build business case converting latency reduction into revenue retention metrics.
- [ ] **Day 175** | [`staff-engineering`](file:///Users/tushar/desktop/private/repos/staff-engineering-and-product-mindset-from-scratch) | Phases 101–140: Multi-team alignment, managing cross-functional friction, engineering strategy.  
  *Task:* Draft RFC 02: "Zero-Trust Service Mesh & mTLS Workload Identity Migration".
- [ ] **Day 176** | [`staff-engineering`](file:///Users/tushar/desktop/private/repos/staff-engineering-and-product-mindset-from-scratch) | Phases 141–180: Leading Major Outage War Rooms, blameless postmortems, action item enforcement.  
  *Task:* Write retrospective postmortem for complex cascading outage simulation.
- [ ] **Day 177** | [`staff-engineering`](file:///Users/tushar/desktop/private/repos/staff-engineering-and-product-mindset-from-scratch) | Phases 181–201: Setting 3-Year Technical Architecture Roadmaps.  
  *Task:* Draft RFC 03: "Next-Generation Event-Driven Streaming Platform Architecture".
- [ ] **Day 178** | Final Master Interview Simulation 1: Design a Global Payment Gateway with 99.999% SLA.
- [ ] **Day 179** | Final Master Interview Simulation 2: Design a Distributed Time-Series Database from scratch.
- [ ] **Day 180** | **GRAND MASTER SYNTHESIS**: Complete final portfolio audit, tag releases across monorepo, push all changes to GitHub!

---

## 📈 Daily Progress Tracker

Track your overall progress across the 6-month journey:

```text
[ ] Month 1: Machine Foundations & OS      (Days 001–030)  [0/30]
[ ] Month 2: Protocols & Craftsmanship     (Days 031–060)  [0/30]
[ ] Month 3: Backend & Storage Internals   (Days 061–090)  [0/30]
[ ] Month 4: Persistence, Cache & Streams  (Days 091–120)  [0/30]
[ ] Month 5: OLAP, Data & Cloud Platforms  (Days 121–150)  [0/30]
[ ] Month 6: Distributed Systems, SRE & AI (Days 151–180)  [0/30]

Total Mastery Progress: [░░░░░░░░░░░░░░░░░░░░] 0% (0/180 Days)
```
