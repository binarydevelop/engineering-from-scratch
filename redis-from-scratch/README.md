# redis-from-scratch

<p align="center">
  <b>Understand it. Build it. Measure it. Break it. Fix it. Scale it. Ship it.</b>
</p>

<p align="center">
  <a href="VERSIONS.md"><img src="https://img.shields.io/badge/redis-7.4.x%20%7C%208.x-red?style=flat-square" alt="Redis Version"></a>
  <a href="ROADMAP.md"><img src="https://img.shields.io/badge/phases-51%20phases-blue?style=flat-square" alt="51 Phases"></a>
  <a href="ROADMAP.md"><img src="https://img.shields.io/badge/lessons-51%20lessons-blue?style=flat-square" alt="51 Lessons"></a>
  <a href="LEARNING.md"><img src="https://img.shields.io/badge/philosophy-first--principles-darkgreen?style=flat-square" alt="Philosophy"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-lightgrey?style=flat-square" alt="License"></a>
</p>

```text
░░░▒▒▒░░░▒▒▒░░░▒▒▒░░░▒▒▒░░░▒▒▒░░░▒▒▒░░░▒▒▒░░░▒▒▒░░░▒▒▒░░░▒▒▒░░░▒▒▒░░░▒▒▒░░░▒▒▒░░░▒▒▒░░░▒▒▒
```

> **Most software engineers treat Redis as "a really fast dictionary in the cloud."**
>
> That intuition is acceptable on day one, but it collapses the moment a production incident occurs:
> - Why did a single `KEYS *` call freeze 50 microservices?
> - Where did your session tokens go when the server rebooted?
> - Why did memory explode to 2GB when storing 100MB of strings?
> - Why did a hot key saturate CPU while 49 cluster nodes sat idle?
>
> This curriculum replaces the black-box intuition with an uncompromising, mechanical systems mental model. You will not memorize Redis commands; you will build Redis mechanisms from scratch, benchmark raw TCP sockets, inject network partitions, overflow replication backlogs, and construct resilient distributed topologies.

---

## The Curriculum Progression

```text
Key / Value Store
       │
       ▼
Network TCP Server
       │
       ▼
RESP Wire Protocol
       │
       ▼
Internal Data Structures (SDS, Dict, Listpack, Skiplist)
       │
       ▼
Expiration & Active Sampling (serverCron)
       │
       ▼
Memory & Approximated Eviction (maxmemory, LRU, LFU)
       │
       ▼
Durability & Persistence (RDB Snapshots, AOF, fsync, COW Fork)
       │
       ▼
Caching Architectures (Cache-Aside, Invalidation, Stampede Mutex)
       │
       ▼
Messaging & Distributed Coordination (Pub/Sub vs Streams, Locks)
       │
       ▼
Benchmarking & Latency Diagnostics (SLOWLOG, Memory Profiling)
       │
       ▼
High Availability & Clustering (Replication, Sentinel, Hash Slots)
       │
       ▼
Production Capstones (Mini-Redis Server, Resilient Cluster Lab)
```

---

## 41 Systems Questions Answered by This Course

By completing this curriculum, you will be able to answer every one of these questions with technical rigor:

1. **Why does Redis exist?** Because RAM latency (~100ns) is 3 to 4 orders of magnitude faster than NVMe storage (~50µs) and disk block paging.
2. **Why is Redis fast?** Pure in-memory execution, non-blocking I/O multiplexing (`epoll`/`kqueue`), zero thread-synchronization locking on dataset operations, and compact data representations.
3. **What does "in-memory database" actually mean?** The primary live dataset resides at CPU-addressable memory pointers, not paged through an OS filesystem buffer cache.
4. **What happens when I run `SET key value`?** Packets travel over TCP, are framed via RESP, parsed in the query buffer, dispatched via `server.commands`, allocated via jemalloc, inserted into `server.db[0].dict`, updated in the LRU clock, and appended to persistence buffers.
5. **How does Redis communicate with clients?** Over persistent full-duplex TCP sockets using length-prefixed protocol frames.
6. **What is RESP?** The Redis Serialization Protocol: a human-readable, binary-safe, length-prefixed wire protocol.
7. **How does Redis represent different data types?** Using a 16-byte `redisObject` header pointing to specialized C data structures (SDS, listpack, dict, quicklist, skiplist, intset).
8. **How do strings, hashes, lists, sets, and sorted sets differ?** In access complexity ($O(1)$ vs $O(\log N)$ vs $O(N)$), memory layout, and operational semantics.
9. **When should each Redis data structure be used?** Matched specifically to access patterns (counters for Strings, domain entities for Hashes, sliding logs for Lists, uniqueness for Sets, ranking for Sorted Sets).
10. **How does expiration work?** Dual engine: passive lazy deletion on key lookup + active periodic sampling (20 keys, 10 times/sec) in `serverCron`.
11. **What happens when memory fills up?** If writes exceed `maxmemory`, Redis activates its configured eviction policy or returns an OOM error under `noeviction`.
12. **What are eviction policies?** Algorithmic rules (`allkeys-lru`, `volatile-lfu`, `volatile-ttl`, etc.) dictating which keys are sacrificed to reclaim RAM.
13. **What happens if Redis crashes?** Volatile DRAM is erased; state is restored upon reboot by loading the latest RDB snapshot and replaying the AOF log.
14. **What is RDB?** Point-in-time binary dataset snapshot created via background `fork()` utilizing OS Copy-on-Write (COW).
15. **What is AOF?** Append-Only File: a write-ahead command log replayed on boot to reconstruct exact dataset mutations.
16. **What durability guarantees does each persistence mode provide?** RDB loses data since the last snapshot (minutes); AOF `everysec` loses at most 1–2 seconds; AOF `always` guarantees sync-before-ack at high throughput cost.
17. **How does replication work?** Asynchronous streaming: primary applies mutations and forwards byte streams to read-only replicas via a circular backlog buffer.
18. **What happens when a replica falls behind?** If its offset is within `repl-backlog-size`, it executes a fast partial resync (`PSYNC`). If it falls off the ring, a full RDB snapshot transfer is forced.
19. **What is Sentinel solving?** Automated high availability: health monitoring, quorum consensus, automatic replica promotion, and client reconfiguration.
20. **How does Redis Cluster partition data?** Across exactly 16,384 logical Hash Slots using `CRC16(key) mod 16384`.
21. **What are hash slots?** Fixed virtual partitions that decouple keys from physical nodes, allowing online resharding without recalculating hashes.
22. **Why can multi-key operations become difficult in a cluster?** Commands touching multiple keys must reside in the exact same slot; cross-slot operations fail unless forced to the same node via Hash Tags `{...}`.
23. **What is pipelining?** Batching multiple client command writes into a single TCP socket flush without waiting for sequential replies.
24. **Why is pipelining faster?** It amortizes network Round Trip Time (RTT) and kernel system call context switches.
25. **What are transactions in Redis?** Sequentially queued command blocks (`MULTI`/`EXEC`) executed without interleaving from other clients.
26. **What does `WATCH` solve?** Optimistic Concurrency Control (OCC): aborts `EXEC` if any watched key was modified by another client during preparation.
27. **What does Lua scripting or Redis Functions solve?** Atomic execution of complex multi-step application logic directly on the engine core, eliminating network round-trip race conditions.
28. **What is Pub/Sub?** Fire-and-forget real-time message broadcasting to currently connected channel subscribers.
29. **Why is Pub/Sub not a durable message queue?** The server buffers no historical messages; if a subscriber is offline, messages are discarded permanently.
30. **What are Redis Streams?** Persistent, append-only event logs indexed by millisecond timestamps and sequence IDs.
31. **How do consumer groups work?** Partition stream messages among cooperating worker instances with persistent offset tracking and acknowledgment (`XACK`).
32. **How should Redis be used as a cache?** Via Cache-Aside with explicit TTLs, cache invalidation on mutation, and stampede defenses.
33. **What are cache-aside, write-through, and write-behind?** Three caching patterns balancing read latency, write latency, and data consistency.
34. **What is a cache stampede?** A thundering herd event where an intensely requested hot key expires, causing thousands of concurrent requests to hammer the database.
35. **What is a hot key?** A single key receiving a disproportionate fraction of queries, saturating the single thread or node holding that key.
36. **What is a distributed lock?** A synchronization mechanism providing mutually exclusive resource access across independent server nodes.
37. **Why can naive Redis locks be dangerous?** Unhandled process pauses, clock drift, and lack of unique release tokens cause workers to delete other workers' locks.
38. **What metrics should be monitored in production?** `connected_clients`, `instantaneous_ops_per_sec`, `used_memory_rss`, `mem_fragmentation_ratio`, `evicted_keys`, and replication lag.
39. **How do you diagnose high latency?** Using the 7-step debugging tree: `SLOWLOG`, `LATENCY DOCTOR`, client buffers, memory fragmentation, and persistence fork delays.
40. **How do you reason about memory usage?** Accounting for per-key `dictEntry` overhead (24B), `robj` headers (16B), allocator alignment padding, and fragmentation ratios.
41. **When should Redis NOT be used?** For cold archival data exceeding RAM budgets, multi-table complex relational queries, or workloads requiring strict distributed ACID transactions across shards.

---

## Repository Structure

```text
redis-from-scratch/
├── README.md               # Flagship curriculum guide
├── ROADMAP.md              # 51-phase roadmap with prerequisites & artifacts
├── LEARNING.md             # The 12-step engineering learning loop
├── LESSON_TEMPLATE.md      # Standardized pedagogical lesson schema
├── VERSIONS.md             # Pinned Redis 7.4.x / 8.x specifications & distinctions
├── CONTRIBUTING.md         # Contribution guidelines
├── Makefile                # Transparent laboratory automation (Make != Docker != Redis)
├── docker-compose.yml      # Multi-node topologies (Standalone, Replica, Postgres)
├── requirements.txt        # Minimal Python test dependencies
│
├── scripts/
│   ├── check-environment.sh    # Preflight dependency verification
│   ├── start-redis.sh          # Intelligent runner (Local or Docker)
│   ├── stop-redis.sh           # Graceful lab termination
│   ├── reset-lab.sh            # FLUSHALL and persistence cleaner
│   └── run-all-tests.py        # Automated test suite across all 51 phases
│
├── docs/
│   ├── glossary.md             # Systems & Redis terminology
│   ├── mental-models.md        # ASCII architectural diagrams & packet flows
│   ├── command-reference.md    # Complexity ($O(1), O(N)$) & danger matrix
│   └── troubleshooting.md      # 7-step latency diagnosis flowchart
│
├── phases/                     # 51 Complete Phases (Phases 00 to 50)
│   ├── 00-environment-and-redis-lab/
│   ├── 01-why-redis-exists/
│   ├── ...
│   └── 50-final-mental-model/
│       ├── docs/en.md              # Rigorous first-principles lesson
│       ├── code/*.py               # Runnable Python prototypes & clients
│       ├── experiments/*.sh        # Executable experiment verification scripts
│       └── outputs/*.md            # Evidence record templates
│
├── projects/                   # 4 Production-Grade End-to-End Applications
│   ├── 01-cached-api/              # REST API + Cache-Aside + Stampede Lock + SQLite
│   ├── 02-leaderboard/             # Real-time tournament ranking engine with ZSETs
│   ├── 03-rate-limiter/            # Fixed Window, Sliding Window Log & Token Bucket
│   └── 04-task-queue/              # Durable background workers with Streams & PEL
│
├── benchmarks/
│   └── run_benchmarks.py       # RAM vs Disk vs Redis, Pipelining speedup, Percentiles
│
└── outputs/
    └── evidence-template.md    # Canonical personal engineering lab notebook
```

---

## Quickstart: Your First Commands

### 1. Verify Prerequisites
Run the preflight environment check:
```bash
./scripts/check-environment.sh
```

### 2. Launch the Redis Laboratory
Start Redis (local daemon or Docker container):
```bash
./scripts/start-redis.sh
```

### 3. Run Benchmark Suite
Compare in-memory RAM access vs disk SQLite transactions vs Redis TCP round trips:
```bash
python3 benchmarks/run_benchmarks.py
```

### 4. Execute Phase 00 Experiment
Verify the client-server boundary:
```bash
./phases/00-environment-and-redis-lab/experiments/run_experiment.sh
```

### 5. Run Automated Test Suite
Verify that all 51 phases, unit tests, and Python algorithms pass:
```bash
python3 scripts/run-all-tests.py
```

---

## Relationship to System Design

This curriculum prepares you for large-scale distributed system design. As you progress, you will connect Redis mechanisms to fundamental architectural concepts:

| Systems Concept | Redis Mechanism | Explored In |
| :--- | :--- | :--- |
| **Latency Hierarchy** | DRAM vs NVMe flash storage | [Phase 01](phases/01-why-redis-exists/docs/en.md) |
| **Protocol Framing** | Length-prefixed binary-safe RESP frames | [Phase 04](phases/04-redis-protocol-resp/docs/en.md) |
| **Event Loops & I/O** | Single-threaded Reactor pattern (`ae.c`, `epoll`) | [Phase 05](phases/05-command-execution-mental-model/docs/en.md) |
| **Compact Encoding** | Listpack vs Doubly-Linked Hash Tables | [Phase 11](phases/11-redis-data-structure-internals/docs/en.md) |
| **Memory Reclamation** | Active probabilistic sampling vs LRU eviction | [Phases 12-14](phases/12-expiration-and-ttl/docs/en.md) |
| **Batching & Network RTT** | Socket pipelining | [Phase 15](phases/15-pipelining/docs/en.md) |
| **Optimistic Concurrency**| `WATCH` / `MULTI` / `EXEC` | [Phase 16](phases/16-transactions/docs/en.md) |
| **Write-Ahead Logging** | Append-Only File (AOF) & fsync barriers | [Phases 19-21](phases/20-append-only-file/docs/en.md) |
| **Cache Stampede** | Single-flight distributed mutex locking | [Phase 24](phases/24-cache-stampede/docs/en.md) |
| **Event Streaming** | Redis Streams consumer groups & PEL recovery | [Phase 28](phases/28-redis-streams/docs/en.md) |
| **High Availability** | Primary-Replica streaming & Sentinel quorum | [Phases 34-36](phases/36-sentinel/docs/en.md) |
| **Horizontal Sharding** | 16,384 virtual Hash Slots & `-MOVED` routing | [Phases 37-39](phases/38-redis-cluster/docs/en.md) |

---

## Scope Boundaries

To maintain rigor, this course focuses strictly on **Redis and in-memory architectures**:
* It is **NOT** a general relational SQL database course.
* It is **NOT** an Apache Kafka or RabbitMQ deep dive.
* It is **NOT** a Kubernetes operations training course.
* It introduces Docker and Linux kernel primitives only where necessary to explain Redis process isolation, networking, and storage.

---

> ### Final Standard
>
> Redis is no longer a black box.
>
> We started with a dictionary, turned it into a networked key-value server, added data structures, expiration, memory management, persistence, messaging, replication, failover, and partitioning, and then used those mechanisms to solve real system-design problems.
>
> Now when Redis appears inside a system architecture, we can reason about why it is there, what guarantees it provides, how it can fail, and whether it belongs there at all.
