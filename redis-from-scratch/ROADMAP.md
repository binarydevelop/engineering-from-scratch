# Curriculum Roadmap: 51 Phases to Redis Mastery

> **Motto:** Understand it. Build it. Measure it. Break it. Fix it. Scale it. Ship it.

This roadmap outlines the complete 51-phase progression from a single in-memory Python dictionary to distributed, partitioned, failover-tolerant production clusters and custom server engines.

---

## High-Level Curriculum Progression

```text
  FOUNDATIONS & PROTOCOL
  ├── Phase 00: Environment and Redis Lab
  ├── Phase 01: Why Redis Exists (RAM vs Disk Latencies)
  ├── Phase 02: Build a Tiny Key-Value Store
  ├── Phase 03: Make the Key-Value Store a Server (TCP Sockets)
  ├── Phase 04: Redis Protocol (RESP2 / RESP3 Deep Dive)
  └── Phase 05: Redis Command Execution Mental Model (Event Loop & ae.c)
        │
  DATA STRUCTURES & MEMORY INTERNALS
  ├── Phase 06: Strings (Counters, Blobs, Bitmaps, SDS)
  ├── Phase 07: Hashes (Objects, Listpack vs Hashtable)
  ├── Phase 08: Lists (Queues, Stacks, Quicklists)
  ├── Phase 09: Sets (Uniqueness, Intersections, Intsets)
  ├── Phase 10: Sorted Sets (Leaderboards, Skiplists)
  ├── Phase 11: Redis Data Structure Internals (robj & Encoding Shifts)
  ├── Phase 12: Expiration & TTL (Active vs Passive Deletion)
  ├── Phase 13: Memory & Eviction (maxmemory & Allocator Limits)
  └── Phase 14: LRU and LFU From Scratch (Approximations vs Doubly-Linked Lists)
        │
  CONCURRENCY, TRANSACTIONS & SCRIPTING
  ├── Phase 15: Pipelining (Amortizing Network RTT)
  ├── Phase 16: Transactions (MULTI, EXEC, WATCH & Optimistic Locking)
  └── Phase 17: Atomicity and Server-Side Logic (Lua & Redis Functions)
        │
  PERSISTENCE & DURABILITY
  ├── Phase 18: Persistence: Why Memory Is Not Enough
  ├── Phase 19: RDB Snapshots (fork(), Copy-on-Write)
  ├── Phase 20: Append-Only File (AOF & fsync Guarantees)
  └── Phase 21: AOF Rewrite and Persistence Tradeoffs
        │
  CACHING ARCHITECTURES & PATTERNS
  ├── Phase 22: Redis as a Cache (Cache-Aside vs Write-Through)
  ├── Phase 23: Cache Invalidation (Stale Reads & Consistency)
  ├── Phase 24: Cache Stampede (Thundering Herd & Mutex Mitigation)
  └── Phase 25: Hot Keys (Workload Skew & Local Buffering)
        │
  MESSAGING, STREAMING & COORDINATION
  ├── Phase 26: Pub/Sub (Ephemeral Fire-and-Forget)
  ├── Phase 27: Build an Append-Only Event Log
  ├── Phase 28: Redis Streams (Consumer Groups, PEL, XACK)
  ├── Phase 29: Rate Limiting (Fixed Window, Sliding Log, Token Bucket)
  └── Phase 30: Distributed Locks (SET NX PX, Redlock Analysis)
        │
  OPERATIONS, MEASUREMENT & DIAGNOSIS
  ├── Phase 31: Performance & Benchmarking (Measuring Under Load)
  ├── Phase 32: Latency Diagnosis (SLOWLOG, LATENCY DOCTOR)
  ├── Phase 33: Memory Analysis (Memory Footprint & Defragmentation)
        │
  DISTRIBUTED TOPOLOGIES: REPLICATION, FAILOVER & CLUSTERING
  ├── Phase 34: Replication From First Principles
  ├── Phase 35: Replication Failure Modes (Lag, Desync, Backlog Ring)
  ├── Phase 36: Redis Sentinel (Health Checks, Quorum, Failover)
  ├── Phase 37: Partitioning From First Principles (Hashing vs Slots)
  ├── Phase 38: Redis Cluster (16,384 Hash Slots & MOVED Redirects)
  ├── Phase 39: Cluster Failure and Resharding (Slot Migration)
  ├── Phase 40: Redis Security Basics (ACLs, Protected Mode, TLS)
  └── Phase 41: Observability (INFO, Metrics & Monitoring)
        │
  PRODUCTION PROJECTS & CAPSTONES
  ├── Phase 42: Real Application: Cached API with PostgreSQL Fallback
  ├── Phase 43: Real Application: Real-Time Leaderboard System
  ├── Phase 44: Real Application: Distributed Rate Limiting Engine
  ├── Phase 45: Real Application: Durable Background Worker Pipeline
  ├── Phase 46: Redis Anti-Patterns (10 Catastrophic Production Mistakes)
  ├── Phase 47: Capstone 1: Build Mini-Redis From Scratch in Python
  ├── Phase 48: Capstone 2: Production-Like Resilient Redis Laboratory
  ├── Phase 49: System Design With Redis (12 Architectural Scenarios)
  └── Phase 50: The Final Mental Model (Complete Command Journey)
```

---

## Detailed Phase Breakdown

| Phase | Title | Prerequisite | Primary Experiment | Shipped Artifact | Mastery Check |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **00** | Environment and Redis Lab | None | Run verification script, start local & container Redis, test TCP connection | `scripts/check-environment.sh` | Can explain client/server split and verify port 6379 connectivity without GUI tools. |
| **01** | Why Redis Exists | Phase 00 | Benchmark in-memory dict vs disk SQLite access over 10,000 queries | `benchmarks/ram_vs_disk.py` | Can quote RAM vs NVMe latencies and explain serialization overhead. |
| **02** | Build a Tiny Key-Value Store | Phase 01 | Implement CLI key-value store with SET, GET, DEL, EXISTS | `code/mini_kv.py` | Can identify 6 critical missing capabilities of a basic dictionary. |
| **03** | Make Key-Value Store a Server | Phase 02 | Add TCP socket server with custom text protocol; discover framing issues | `code/tcp_kv_server.py` | Explains why newline-delimited protocols break with arbitrary binary data. |
| **04** | Redis Protocol / RESP | Phase 03 | Build raw RESP2 parser; send raw TCP bytes to Redis via netcat / Python | `code/raw_resp_client.py` | Can decode `*3\r\n$3\r\nSET...` by hand on paper. |
| **05** | Command Execution Mental Model | Phase 04 | Trace command dispatch in `server.c`; inspect with MONITOR | `code/trace_command.py` | Can trace packet flow from kernel socket to dict insertion. |
| **06** | Strings | Phase 05 | Compare text, counters, JSON strings, and binary safe byte buffers | `code/string_experiments.py` | Explains SDS length tracking and atomic `INCR` behavior. |
| **07** | Hashes | Phase 06 | Benchmark single JSON string vs Redis Hash with field-level reads/writes | `code/hash_vs_json.py` | Knows when hash field access beats deserializing 1MB JSON blobs. |
| **08** | Lists | Phase 07 | Build Python deque; implement queue and recent-item ring buffer with LPUSH/RPOP | `code/list_queue.py` | Understands quicklist structure and why lists lack consumer group offsets. |
| **09** | Sets | Phase 08 | Implement set operations; compute mutual social followers with SINTER | `code/set_intersections.py` | Explains intset vs hash table internal encoding shifts. |
| **10** | Sorted Sets | Phase 09 | Build member->score leaderboard; test range queries and ranking | `code/leaderboard_engine.py` | Explains why skiplist enables $O(\log N)$ rank queries while hash table is $O(1)$ score lookup. |
| **11** | Data Structure Internals | Phase 10 | Inspect memory encodings as collections grow past listpack limits | `code/inspect_encodings.py` | Predicts exact byte threshold when `listpack` converts to `hashtable`. |
| **12** | Expiration and TTL | Phase 11 | Build TTL dictionary; test active vs passive expiration with 50,000 keys | `code/ttl_benchmark.py` | Explains how `serverCron` prevents unread expired keys from leaking RAM. |
| **13** | Memory and Eviction | Phase 12 | Configure small maxmemory; compare eviction policies under write bursts | `code/eviction_stress.py` | Explains the fundamental mechanical difference between expiration and eviction. |
| **14** | LRU and LFU From Scratch | Phase 13 | Build doubly linked list LRU and frequency LFU; compare with Redis sample | `code/cache_algorithms.py` | Proves why Redis approximates LRU with random sampling instead of linked lists. |
| **15** | Pipelining | Phase 14 | Benchmark 1,000 sequential commands vs 100-command pipeline batch | `code/pipeline_benchmark.py` | Quantifies network RTT savings and disproves that pipelining is transactional. |
| **16** | Transactions | Phase 15 | Demonstrate race conditions in balance transfer; fix using WATCH/MULTI/EXEC | `code/bank_transfer_race.py` | Explains why Redis transactions lack SQL rollback on runtime data errors. |
| **17** | Atomicity & Server Logic | Phase 16 | Implement atomic inventory check-and-decrement using Lua scripts | `code/atomic_inventory.py` | Explains why server-side scripts eliminate client-server round-trip races. |
| **18** | Persistence: Why Memory Fails | Phase 17 | Kill Redis process ungracefully; measure data loss without persistence | `code/unclean_kill.py` | Clarifies the cost of volatile storage. |
| **19** | RDB Snapshots | Phase 18 | Trigger `BGSAVE`; inspect `dump.rdb` binary header; reboot and restore | `code/rdb_inspector.py` | Explains Copy-on-Write (COW) memory amplification during fork. |
| **20** | Append-Only File | Phase 19 | Corrupt an AOF entry; test redis-check-aof repair tool; test fsync policies | `code/aof_durability.py` | Balances throughput vs durability across `always`, `everysec`, and `no`. |
| **21** | AOF Rewrite & Tradeoffs | Phase 20 | Run 100k increments; trigger `BGREWRITEAOF`; observe file compaction | `code/aof_rewrite_demo.py` | Knows when to run RDB+AOF dual persistence. |
| **22** | Redis as a Cache | Phase 21 | Build cache-aside pattern with simulated DB latency; record hit/miss rates | `code/cache_aside.py` | Measures database load reduction and cache hit ratio. |
| **23** | Cache Invalidation | Phase 22 | Reproduce stale read bugs when database is updated behind cache | `code/cache_stale_demo.py` | Evaluates TTL, explicit invalidation, and versioned keys. |
| **24** | Cache Stampede | Phase 23 | Simulate 200 concurrent clients on expired hot key; mitigate with mutex | `code/stampede_mitigation.py`| Demonstrates single-flight locking and probabilistic early expiration. |
| **25** | Hot Keys | Phase 24 | Create 95% skewed traffic to 1 key; observe CPU saturation and local cache | `code/hot_key_mitigation.py` | Reasons about client-side caching and key sharding. |
| **26** | Pub/Sub | Phase 25 | Disconnect subscriber, publish message, reconnect; observe message loss | `code/pubsub_demo.py` | Proves definitively why Pub/Sub is not a durable message queue. |
| **27** | Append-Only Event Log | Phase 26 | Build Python stream with event IDs and offsets; discover consumer group bugs | `code/simple_event_log.py` | Identifies coordination problems before touching Redis Streams. |
| **28** | Redis Streams | Phase 27 | Create worker group; kill worker mid-processing; inspect and claim PEL message| `code/stream_consumer_lab.py`| Recovers stuck messages using `XPENDING` and `XCLAIM`. |
| **29** | Rate Limiting | Phase 28 | Implement fixed window, sliding window log, and token bucket algorithms | `code/rate_limiters.py` | Compares memory overhead and burst characteristics across algorithms. |
| **30** | Distributed Locks | Phase 29 | Implement single-instance lock with `SET NX PX` and safe Lua release token | `code/distributed_lock.py` | Explains process pause risks and fencing tokens. |
| **31** | Performance & Benchmarking | Phase 30 | Run `redis-benchmark` across payload sizes; measure localhost bias | `code/benchmark_runner.py` | Explains why localhost microbenchmarks deceive production capacity planning. |
| **32** | Latency Diagnosis | Phase 31 | Inject artificial slow commands; diagnose using SLOWLOG and LATENCY DOCTOR | `code/latency_injector.py` | Executes the 7-step latency debugging tree. |
| **33** | Memory Analysis | Phase 32 | Compare memory footprints of 100k strings vs 100k hashes with `MEMORY USAGE` | `code/memory_audit.py` | Explains memory overhead per key and defragmentation. |
| **34** | Replication From First Principles| Phase 33 | Forward commands to replica socket; introduce network lag; observe desync | `code/toy_replication.py` | Explains asynchronous replication trade-offs. |
| **35** | Replication Failure Modes | Phase 34 | Disconnect replica, exceed replication backlog buffer, force full resync | `code/repl_backlog_overflow.py`| Explains the difference between PSYNC partial resync and full RDB dump sync. |
| **36** | Redis Sentinel | Phase 35 | Launch Primary + 2 Replicas + 3 Sentinels; kill Primary; observe failover | `code/sentinel_failover.py` | Explains quorum consensus, split-brain risks, and client redirection. |
| **37** | Partitioning From Scratch | Phase 36 | Implement naive modulo partitioning; add node; measure 75% key dislocation | `code/partition_scratch.py` | Contrasts consistent hashing with Redis Cluster's slot architecture. |
| **38** | Redis Cluster | Phase 37 | Compute CRC16 slots; handle `-MOVED` redirection errors in raw Python client | `code/cluster_slot_client.py` | Uses hash tags `{...}` to execute multi-key operations safely. |
| **39** | Cluster Failure & Resharding | Phase 38 | Move slots between nodes; observe `-ASK` redirection protocol | `code/reshard_demo.py` | Understands slot migration lifecycle and client failover. |
| **40** | Redis Security Basics | Phase 39 | Configure ACL users with granular keyspace and command restrictions | `code/acl_security.py` | Secures Redis against unauthorized access and dangerous commands (`KEYS`, `FLUSHALL`). |
| **41** | Observability | Phase 40 | Build Python metrics collector scraping connection, memory, and eviction stats | `code/metrics_exporter.py` | Identifies the top 8 operational metrics for production alerting. |
| **42** | Project: Cached API | Phase 41 | Full FastAPI application with cache-aside, DB fallback, and invalidation | `projects/01-cached-api/` | Measures 10x throughput increase and p99 latency reduction. |
| **43** | Project: Real-Time Leaderboard | Phase 42 | High-throughput gaming leaderboard with pagination and rank lookup | `projects/02-leaderboard/` | Manages concurrent score updates without database bottlenecks. |
| **44** | Project: Distributed Rate Limiter| Phase 43 | Token bucket rate limiting middleware protecting HTTP endpoints | `projects/03-rate-limiter/` | Accurately throttles bursts with zero race conditions. |
| **45** | Project: Background Worker System| Phase 44 | Reliable task queue with Redis Streams, retries, and dead-letter queue | `projects/04-task-queue/` | Guarantees at-least-once task execution during worker crashes. |
| **46** | Redis Anti-Patterns | Phase 45 | Code 10 anti-patterns (unbounded keys, giant JSON blobs, lock leaks) and fixes | `code/anti_patterns.py` | Audits real-world codebases for Redis architectural pitfalls. |
| **47** | Capstone 1: Build Mini-Redis | Phase 46 | Pure Python async server supporting RESP, SET, GET, DEL, INCR, TTL, SAVE | `code/mini_redis_server.py` | Connects official `redis-cli` directly to the custom Python server! |
| **48** | Capstone 2: Resilient Lab | Phase 47 | Complete Dockerized topology with primary, replica, sentinel, and load tests | `code/resilient_lab.py` | Verifies zero downtime during simulated node failures. |
| **49** | System Design With Redis | Phase 48 | Architectural analysis across 12 production scenarios with trade-offs | `docs/system_design_cases.md` | Chooses optimal Redis data structures and persistence policies for complex architectures. |
| **50** | The Final Mental Model | Phase 49 | Trace complete path of `SET user:42 Tushar` from terminal to kernel to disk | `docs/final_mental_model.md` | Explains Redis mechanical reality with zero abstraction leaks. |
