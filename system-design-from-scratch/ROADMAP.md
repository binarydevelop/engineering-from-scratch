# Curriculum Roadmap: System Design From Scratch

> **Understand it. Derive it. Build it. Measure it. Break it. Scale it. Recover it. Ship it.**

An exhaustive, 20-part curriculum spanning **201 phases (Phase 00 through Phase 200)**.
Every phase forces the learner to start from first principles, measure real constraints, and derive architectural additions under pressure.

---

## Curriculum Structure at a Glance

| Part | Title | Phase Range | Core Architectural Theme |
| :--- | :--- | :--- | :--- |
| **01** | Foundations of Systems & Single-Node Limits | 00–06 | Lab setup, single-machine baseline, bottlenecks, latency vs throughput, percentiles, vertical scaling |
| **02** | Scaling Compute & Traffic Routing | 07–11 | Horizontal scaling, load balancers from scratch, algorithms, stateless app tier, reverse proxies vs gateways |
| **03** | Data Modeling, Persistence, & IDs | 12–16 | Relational vs NoSQL choice framework, primary keys, distributed snowflake ID generation, index cost |
| **04** | Read Scaling, Replication, & Consistency | 17–24 | Primary-replica replication, replication lag, read-after-write, CAP theorem from scratch, PACELC, failover |
| **05** | Caching & Edge Acceleration | 25–31 | Cache-Aside, invalidation, LRU/LFU eviction, cache stampedes, hot-key mitigations, CDN edge caching |
| **06** | Asynchronous Processing & Queues | 32–39 | In-memory to durable queues, at-least-once delivery, idempotency keys, retries with backoff & jitter, DLQs |
| **07** | Event-Driven Systems & Streaming | 40–45 | Pub/Sub, append-only event logs, queue vs log, consumer lag calculations, backpressure signals |
| **08** | Data Partitioning & Sharding | 46–54 | Modulo partitioning, consistent hash ring with virtual nodes, hash slots, range sharding, cross-shard queries |
| **09** | Distributed Replication & Quorums | 55–58 | N/W/R quorums, leader-based vs leaderless replication, conflict resolution (LWW vs CRDTs) |
| **10** | Time, Clocks, & Consensus | 59–68 | Clock skew, Lamport clocks, vector clocks, leader election, Raft consensus mental model, fencing tokens |
| **11** | Distributed Transactions & Outbox | 69–74 | Two-phase commit (2PC) limitations, Saga orchestration vs choreography, Transactional Outbox, CDC |
| **12** | Search, Blobs, & Content Delivery | 75–79 | Search indexes as derived state (Elasticsearch), blob vs metadata separation, direct-to-object upload |
| **13** | Traffic Control & Resiliency | 80–87 | Rate limiting (Token Bucket, Sliding Window), load shedding, circuit breakers, bulkheads, deadline budgeting |
| **14** | High Availability & Disaster Recovery | 88–97 | Calculating nines, fault domains, SPOF elimination, Multi-AZ vs Multi-Region, RPO/RTO disaster recovery |
| **15** | Capacity Planning & Cost Engineering | 98–102 | Mathematical models for app instances, DB pools, queue growth, storage retention, and infrastructure cost |
| **16** | Security & Identity Boundaries | 103–106 | Threat modeling, session vs JWT token auth, RBAC authorization, API gateway security boundaries |
| **17** | Observability & Failure Injection | 107–119 | RED metrics, distributed tracing, correlation IDs, heartbeats, chaos testing, fanout tail latency amplification |
| **18** | Microservices, Domain Boundaries, & Pipelines| 120–130 | Monolith vs microservice criteria, database per service, API composition, CQRS, event sourcing, batch vs stream |
| **19** | Foundational Distributed Subsystems | 131–149 | Schedulers, presence systems, leaderboards, news feed fanout, celebrity problems, geospatial geohashes |
| **20** | Real-World Systems & Interview Mastery | 150–200 | URL shortener, Chat, Feed, Video streaming, Ride-sharing, Ticket booking, Payment ledger, 7 Capstones, Final Review |

---

## Detailed Phase Syllabus (Phases 00 to 200)

### Part 01: Foundations of Systems & Single-Node Limits
- **Phase 00: System Design Laboratory** — Environment setup, sample API, SQLite/Postgres, Redis, metrics harness.
- **Phase 01: What Is System Design?** — Distinguishing code design, low-level design, backend architecture, and system design.
- **Phase 02: Start With One Machine** — The default baseline: one application and one database. Measuring baseline capacity.
- **Phase 03: Identify Bottlenecks** — Generating synthetic load to isolate the first point of failure (CPU, Memory, Disk, Connections).
- **Phase 04: Latency vs Throughput** — Understanding the inverse relationship; batching experiments and tradeoffs.
- **Phase 05: Percentiles** — Why averages lie. Measuring p50, p95, and p99 long-tail distributions.
- **Phase 06: Vertical Scaling** — Scaling CPU and RAM. Advantages, cost curves, and physical single-node hardware limits.

### Part 02: Scaling Compute & Traffic Routing
- **Phase 07: Horizontal Scaling** — Running multiple application processes; client dispatch problems.
- **Phase 08: Load Balancers From First Principles** — Building a reverse proxy dispatching across backend instances with health checks.
- **Phase 09: Load Balancing Algorithms** — Round-robin, random, least connections, and IP hashing under skewed workloads.
- **Phase 10: Stateless Services** — In-memory session breakdown; deriving stateless application tiers and centralized sessions.
- **Phase 11: Reverse Proxy and Gateway Concepts** — Distinguishing reverse proxies, L4/L7 load balancers, and API gateways.

### Part 03: Data Modeling, Persistence, & IDs
- **Phase 12: Data Modeling for System Design** — Identifying entities, access patterns, read/write ratios, and normalization.
- **Phase 13: Database Choice Framework** — Relational vs Key-Value vs Document vs Wide-Column vs Search Index.
- **Phase 14: Primary Keys** — Auto-increment vs UUIDv4 vs ULID vs natural keys. Locality, B-Tree fragmentation, predictability.
- **Phase 15: Distributed ID Generation** — Snowflake algorithm, timestamp ordering, worker node IDs, sequence counters.
- **Phase 16: Database Indexes in System Design** — B-Tree and Hash indexes; query performance vs write amplification.

### Part 04: Read Scaling, Replication, & Consistency
- **Phase 17: Read Scaling** — When single-node database reads saturate. Read replicas vs caching vs denormalization.
- **Phase 18: Replication From First Principles** — Primary-replica state copying; asynchronous vs synchronous replication.
- **Phase 19: Replication Lag** — Network propagation delay; observing and measuring stale reads on replicas.
- **Phase 20: Read-After-Write** — Mitigating read-your-own-writes inconsistencies using session routing and primary fallbacks.
- **Phase 21: Consistency Models** — Linearizable, sequential, read-your-writes, monotonic reads, and eventual consistency.
- **Phase 22: CAP From First Principles** — Simulating network partitions; proving why availability and consistency trade off.
- **Phase 23: PACELC Intuition** — Evaluating normal operating latency vs consistency alongside partition behavior.
- **Phase 24: Database Failover** — Primary node death; heartbeat detection, leader promotion, and client routing updates.

### Part 05: Caching & Edge Acceleration
- **Phase 25: Caching From First Principles** — Measuring read latency gains; defining what data can tolerate staleness.
- **Phase 26: Cache-Aside** — Implementing lazy loading cache patterns; tracking hit ratios and database offload.
- **Phase 27: Cache Invalidation** — TTL expiration vs write-through vs explicit invalidation; cache consistency challenges.
- **Phase 28: Cache Eviction** — LRU, LFU, and FIFO eviction algorithms under memory constraints.
- **Phase 29: Cache Stampede** — Hot key expiration; simulating thundering herd crashes and implementing mutex locks.
- **Phase 30: Hot Keys** — 90% traffic targeting a single key; local in-memory caching and key-splitting mitigations.
- **Phase 31: CDN From First Principles** — Edge caching static and media assets; point of presence (PoP) routing.

### Part 06: Asynchronous Processing & Queues
- **Phase 32: Async Processing** — Long-running synchronous HTTP requests; decoupling work from the request-response loop.
- **Phase 33: Queue From First Principles** — Producer-consumer queue models; durable persistence vs process crashes.
- **Phase 34: Queue Semantics** — Message leasing, visibility timeouts, acknowledgement (ACK), and automatic re-queuing.
- **Phase 35: At-Least-Once Processing** — Crash before ACK; observing duplicate message deliveries.
- **Phase 36: Idempotency** — Idempotency keys, atomic deduplication stores, and preventing duplicate side-effects.
- **Phase 37: Retry** — Distinguishing transient network faults from permanent business logic errors.
- **Phase 38: Backoff and Jitter** — Simulating retry storms; exponential backoff with full jitter to smooth recovery.
- **Phase 39: Dead-Letter Queue** — Isolating poison pill messages into DLQs for manual inspection and replay.

### Part 07: Event-Driven Systems & Streaming
- **Phase 40: Event-Driven Architecture** — Commands vs Events vs Event Streams; choreography vs loose coupling.
- **Phase 41: Pub/Sub** — 1-to-N fanout; multiple independent consumers reacting to domain events.
- **Phase 42: Event Log** — Append-only immutable commit logs; partitioned ordering and consumer offset tracking.
- **Phase 43: Queue vs Log** — Task distribution queues (RabbitMQ/SQS) vs replayable event streams (Kafka).
- **Phase 44: Consumer Lag** — Calculating backlog growth, processing deficits, and worker scaling catch-up time.
- **Phase 45: Backpressure** — Arrival rate exceeding service rate; shedding load, buffering, and upstream throttling.

### Part 08: Data Partitioning & Sharding
- **Phase 46: Partitioning Data** — Single-node storage and write limits; hash-based partitioning ($hash(key) \% N$).
- **Phase 47: Partitioning Problems** — Adding node $N+1$; observing catastrophic key remapping and cache flushing.
- **Phase 48: Consistent Hashing** — Implementing consistent hash ring with virtual nodes; remapping only $K/N$ keys.
- **Phase 49: Hash Slots** — Pre-allocated slot architectures (Redis Cluster model); deterministic cluster rebalancing.
- **Phase 50: Range Partitioning** — Partitioning by key ranges or timestamps; range scan benefits vs write hotspots.
- **Phase 51: Shard Key Selection** — Cardinality, write distribution, query locality, and hot-key risks.
- **Phase 52: Cross-Shard Queries** — Fan-out query amplification across $N$ shards; distributed scatter-gather costs.
- **Phase 53: Rebalancing** — Moving partitions online; data migration throughput, locking, and dual-routing.
- **Phase 54: Replication + Partitioning** — Combining sharded partitions with primary-replica fault tolerance.

### Part 09: Distributed Replication & Quorums
- **Phase 55: Quorums** — Configurable consistency ($N, W, R$); strict quorum overlap ($W + R > N$) vs sloppy quorums.
- **Phase 56: Leader-Based Replication** — Single leader coordination; write bottlenecks and failover complexity.
- **Phase 57: Leaderless Replication** — Dynamo-style multi-node writes; hinted handoff and read repair.
- **Phase 58: Conflict Resolution** — Concurrent updates; Last-Write-Wins (LWW) data loss vs CRDTs and application merges.

### Part 10: Time, Clocks, & Consensus
- **Phase 59: Time in Distributed Systems** — Physical clock drift, NTP synchronization limits, and why wall clocks lie.
- **Phase 60: Logical Clocks** — Lamport timestamps establishing causal event ordering without physical clocks.
- **Phase 61: Vector Clocks Concept** — Detecting concurrent conflicting writes across multi-master nodes.
- **Phase 62: Coordination Problem** — Electing leaders, assigning locks, and partition owners in distributed clusters.
- **Phase 63: Leader Election** — Heartbeat leasing and bully election simulators.
- **Phase 64: Consensus Problem** — Reaching agreement among untrusted network nodes in the presence of failures.
- **Phase 65: Raft Mental Model** — Terms, leader heartbeats, log replication, and majority commit rules.
- **Phase 66: Consensus vs Replication** — Copying state vs agreeing on authoritative ordered commit logs.
- **Phase 67: Distributed Locks** — Redis/ZooKeeper locks; lease timeouts, network pauses, and false releases.
- **Phase 68: Fencing Tokens** — Monotonically increasing tokens preventing stale lock holders from corrupting storage.

### Part 11: Distributed Transactions & Outbox
- **Phase 69: Transactions Across Services** — The dual-write defect: database commit succeeds, message broker fails.
- **Phase 70: Two-Phase Commit Concept** — Prepare and Commit phases; blocking coordinator hazards and availability loss.
- **Phase 71: Saga Pattern** — Choreographed and orchestrated compensating transactions for distributed workflows.
- **Phase 72: Orchestration vs Choreography** — Centralized workflow coordinators vs decentralized event reactions.
- **Phase 73: Transactional Outbox** — Writing state and events into the same atomic DB transaction; outbox pollers.
- **Phase 74: Change Data Capture** — Reading database WAL transaction logs directly into event streams.

### Part 12: Search, Blobs, & Content Delivery
- **Phase 75: Search Systems** — Inverted indexes, tokenization, and BM25 relevance scoring.
- **Phase 76: Search Index as Derived State** — Keeping Elasticsearch synchronized with primary relational DBs via CDC.
- **Phase 77: Object Storage** — Storing unstructured binary blobs; immutable key-value architecture vs block storage.
- **Phase 78: Metadata vs Blob Storage** — Storing file metadata in relational DB and file bytes in object storage.
- **Phase 79: Content Delivery** — CDN origin shielding, cache headers, signed URLs, and regional edge caches.

### Part 13: Traffic Control & Resiliency
- **Phase 80: Rate Limiting** — Fixed Window, Sliding Window Log, Sliding Window Counter, and Token Bucket algorithms.
- **Phase 81: Distributed Rate Limiting** — Redis-backed token buckets; race conditions and Lua script atomicity.
- **Phase 82: Load Shedding** — Detecting server overload; gracefully rejecting low-priority requests with 429/503.
- **Phase 83: Circuit Breakers** — CLOSED, OPEN, and HALF_OPEN states preventing cascade crashes into slow dependencies.
- **Phase 84: Bulkheads** — Isolating thread pools and connection pools between separate service dependencies.
- **Phase 85: Timeout Budgets** — End-to-end request deadlines; allocating and propagating downstream timeout budgets.
- **Phase 86: Retry Amplification** — Multi-tier retries; calculating exponential request explosions during outages.
- **Phase 87: Graceful Degradation** — Designing degraded fallback experiences (e.g. omitting personalized recommendations).

### Part 14: High Availability & Disaster Recovery
- **Phase 88: Availability** — Calculating availability percentage; annual downtime formulas for 99.9%, 99.99%, and 99.999%.
- **Phase 89: Reliability vs Availability** — Distinguishing whether a system is available vs whether its responses are correct.
- **Phase 90: Fault Domains** — Process, physical host, rack, Availability Zone (AZ), and geographic region boundaries.
- **Phase 91: Redundancy** — Active-passive vs active-active redundancy; why redundancy alone does not equal availability.
- **Phase 92: Single Points of Failure** — Auditing architecture diagrams to detect hidden unmanaged single points of failure.
- **Phase 93: Multi-AZ Design** — Synchronous cross-AZ replication; balancing low latency with power/datacenter isolation.
- **Phase 94: Multi-Region Motivations** — Latency, regulatory sovereignty, and disaster recovery justifications.
- **Phase 95: Multi-Region Complexity** — Asynchronous cross-region replication, conflict resolution, and split-brain risks.
- **Phase 96: Disaster Recovery** — Recovery Point Objective (RPO) and Recovery Time Objective (RTO) business metrics.
- **Phase 97: Backups** — Why replication does not equal backup; surviving ransomware, human error, and database drops.

### Part 15: Capacity Planning & Cost Engineering
- **Phase 98: Capacity Planning** — Deriving required CPU cores, RAM, and network bandwidth from traffic projections.
- **Phase 99: Queue Capacity** — Calculating buffer sizing and catch-up velocity during consumer downtime.
- **Phase 100: Connection Capacity** — Calculating socket file descriptors, epoll limits, and database connection pool sizes.
- **Phase 101: Storage Growth** — Projecting database and object store disk growth over 1, 3, and 5-year horizons.
- **Phase 102: Cost as Architecture Constraint** — Calculating the financial bills of compute, RAM, storage, and egress bandwidth.

### Part 16: Security & Identity Boundaries
- **Phase 103: Security in System Design** — Defense-in-depth, zero-trust network boundaries, and principle of least privilege.
- **Phase 104: Authentication Architecture** — Centralized sessions vs stateless JWT tokens vs OAuth2/OIDC identity providers.
- **Phase 105: Authorization Architecture** — Role-Based Access Control (RBAC) vs Attribute-Based Access Control (ABAC).
- **Phase 106: API Gateway Security Boundary** — Perimeter authentication, rate limiting, and WAF protection.

### Part 17: Observability & Failure Injection
- **Phase 107: Observability From First Principles** — Why telemetry is required; distinguishing metrics, logs, and traces.
- **Phase 108: Metrics** — Counter, Gauge, and Histogram metrics; calculating rates and percentiles.
- **Phase 109: Distributed Tracing** — W3C TraceContext; span propagation across microservice RPC calls.
- **Phase 110: Correlation IDs** — Passing request identifiers across HTTP headers, message queues, and worker logs.
- **Phase 111: SLI / SLO Concepts** — Defining Service Level Indicators and Service Level Objectives; error budgets.
- **Phase 112: Failure Detection** — Heartbeats, leases, and the impossibility of perfect failure detection in async networks.
- **Phase 113: Health Checks** — Shallow liveness (`/livez`) vs deep readiness (`/readyz`) dependency checking.
- **Phase 114: Heartbeats** — Lease timeouts and heartbeat intervals under transient network jitter.
- **Phase 115: Chaos / Failure Injection** — Introducing synthetic packet loss, connection drops, and CPU stalls.
- **Phase 116: Dependency Graphs** — Mapping upstream and downstream call graphs to identify circular dependency risks.
- **Phase 117: Critical Path** — Tracing synchronous dependencies on user-facing paths to minimize latency.
- **Phase 118: Fan-Out** — Querying $N$ distributed shards in parallel; observing throughput gains and connection costs.
- **Phase 119: Tail Latency Amplification** — Why 100 parallel requests make p99 latency dictate 63% of user requests.

### Part 18: Microservices, Domain Boundaries, & Pipelines
- **Phase 120: Monolith vs Microservices** — When to split: team scaling, independent deployments, and failure isolation.
- **Phase 121: Service Boundaries** — Bounded contexts, business capabilities, and avoiding noun-based microservice sprawl.
- **Phase 122: Shared Database Problem** — Microservices accessing the same DB tables; schema coupling and lock contention.
- **Phase 123: Database Per Service** — Data encapsulation; trading local foreign keys for distributed consistency.
- **Phase 124: Sync vs Async Service Communication** — REST/gRPC RPC calls vs asynchronous message queue decoupling.
- **Phase 125: API Composition** — Aggregating data across multiple microservices; API Gateway vs BFF pattern.
- **Phase 126: CQRS** — Command Query Responsibility Segregation; separating write-optimized and read-optimized models.
- **Phase 127: Event Sourcing** — Storing domain state as an immutable sequence of events rather than current state snapshots.
- **Phase 128: Materialized Views** — Transforming append-only event streams into optimized read-side database views.
- **Phase 129: Data Pipelines** — Extracting operational transactional data into data lakes and analytical warehouses.
- **Phase 130: Batch vs Stream Processing** — Periodic high-throughput batch processing vs low-latency streaming pipelines.

### Part 19: Foundational Distributed Subsystems
- **Phase 131: Scheduler Systems** — Distributed cron and task execution; lease stealing, timers, and missed execution recovery.
- **Phase 132: Notification System Fundamentals** — Multi-channel dispatch (Email, SMS, Push) with priority tiers.
- **Phase 133: Presence System** — Tracking online/offline user status via heartbeat leases and ephemeral Redis keys.
- **Phase 134: Leaderboard System** — Real-time game score ranking using Redis Sorted Sets (`ZADD`, `ZRANGE`).
- **Phase 135: Feed Generation** — Fanout-on-write (push) vs Fanout-on-read (pull) models for activity feeds.
- **Phase 136: Hot Celebrity Problem** — Users with 100M followers breaking fanout-on-write; hybrid feed architecture.
- **Phase 137: Geospatial Systems** — Geohash and Quadtree spatial partitioning for ride-matching and nearby queries.
- **Phase 138: Time-Series Systems** — High-throughput timestamped ingestion; time-partitioned tables and downsampling.
- **Phase 139: Logging System** — Distributed log aggregation pipeline (Fluentd/Kafka/OpenSearch) under burst load.
- **Phase 140: Metrics System** — High-cardinality time-series metric storage and downsampled rollups.
- **Phase 141: Distributed Cache System** — Consistent-hash partitioned cache clusters with primary-replica failover.
- **Phase 142: Blob Storage System** — Chunked distributed file storage, chunk manifests, and Reed-Solomon erasure coding.
- **Phase 143: File Upload Service** — Pre-signed S3 URLs, multipart uploads, and asynchronous background transcode queues.
- **Phase 144: API Rate Limiter Design** — Distributed rate-limiting service using Redis token buckets and local memory caches.
- **Phase 145: Distributed Lock Service** — Fencing-token lock manager with lease expiration and split-brain defenses.
- **Phase 146: Configuration Service** — Dynamic runtime configuration distribution (Consul/etcd model) with watch notifications.
- **Phase 147: Service Discovery** — Client-side vs server-side service registries with automated health deregistration.
- **Phase 148: Feature Flag System** — Low-latency targeting evaluation via local in-memory rule caches and CDN distribution.
- **Phase 149: Webhook Delivery System** — Outbound webhook dispatch with exponential retries, HMAC signatures, and DLQs.

### Part 20: Real-World Systems, Capstones, & Interview Mastery
- **Phase 150: URL Shortener** — Complete design: Base62 encoding, 100M users, cache-aside read path, click counters.
- **Phase 151: Pastebin** — Text blob storage, TTL expiration, pre-signed upload URLs, and rate limiting.
- **Phase 152: TinyURL at Large Scale** — Evolving the URL shortener to global multi-region scale with 10B links.
- **Phase 153: Chat System** — 1-to-1 real-time messaging, WebSockets, message sequencing, and offline delivery queues.
- **Phase 154: Group Chat** — Group membership, message fanout, read receipts, and room state management.
- **Phase 155: High-Volume Notification Platform** — Multi-provider failover, rate throttling, and delivery templates.
- **Phase 156: News Feed** — Aggregating posts from followed users, ranking algorithms, and hybrid feed caching.
- **Phase 157: Twitter/X-Like Timeline** — Timeline generation, handling celebrity accounts, and real-time tweet indexing.
- **Phase 158: Instagram-Like Feed** — Image/video media metadata, CDN edge caching, and feed hydration.
- **Phase 159: YouTube-Like Video Platform** — Video ingestion, chunking, adaptive bitrate transcoding (HLS/DASH), and CDN.
- **Phase 160: Netflix-Like Streaming** — Video manifest generation, client telemetry, and multi-CDN steering.
- **Phase 161: Dropbox/Drive-Like Storage** — Block-level chunking, deduplication, synchronization protocol, and metadata DB.
- **Phase 162: Search Autocomplete** — Prefix trie indexes, query frequency ranking, and client-side prefix caching.
- **Phase 163: Web Search Engine Overview** — Web crawler, inverted index builder, PageRank scoring, and query serving.
- **Phase 164: Ride-Sharing System** — Real-time driver location updates, Geohash spatial index, matching algorithm, trip state.
- **Phase 165: Food Delivery** — Multi-actor workflow (Customer, Restaurant, Courier), order lifecycle, and delivery tracking.
- **Phase 166: Ticket Booking** — High-concurrency seat reservation, temporary holds, and double-booking prevention.
- **Phase 167: Hotel Booking** — Date-range inventory indexing, optimistic concurrency, and overbooking tolerances.
- **Phase 168: E-Commerce Platform** — Catalog search, cart checkout, inventory reservation, and payment processing.
- **Phase 169: Payment System** — Double-entry bookkeeping, idempotency keys, payment gateway state machine.
- **Phase 170: Digital Wallet / Ledger** — Immutable audit journal, derived account balances, and concurrency locks.
- **Phase 171: Banking Transfer** — ACID transactions, inter-bank messaging (ISO 20022), and reconciliation loops.
- **Phase 172: Stock Exchange Matching Concept** — Central limit order book (CLOB), price-time priority, and low-latency queues.
- **Phase 173: Ad Click Aggregation** — High-throughput event ingestion, deduplication, and windowed stream aggregation.
- **Phase 174: Analytics Pipeline** — Real-time event streaming into columnar storage (ClickHouse/Parquet) for OLAP queries.
- **Phase 175: Distributed Job Scheduler** — Distributed cron execution, distributed task queue, worker heartbeats, and leasing.
- **Phase 176: Web Crawler** — URL frontier, politeness delays, robot.txt parser, and document fingerprint deduplication.
- **Phase 177: Email Service** — SMTP transmission queue, provider quota tracking, bounce handling, and spam scoring.
- **Phase 178: API Gateway** — Gateway routing, JWT validation, rate limiting, and circuit breaking at the perimeter.
- **Phase 179: Distributed Key-Value Store** — Partitioned hash ring, quorum replication, and hinted handoff prototype.
- **Phase 180: Design Review Discipline** — Comprehensive 12-point architectural audit checklist.
- **Phase 181: Architecture Evolution Challenges** — Incrementally evolving a system under 10x read, 10x write, and failover pressure.
- **Phase 182: Broken Architecture Challenges** — Diagnosing and fixing flawed distributed diagrams.
- **Phase 183: Tradeoff Challenges** — Real-world scenarios forcing choices between consistency, latency, durability, and cost.
- **Phase 184: Architecture Comparison** — Designing a system for 100 QPS vs 100,000 QPS and explaining complexity differences.
- **Phase 185: Interview Framework** — Mastering the 45-minute collaborative system design interview structure.
- **Phase 186: Interview Simulation I** — Mock interview: Design a Global URL Shortener.
- **Phase 187: Interview Simulation II** — Mock interview with changing requirements: Adapting to Global Multi-Region Traffic.
- **Phase 188: Interview Simulation III** — Mock interview with strict consistency: Flash-Sale Ticket Reservation.
- **Phase 189: Interview Simulation IV** — Mock interview with 10x traffic surge: Scaling a Real-Time Social Feed.
- **Phase 190: Interview Simulation V** — Mock interview with budget constraints: Cost-Optimized Analytics Ingestion.
- **Phase 191: Capstone 1: Scalable URL Shortener** — Complete runnable implementation from single process to multi-node cache.
- **Phase 192: Capstone 2: Event-Driven Order Platform** — Transactional Outbox, order processing, and worker queues.
- **Phase 193: Capstone 3: Real-Time Chat** — WebSocket connection manager, message broadcast, and presence tracking.
- **Phase 194: Capstone 4: Distributed Cache Simulator** — Partitioning, consistent hash ring, replication, and node failover.
- **Phase 195: Capstone 5: Distributed Queue Simulator** — Partitions, consumer group offsets, visibility timeouts, and DLQs.
- **Phase 196: Capstone 6: Tiny Distributed KV Store** — Replicated key-value storage with N/W/R quorums.
- **Phase 197: Capstone 7: Production-Like Social Feed** — Feed generation with hybrid fanout handling celebrity accounts.
- **Phase 198: Failure Day** — Comprehensive chaos day: injecting 8 failure modes into a production capstone and recovering.
- **Phase 199: Architecture Review** — Complete architectural scorecard evaluation across all 11 non-functional dimensions.
- **Phase 200: Final Design Challenge** — Independent end-to-end design: Globally Available Collaborative Document Service.
