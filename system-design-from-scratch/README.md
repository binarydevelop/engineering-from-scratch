# system-design-from-scratch

> **Understand it. Derive it. Build it. Measure it. Break it. Scale it. Recover it. Ship it.**

---

## 1. Core Philosophy

Too many engineers study system design as an exercise in memorizing famous architectures: drawing 20 boxes containing Kafka, Redis, CDN, microservices, and sharded databases before even understanding what problem they are solving.

This repository takes the opposite approach: **Zero Premature Complexity**.

Every system starts from the simplest possible baseline: **one process and one database on a single machine**. We measure where it breaks under pressure, reason through the fundamental limits of computation, memory, disk, and network, and introduce architectural mechanisms **only when physical or operational constraints force us to**.

```text
[ Ambiguous Requirement ]
         │
         ▼
[ Requirements & Scope ]
         │
         ▼
[ Back-of-the-Envelope Estimation ]
         │
         ▼
[ Single-Machine Baseline (1 App, 1 DB) ]
         │
         ▼
[ Measure & Apply Load Pressure ]
         │
         ▼
[ Identify Physical Bottleneck (CPU / Disk IOPS / Memory / Network RTT) ]
         │
         ▼
[ Derive Mechanism (Cache, Read Replicas, Sharding, Message Queue, Consensus) ]
         │
         ▼
[ Inject Failure & Test Resilience ]
         │
         ▼
[ State Tradeoffs Explicitly ]
```

---

## 2. The 7 Justification Questions

Before adding **any** component, layer, queue, cache, or external service to an architecture diagram, you must answer these seven questions:

1. **Why does this exist?** (What fundamental physical or logical bottleneck does it solve?)
2. **What problem appears without it?** (What breaks, saturates, or drops under load?)
3. **What does it cost?** (Financial cost, latency penalty, operational overhead, mental complexity.)
4. **What new failure mode does it introduce?** (Stale data, split-brain, thundering herd, cascading failure?)
5. **What assumption does it rely on?** (Clock synchronization, idempotent consumers, network partitions being rare?)
6. **How would I know it is failing?** (What metrics, alerts, logs, and SLIs expose its degradation?)
7. **What simpler alternative exists?** (Can we scale vertically, optimize indexes, batch queries, or do nothing?)

---

## 3. End-to-End Request Journey Under Scale

Tracing a request from the user's browser down to disk and back:

```text
User / Client Device
    │
    ▼ [DNS Resolution / Geo-DNS / Anycast BGP]
Global CDN Edge (Static assets, TLS termination, DDoS shield, Edge Caching)
    │
    ▼ [Internet Backbone / HTTP/2 or HTTP/3 QUIC / TLS 1.3]
Network Load Balancer (L4 TCP/UDP eBPF / Maglev / AWS NLB)
    │
    ▼ [Direct Server Return / Internal VPC Route]
Application Gateway / Reverse Proxy (L7 Envoy / NGINX: SSL, Path Routing, Rate Limiting, Auth)
    │
    ▼ [Private Network / Distributed Tracing Context / Trace ID]
Stateless Application Cluster (FastAPI / gRPC / Go / Rust Workers)
    │
    ├──► [Cache-Aside Layer (Redis / Memcached): In-Memory Key-Value, Sub-ms Read]
    │
    ├──► [Durable Message Broker (Kafka / RabbitMQ / Outbox Pattern): Async Decoupling]
    │
    ▼ [Connection Pool / Shard Routing Layer / Transaction Coordinator]
Primary Database Cluster (PostgreSQL / MySQL / Distributed SQL)
    │
    ├── Primary Node (ACID Transactions, WAL Write Ahead Log, Row Locks)
    │     │
    │     ├──► [Asynchronous Replication Stream] ──► Read Replicas (Read Scaling)
    │     │
    │     └──► [CDC / Debezium Connector] ──► Search Indexer (Elasticsearch / OpenSearch)
    │
    ▼
Storage Subsystem (NVMe SSD Page Cache, Disk Controller, Block Storage, Object Store S3)
```

---

## 4. The 10 Invariant Mental Models

1. **Little's Law ($L = \lambda W$)**: The average number of requests in a system ($L$) equals arrival rate ($\lambda$) multiplied by average latency ($W$). If latency doubles, concurrency doubles.
2. **Latency Numbers Every Programmer Should Know**: L1 cache (1 ns), RAM (100 ns), NVMe SSD read (10–50 $\mu$s), Datacenter RTT (500 $\mu$s), Cross-country RTT (50–100 ms).
3. **CAP / PACELC Theorem**: Under a Network Partition ($P$), choose Availability ($A$) or Consistency ($C$). Else ($E$), choose Latency ($L$) or Consistency ($C$).
4. **Amdahl's Law**: System speedup is strictly bounded by the serial (non-parallelizable) portion of the workload.
5. **Two Generals & Byzantine Faults**: In an asynchronous network with message loss, two processes cannot achieve 100% common knowledge without consensus rounds.
6. **Single Point of Failure (SPOF)**: Any component without redundant failover that halts the entire service if disrupted.
7. **Thundering Herd / Cache Stampede**: When a hot cache key expires, thousands of concurrent requests bypass the cache simultaneously, crashing the database.
8. **Backpressure & Queuing Theory**: Unbounded queues don't prevent outages; they convert instant rejection into unbounded latency and memory exhaustion.
9. **Split-Brain Anomaly**: When a partitioned cluster forms two independent majorities, both accept conflicting writes, permanently corrupting state.
10. **Read-Your-Own-Writes Consistency**: A user must always observe their own recent updates immediately, even when reading from lagging asynchronous replicas.

---

## 5. Curriculum Roadmap (201 Progressive Phases)

The 201 phases are structured into 20 progressive parts across the complete systems engineering journey:

| Part | Phase Range | Core Systems Domain | Focus & Learning Outcomes |
| :--- | :--- | :--- | :--- |
| **Part 01** | Phase 00 – 10 | **Foundations & Physical Constraints** | Latency hierarchy, Little's Law, single-node limits, Amdahl's Law, memory vs disk |
| **Part 02** | Phase 11 – 20 | **Estimation & Capacity Planning** | QPS calculations, storage modeling, network bandwidth, IOPS math, cost derivation |
| **Part 03** | Phase 21 – 30 | **Networking, Transport & Routing** | OSI model, TCP vs UDP, HTTP evolution (1.1, 2, 3), TLS handshake, DNS & Anycast |
| **Part 04** | Phase 31 – 40 | **Load Balancing & Ingress** | L4 vs L7, round-robin, least connections, consistent hashing, health checks, eBPF |
| **Part 05** | Phase 41 – 50 | **Caching Strategies & Memory Systems** | Cache-aside, read/write-through, eviction (LRU/LFU), stampedes, cache coherence |
| **Part 06** | Phase 51 – 60 | **Database Storage Engines & Indexing** | B-Trees vs LSM-Trees, WAL, indexing strategies, buffer pools, disk layout |
| **Part 07** | Phase 61 – 70 | **Transactions, Concurrency & Isolation** | ACID guarantees, isolation levels, MVCC, 2PL, optimistic concurrency control, deadlocks |
| **Part 08** | Phase 71 – 80 | **Scaling Databases: Replication & Sharding** | Primary-replica, synchronous vs asynchronous, shard keys, rebalancing, scatter-gather |
| **Part 09** | Phase 81 – 90 | **Asynchronous Systems & Message Queues** | Queues vs event streams, pub/sub, consumer groups, backpressure, dead letter queues |
| **Part 10** | Phase 91 – 100 | **Distributed Systems Theory & Consensus** | CAP & PACELC, FLP impossibility, 2PC, Paxos, Raft consensus, vector clocks |
| **Part 11** | Phase 101 – 110 | **Distributed State, Storage & Coordination**| Distributed transactions, Saga pattern, outbox pattern, ZooKeeper/etcd locks |
| **Part 12** | Phase 111 – 120 | **Search, Analytics & Stream Processing** | Inverted indexes, log compaction, real-time aggregation, Lambda vs Kappa |
| **Part 13** | Phase 121 – 130 | **Rate Limiting, Throttling & Protection** | Token bucket, leaky bucket, sliding window counter, DDoS mitigation, shedding |
| **Part 14** | Phase 131 – 140 | **Observability, Tracing & Chaos** | Distributed tracing, RED/USE metrics, structured logging, chaos engineering |
| **Part 15** | Phase 141 – 150 | **Reliability, Fault Tolerance & Recovery** | Circuit breakers, retry storms with jitter, bulkhead isolation, disaster recovery |
| **Part 16** | Phase 151 – 160 | **Security, Identity & Data Protection** | OAuth2, JWT architecture, zero trust, TLS termination, KMS encryption, PII masking |
| **Part 17** | Phase 161 – 170 | **Global Multi-Region Architecture** | Active-passive vs active-active, GeoDNS, data residency, replication conflict resolution |
| **Part 18** | Phase 171 – 180 | **Edge Computing & Content Delivery** | CDN architecture, edge compute, cache invalidation, byte-range streaming |
| **Part 19** | Phase 181 – 190 | **Advanced Specialized Architectures** | Real-time gaming, financial ledgers, time-series engines, high-frequency IoT |
| **Part 20** | Phase 191 – 200 | **Mastering System Design & Synthesis** | End-to-end multi-tier synthesis, interview mastery, tradeoff evaluation, production readiness |

*For complete details, review [ROADMAP.md](ROADMAP.md).*

---

## 6. Repository Components

### 22 Runnable System Simulators (`simulations/`)
Executable pure-Python algorithmic models with verified tests:
1. `01_load_balancer`: Round-robin, least connections, weighted round-robin.
2. `02_consistent_hashing`: Virtual node ring, minimal keys moved on node addition/removal.
3. `03_lru_cache`: Doubly linked list + hash map $O(1)$ cache.
4. `04_token_bucket`: Burst handling and smooth replenishment rate limiter.
5. `05_leaky_bucket`: Fixed leak rate buffer smoothing bursty traffic.
6. `06_sliding_window_counter`: Granular time-window rate limiter without edge burst anomalies.
7. `07_message_broker`: Topic partition routing and consumer offset management.
8. `08_raft_consensus`: Leader election, heartbeat timeouts, and log replication.
9. `09_lsm_tree`: MemTable, Write-Ahead Log (WAL), immutable SSTable flushes.
10. `10_b_tree`: Multi-way balanced search tree index simulator.
11. `11_circuit_breaker`: Closed, Open, Half-Open state transitions with failure counters.
12. `12_two_phase_commit`: Transaction coordinator and 2PC participant prepare/commit voting.
13. `13_saga_orchestrator`: Distributed transaction workflow with compensating rollbacks.
14. `14_distributed_lock`: Leased mutex with expiration and fencing tokens.
15. `15_bloom_filter`: Bit array with optimal $k$ hash functions and false-positive math.
16. `16_hyperloglog`: Cardinality estimation with register bucketing and harmonic mean.
17. `17_merkle_tree`: Cryptographic hash tree for anti-entropy and partition synchronization.
18. `18_vector_clocks`: Causality tracking in distributed concurrent event streams.
19. `19_database_sharder`: Range and hash partitioning router across distributed shards.
20. `20_event_sourcing`: Append-only event store and aggregate projection rebuilder.
21. `21_gossip_protocol`: Epidemic node membership, heartbeat dissemination, and failure detection.
22. `22_write_ahead_log`: Crash recovery via sequential append-only log replay.

### 32 Broken System Debugging Labs (`broken-systems/`)
Real-world pathological architectural failure modes with reproduction and verified solutions:
1. `01_thundering_herd_on_cache_miss`
2. `02_split_brain_two_node_cluster`
3. `03_retry_storm_exponential_amplification`
4. `04_unbounded_in_memory_queue`
5. `05_connection_pool_exhaustion`
6. `06_stale_read_after_write_replica`
7. `07_slow_query_blocking_event_loop`
8. `08_hot_partition_key_saturation`
9. `09_deadlock_in_concurrent_transfers`
10. `10_cascading_timeout_deadline_missing`
11. `11_dual_write_inconsistency_db_and_cache`
12. `12_message_ordering_loss_across_partitions`
13. `13_distributed_lock_without_fencing_token`
14. `14_n_plus_one_query_performance_collapse`
15. `15_cache_invalidation_race_condition`
16. `16_zookeeper_session_timeout_thrashing`
17. `17_kafka_consumer_rebalance_storm`
18. `18_bloom_filter_false_positive_explosion`
19. `19_dns_ttl_caching_preventing_failover`
20. `20_database_wal_disk_saturation`
21. `21_noisy_neighbor_starvation`
22. `22_out_of_order_event_delivery`
23. `23_phantom_read_in_read_committed_isolation`
24. `24_clock_skew_corrupting_event_ordering`
25. `25_circuit_breaker_half_open_flapping`
26. `26_saga_partial_failure_missing_compensation`
27. `27_rate_limiter_race_condition_under_concurrency`
28. `28_memory_leak_in_long_lived_connection_pool`
29. `29_tls_handshake_cpu_exhaustion`
30. `30_scatter_gather_tail_latency_explosion`
31. `31_leader_failover_data_loss_unreplicated_wal`
32. `32_idempotency_token_collision_and_reuse`

### 50 System Design Interview Problems (`interview-problems/`)
Tiered interview challenge problems with functional/non-functional requirements, back-of-the-envelope calculations, and architectural solutions:
- **Beginner (15 problems)**: URL Shortener, Pastebin, Key-Value Store, Rate Limiter, Notification Service, Web Crawler, Unique ID Generator, Task Scheduler, Poll Voting System, Hit Counter, Content Delivery Network, In-Memory Cache, Metric Logging Collector, File Metadata Registry, E-Commerce Cart.
- **Intermediate (20 problems)**: Twitter/X Timeline, WhatsApp/Chat Service, YouTube/Video Streaming, Instagram Newsfeed, Google Drive File Sync, Uber/Ride Sharing, E-Commerce Flash Sale, Airbnb Booking System, Payment Gateway Engine, Distributed Search Engine, Uber Eats Delivery Tracking, Ticketmaster Seat Reservation, Yelp Proximity Search, Distributed Message Queue, Web Analytics Pipeline, Live Comment Stream, Stock Exchange Matching Engine, Collaborative Document Editor, Cloud Storage Tiering, IoT Fleet Telemetry.
- **Advanced (15 problems)**: Global Distributed Database, Distributed Consensus Engine, Multi-Region Active-Active Cloud Platform, Real-Time Ad Bidding Exchange, Large-Scale Fraud Detection, Multi-Tenant Cloud Object Store, Global CDN with Edge Compute, Distributed Time-Series Engine, High-Throughput Financial Ledger, Global Package Delivery Optimizer, Real-Time Multiplayer Game Backend, Autonomous Vehicle Fleet Coordinator, Distributed Machine Learning Serving, Global Health Telemetry Ingestion, Video Conference Infrastructure.

### 105 Estimation Drills (`calculations/`)
Mastery exercises on QPS, peak load, storage growth, network bandwidth, RAM caching sizes, and disk IOPS with separated solutions in `calculations/solutions/`.

### 7 Production Capstone Projects (`projects/`)
1. `01_distributed_key_value_store`: Consistent hashing, quorum reads/writes, hints handoff.
2. `02_high_throughput_message_broker`: Segment-based write-ahead log, partitioned consumer groups.
3. `03_distributed_rate_limiter`: Multi-tier token bucket with Redis synchronization and fallback.
4. `04_scalable_url_shortener`: Base62 encoding, read-through caching, bloom filter dedup.
5. `05_realtime_chat_service`: WebSocket connection management, fan-out outbox, distributed pub/sub.
6. `06_event_driven_ecommerce`: Transactional outbox, order lifecycle Saga, idempotent payment worker.
7. `07_metrics_observability_pipeline`: Ingestion buffer, sliding window aggregator, downsampling storage.

### Architecture Evolution Cases (`architectures/`)
- `01_single_machine_to_multitier`
- `02_read_heavy_scaling_cache_and_replicas`
- `03_write_heavy_partitioning_sharding`
- `04_asynchronous_event_driven_decoupling`
- `05_global_multi_region_deployment`

### Chaos & Failure Injection Experiments (`experiments/`)
- `01_thundering_herd_collapse`
- `02_split_brain_network_partition`
- `03_retry_storm_and_circuit_breaker`
- `04_cascading_failure_deadline_propagation`
- `05_replication_lag_read_inconsistency`
- `06_noisy_neighbor_starvation`

---

## 7. Quickstart Guide

### Prerequisites
- Python 3.12+ (CPython)
- `uv` (recommended) or standard `python3 -m venv`
- GNU Make

### Installation & Environment Verification
```bash
# Clone the repository
git clone https://github.com/your-org/system-design-from-scratch.git
cd system-design-from-scratch

# Setup virtual environment and dependencies
make setup

# Run environment check
make env-check
```

### Running the Test Suite
```bash
# Run all tests across the entire repository (900+ tests)
make test

# Run specific modules
make test-phases         # All 201 curriculum phases
make test-simulations    # 22 runnable system simulators
make test-broken         # 32 broken system debugging labs
make test-problems       # 50 interview problems & solutions
make test-calculations   # 105 back-of-the-envelope exercises
make test-projects       # 7 capstone projects
make test-architectures  # Architecture evolution studies
make test-experiments   # Chaos failure experiments
```

### Executing a Simulator Directly
```bash
# Run the Consistent Hash Ring simulator
.venv/bin/python simulations/02_consistent_hashing/main.py

# Run the Raft Consensus simulator
.venv/bin/python simulations/08_raft_consensus/main.py

# Run the Rate Limiter simulator
.venv/bin/python simulations/04_token_bucket/main.py
```

### Reproducing and Fixing a Broken System Lab
```bash
cd broken-systems/01_thundering_herd_on_cache_miss
python reproduce.py      # Observe the database lock failure under stampede
python fix.py            # Verify singleflight mutex coalescing resolves the stampede
pytest test_reproduce.py # Run the automated assertions
```

---

## 8. Documentation Suite (`docs/`)

- [`design-framework.md`](docs/design-framework.md): The canonical 16-step system design framework.
- [`mental-models.md`](docs/mental-models.md): The 7 justification questions, Little's Law, latency table, and CAP/PACELC.
- [`estimation-guide.md`](docs/estimation-guide.md): Mathematical cheat sheet, unit conversions, and rules of thumb.
- [`tradeoff-map.md`](docs/tradeoff-map.md): Decision matrix comparing SQL vs NoSQL, sync vs async, push vs pull.
- [`failure-models.md`](docs/failure-models.md): Formal failure taxonomy (crash-stop, byzantine, partitions, gray failures).
- [`interview-framework.md`](docs/interview-framework.md): 45-minute interview pacing guide and evaluation rubric.
- [`glossary.md`](docs/glossary.md): Deep definitions of over 60 essential distributed systems concepts.

---

## 9. License

This repository is distributed under the terms of the **MIT License**. See [LICENSE](LICENSE) for details.
