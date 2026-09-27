# Curriculum Roadmap: 68 Phases to Apache Kafka Mastery

> **Motto:** Understand it. Build it. Measure it. Break it. Recover it. Scale it. Ship it.

This roadmap outlines the complete 68-phase progression from a raw binary append-only log file to multi-broker KRaft clusters, transactional stream processing, and production system architecture.

---

## High-Level Curriculum Progression

```text
FOUNDATIONS & APPEND-ONLY LOGS
├── Phase 00: Environment and Kafka Lab
├── Phase 01: Why Kafka Exists (Direct Coupling Collapse)
├── Phase 02: Build an Append-Only Log (MiniLog)
├── Phase 03: Offsets (Log Position vs Consumer Position)
├── Phase 04: Make the Log a Network Service (TCP Sockets)
└── Phase 05: Topics (Named Logical Streams)
      │
KAFKA CLIENTS, PARTITIONS & KEYING
├── Phase 06: Kafka Producers and Consumers
├── Phase 07: Why Partitions Exist (Single Log Bottleneck)
├── Phase 08: Partitioning by Key (Deterministic Routing)
└── Phase 09: Hot Partitions (Workload Skew)
      │
CONSUMER GROUPS, REBALANCING & DELIVERY SEMANTICS
├── Phase 10: Consumer Groups From First Principles
├── Phase 11: Consumer Parallelism Limits (Partitions Ceiling)
├── Phase 12: Consumer Rebalancing (Membership Transitions)
├── Phase 13: Offset Commits (__consumer_offsets Mechanics)
├── Phase 14: At-Most-Once and At-Least-Once
└── Phase 15: Idempotent Consumers (Deduplication Store)
      │
PRODUCER PERFORMANCE & DURABILITY CONTROLS
├── Phase 16: Producer Batching (linger.ms & batch.size)
├── Phase 17: Compression (Batch-Level Codecs)
└── Phase 18: Producer Acknowledgments (acks=0, 1, all)
      │
REPLICATION, LEADERS, ISR & FAULT TOLERANCE
├── Phase 19: Why Replication Exists (Hardware Mortality)
├── Phase 20: Partition Leaders and Followers
├── Phase 21: ISR (In-Sync Replicas & High Watermark)
├── Phase 22: Leader Failure (Failover in <100ms)
├── Phase 23: min.insync.replicas (Durability Guardrails)
└── Phase 24: KRaft and Cluster Metadata (Native Raft Quorum)
      │
STORAGE ENGINE INTERNALS & LOG MECHANICS
├── Phase 25: Kafka Storage Model (.log, .index, .timeindex)
├── Phase 26: Why Kafka Can Be Fast on Disk (Page Cache & sendfile)
├── Phase 27: Segment Rolling (segment.bytes & segment.ms)
├── Phase 28: Retention (Time vs Size Retention)
├── Phase 29: Log Compaction (State Changelogs & Tombstones)
└── Phase 30: Replay (Historical State Reconstruction)
      │
BACKPRESSURE, IDEMPOTENCE & TRANSACTIONS
├── Phase 31: Consumer Lag (The Primary Health Indicator)
├── Phase 32: Backpressure (Little's Law & Buffer Capacity)
├── Phase 33: Producer Retries and Duplicates
├── Phase 34: Idempotent Producer (PID & Sequence Numbers)
├── Phase 35: Kafka Transactions (Two-Phase Commit Streams)
└── Phase 36: Exactly-Once Semantics (The Reality of EOS)
      │
EVENT DESIGN, SCHEMAS & ARCHITECTURE
├── Phase 37: Schema Evolution (Backward/Forward Compatibility)
├── Phase 38: Event Design (Notification vs State Transfer)
├── Phase 39: Ordering (Partition-Scoped Guarantees)
├── Phase 40: Time in Kafka (EventTime vs ProcessingTime)
├── Phase 41: Kafka as Queue vs Log (Architectural Comparison)
└── Phase 42: Multiple Consumer Groups (Independent Fan-out)
      │
RESILIENCE PATTERNS & CAPACITY PLANNING
├── Phase 43: Retry Patterns (Non-Blocking Retry Topics)
├── Phase 44: Dead-Letter Topics (Quarantining Poison Pills)
├── Phase 45: Large Messages (The Claim-Check Pattern)
├── Phase 46: Broker Disk and Capacity (Mathematical Sizing)
├── Phase 47: Partition Count and Capacity (Avoiding Explosion)
├── Phase 48: Reassigning Partitions (Cluster Rebalancing)
└── Phase 49: Adding a Broker (Expansion Semantics)
      │
FAILURE INJECTION, SECURITY & OPERATIONS
├── Phase 50: Broker Failure Scenarios (Chaos Injection)
├── Phase 51: Consumer Failure Scenarios (Rebalance Storms)
├── Phase 52: Producer Failure Scenarios (Retriable vs Fatal)
├── Phase 53: Kafka Security Basics (TLS, SASL, ACLs)
├── Phase 54: Observability (The 6 Golden Metrics)
└── Phase 55: Performance Testing (Benchmark Literacy)
      │
CAPSTONES & ADVANCED PATTERNS
├── Phase 56: Capstone 1: Build Mini-Kafka in Python
├── Phase 57: Capstone 2: Resilient Event-Driven Application
├── Phase 58: Event Sourcing Experiment (State from Events)
├── Phase 59: CDC Concept (Change Data Capture from WAL)
├── Phase 60: Transactional Outbox (Solving Dual-Writes)
├── Phase 61: Kafka Streams Concepts (Topologies & State Stores)
└── Phase 62: Real-Time Aggregation (Tumbling Windows)
      │
SYSTEM DESIGN, TRADE-OFFS & FINAL MASTERY
├── Phase 63: When Kafka Is the Wrong Tool
├── Phase 64: Kafka Anti-Patterns (14 Catastrophic Mistakes)
├── Phase 65: Capstone 3: Production-Like 3-Broker Lab
├── Phase 66: System Design With Kafka (The 20 Questions)
└── Phase 67: Final Mental Model (Complete Record Journey)
```

---

## Detailed Phase Breakdown Table

| Phase | Title | Prerequisite | Primary Experiment | Shipped Artifact | Mastery Check |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **00** | Environment & Kafka Lab | None | Run verification script, test TCP connection to port 9092, query KRaft cluster ID | `verify_lab.py` | Can verify broker TCP connectivity and explain client/broker separation. |
| **01** | Why Kafka Exists | Phase 00 | Simulate checkout service calling downstream services synchronously; inject slow consumer | `direct_coupled_services.py` | Explains how direct synchronous calls propagate latency and cause cascading outages. |
| **02** | Build an Append-Only Log | Phase 01 | Implement length-prefixed binary log with monotonic offsets on disk | `mini_log.py` | Can explain why sequential disk writes maximize throughput and why logs are immutable. |
| **03** | Offsets | Phase 02 | Track consumer position independently from log append offset; inject crash | `offsets_experiment.py` | Explains the fundamental difference: Log Offset != Consumer Position. |
| **04** | Log as Network Service | Phase 03 | Expose `MiniLog` over TCP socket with `APPEND` and `FETCH` commands | `tcp_log_server.py` | Explains why framed byte streams require length delimiters. |
| **05** | Topics | Phase 04 | Implement multi-topic log manager with isolated offset sequences | `topic_log_manager.py` | Explains topic isolation and why auto-topic creation is disabled in production. |
| **06** | Producers and Consumers | Phase 05 | Write real Python producer and consumer against Kafka 3.8.0 KRaft engine | `producer.py`, `consumer.py` | Traces the role of bootstrap servers, record serialization, and the poll loop. |
| **07** | Why Partitions Exist | Phase 06 | Implement multi-partition round-robin log; compare local vs global offsets | `partitioned_log_sim.py` | Explains why total ordering is partition-scoped and why partitions are the unit of scale. |
| **08** | Partitioning by Key | Phase 07 | Test hash-based partition routing with identical vs random keys | `key_partitioning.py` | Demonstrates how keys preserve per-entity ordering across a partitioned topic. |
| **09** | Hot Partitions | Phase 08 | Generate 90% key skew and measure partition workload imbalance | `hot_partition_analyzer.py` | Explains why high partition counts fail to solve key skew and how to salt keys. |
| **10** | Consumer Groups | Phase 09 | Simulate RangeAssignor dividing partitions across multiple consumers | `consumer_group_sim.py` | Enforces the invariant: within a group, each partition has at most one consumer. |
| **11** | Parallelism Limits | Phase 10 | Deploy 5 consumers against a 3-partition topic and observe idle standbys | `parallelism_limits.py` | Explains why active group concurrency cannot exceed topic partition count. |
| **12** | Consumer Rebalancing | Phase 11 | Register rebalance listener; observe partition revocation and assignment | `rebalance_observer.py` | Explains heartbeat timeouts, `session.timeout.ms`, and rebalance stops. |
| **13** | Offset Commits | Phase 12 | Implement manual synchronous offset commits; inspect `__consumer_offsets` | `commit_semantics_demo.py` | Explains the mechanics and trade-offs of commitSync vs commitAsync. |
| **14** | At-Most-Once / At-Least-Once | Phase 13 | Inject crashes before vs after database inserts to prove loss vs duplicates | `delivery_semantics_lab.py` | Derives delivery semantics from failure points; explains why at-least-once is standard. |
| **15** | Idempotent Consumers | Phase 14 | Build order consumer with SQLite deduplication store; deliver duplicates | `idempotent_consumer.py` | Proves that duplicate network deliveries do not produce duplicate business effects. |
| **16** | Producer Batching | Phase 15 | Benchmark synchronous sends vs batched sends with `linger.ms=20` | `batching_benchmark.py` | Quantifies the throughput/latency trade-off governed by `batch.size` and `linger.ms`. |
| **17** | Compression | Phase 16 | Measure compression ratios across batch payloads using Gzip, Snappy, LZ4 | `compression_benchmark.py` | Explains why batch-level compression achieves 5x-10x ratios with low broker CPU. |
| **18** | Producer Acks | Phase 17 | Measure produce latency across `acks=0`, `acks=1`, and `acks=all` | `acks_durability_lab.py` | Explains the durability contract and failure window of each acknowledgment setting. |
| **19** | Why Replication Exists | Phase 18 | Simulate 3-node log replication; kill leader and failover to follower | `replication_sim.py` | Explains why hardware mortality demands active partition replication. |
| **20** | Leaders and Followers | Phase 19 | Query 3-broker cluster to inspect partition leaders, followers, and ISR | `cluster_metadata_inspector.py` | Traces single-leader replication and follower TCP fetch requests. |
| **21** | In-Sync Replicas (ISR) | Phase 20 | Stop a follower; observe ISR drop after timeout; restart and observe recovery | `isr_monitor.py` | Explains ISR criteria, `replica.lag.time.max.ms`, and the High Watermark. |
| **22** | Leader Failure | Phase 21 | Kill partition leader broker; measure failover duration and client retries | `leader_failover_lab.py` | Explains KRaft controller leader election and client transparent reconnection. |
| **23** | min.insync.replicas | Phase 22 | Configure `min.insync.replicas=2`; kill 2 brokers; observe write rejection | `min_isr_lab.py` | Explains the gold-standard durability pair: `acks=all` + `min.insync.replicas=2`. |
| **24** | KRaft & Cluster Metadata | Phase 23 | Explore the `@metadata-0` partition; inspect active controller identity | `kraft_metadata_explorer.py` | Explains KRaft Raft consensus and the historical elimination of ZooKeeper. |
| **25** | Kafka Storage Model | Phase 24 | Inspect partition directories on disk: `.log`, `.index`, `.timeindex` | `inspect_storage_segments.py` | Explains sparse indexing and how memory-mapped indexes enable $O(1)$ lookups. |
| **26** | Why Fast on Disk | Phase 25 | Benchmark sequential disk appends vs random seeks; explain zero-copy | `sequential_vs_random_io.py` | Debunks the "disk is slow" myth; explains page cache and Linux `sendfile()`. |
| **27** | Segment Rolling | Phase 26 | Configure 10KB segments; produce records and observe segment rolls | `segment_rolling_lab.py` | Explains why logs are segmented and why historical segments are immutable. |
| **28** | Retention | Phase 27 | Configure 5s retention; observe background cleaner purging old segments | `retention_lab.py` | Proves that consumption does not delete records and explains time/size retention. |
| **29** | Log Compaction | Phase 28 | Produce updates and tombstones; observe cleaner deduplicating by key | `log_compaction_lab.py` | Contrasts retention with compaction; explains state changelogs and tombstones. |
| **30** | Replay | Phase 29 | Simulate corrupted state calculation; reset consumer offset to 0 and replay | `replay_lab.py` | Explains state reconstruction via replay and the dangers of non-idempotent replays. |
| **31** | Consumer Lag | Phase 30 | Build real-time lag calculator measuring LEO minus committed offset | `lag_monitor.py` | Identifies lag as the primary operational indicator of business health. |
| **32** | Backpressure | Phase 31 | Model queue accumulation under $P > C$; calculate catch-up time via Little's Law | `backpressure_sim.py` | Explains pull-based flow control and storage buffer saturation limits. |
| **33** | Retries and Duplicates | Phase 32 | Simulate lost network ACKs; observe duplicate records on broker | `network_retry_duplicate_sim.py` | Proves why standard retries produce duplicate writes over lossy networks. |
| **34** | Idempotent Producer | Phase 33 | Verify PID and sequence number deduplication on broker with retries | `idempotent_producer_lab.py` | Explains how broker-side sequence tracking eliminates retry duplicates. |
| **35** | Kafka Transactions | Phase 34 | Execute consume-transform-produce transactional loop with 2PC commit markers | `transactional_processor.py` | Explains transaction coordinators and atomic input-offset/output-record commits. |
| **36** | Exactly-Once Semantics | Phase 35 | Demystify EOS; test boundary where Kafka EOS ends and external APIs begin | `eos_boundaries_lab.py` | Clearly articulates what Kafka EOS guarantees vs what it does NOT guarantee. |
| **37** | Schema Evolution | Phase 36 | Test backward/forward compatible schema changes; prevent deserialization crashes | `schema_evolution_lab.py` | Explains schema contracts, optional fields, and breaking change prevention. |
| **38** | Event Design | Phase 37 | Generate domain event envelopes; contrast Notification vs State Transfer | `event_design_patterns.py` | Formulates rich domain events with UUIDs, timestamps, and correlation IDs. |
| **39** | Ordering | Phase 38 | Contrast unkeyed causal interleaving with keyed partition-scoped order | `ordering_guarantees_lab.py` | Explains the fundamental trade-off: local order vs horizontal parallelism. |
| **40** | Time in Kafka | Phase 39 | Contrast CreateTime (Event Time), LogAppendTime, and Processing Time | `time_semantics_lab.py` | Explains why stream windowing must operate on Event Time rather than system time. |
| **41** | Kafka as Queue vs Log | Phase 40 | Side-by-side comparison of destructive pop queues vs non-destructive logs | `queue_vs_log_comparison.py` | Defines exact criteria for selecting RabbitMQ/SQS vs Apache Kafka. |
| **42** | Multiple Consumer Groups | Phase 41 | Demonstrate fan-out across fraud, email, and analytics consumer groups | `multi_group_fanout.py` | Proves independent group offset tracking without producer modifications. |
| **43** | Retry Patterns | Phase 42 | Implement non-blocking retry topics with exponential backoff delay | `retry_topic_pattern.py` | Prevents slow processing from stalling main partition consumption. |
| **44** | Dead-Letter Topics | Phase 43 | Quarantine poison pill records to DLT with forensic diagnostic headers | `dead_letter_queue_lab.py` | Explains DLT triage and why unmonitored DLTs are dangerous. |
| **45** | Large Messages | Phase 44 | Implement Claim-Check pattern using external storage + lightweight event | `claim_check_pattern.py` | Explains why >1MB payloads harm Kafka brokers and how Claim-Check solves it. |
| **46** | Broker Disk & Capacity | Phase 45 | Calculate daily ingestion, replicated storage, headroom, and bandwidth | `capacity_calculator.py` | Provides rigorous capacity math formulas for pre-production planning. |
| **47** | Partition Count Sizing | Phase 46 | Size partition count based on throughput requirements and broker counts | `partition_sizing_tool.py` | Explains the costs of partition explosion (file handles, memory, failover). |
| **48** | Reassigning Partitions | Phase 47 | Generate and execute partition migration plan across cluster brokers | `reassign_partitions_demo.py` | Explains online partition reassignment and replication bandwidth throttling. |
| **49** | Adding a Broker | Phase 48 | Simulate adding Broker 4; prove existing partitions do NOT auto-migrate | `add_broker_simulation.py` | Debunks the myth that Kafka automatically rebalances data on broker join. |
| **50** | Broker Failure Scenarios | Phase 49 | Inject controlled broker failures; observe leader election and ISR healing | `chaos_broker_failure.py` | Verifies cluster high availability under active chaos injection. |
| **51** | Consumer Failure Scenarios | Phase 50 | Simulate poll interval timeouts and diagnose consumer rebalance storms | `chaos_consumer_failure.py` | Diagnoses slow consumers and tunes `max.poll.interval.ms`. |
| **52** | Producer Failure Scenarios | Phase 51 | Classify retriable vs fatal producer exceptions and tune client timeouts | `chaos_producer_failure.py` | Defines robust client retry policies and circuit breaking. |
| **53** | Kafka Security Basics | Phase 52 | Inspect TLS encryption, SASL authentication (SCRAM/mTLS), and ACL rules | `security_config_inspector.py` | Defines production security baseline: SASL_SSL with fine-grained ACLs. |
| **54** | Observability | Phase 53 | Display the 6 Golden Metrics: URP, OfflinePartitions, ControllerCount, Lag | `cluster_metrics_collector.py` | Establishes critical operational alerts to wake on-call engineers. |
| **55** | Performance Testing | Phase 54 | Benchmark throughput and p50/p95/p99 latency under documented settings | `benchmark_runner.py` | Instills benchmark literacy; emphasizes hardware and configuration context. |
| **56** | Capstone 1: Mini-Kafka | Phase 55 | Build a complete Kafka-like engine in pure Python with tests | `mini_kafka.py` | Cements the append-only log, partition, offset, and consumer group mental models. |
| **57** | Capstone 2: Event-Driven App | Phase 56 | Build e-commerce pipeline with Order API, payment, email, analytics workers | `event_driven_app.py` | Integrates idempotency, retry topics, DLT, and lag monitoring into one app. |
| **58** | Event Sourcing | Phase 57 | Build event-sourced ledger; delete projection state and rebuild via replay | `event_sourcing_lab.py` | Demonstrates the append-only log as the fundamental system of record. |
| **59** | CDC Concept | Phase 58 | Simulate database WAL parsing into real-time Kafka change streams | `cdc_simulation.py` | Explains Change Data Capture, Debezium, and streaming database synchronization. |
| **60** | Transactional Outbox | Phase 59 | Eliminate dual-write vulnerabilities with outbox table + relay poller | `transactional_outbox_lab.py` | Solves database + Kafka inconsistency without distributed 2PC. |
| **61** | Kafka Streams Concepts | Phase 60 | Explore streaming topologies: KStream vs KTable and state stores | `stream_processing_concepts.py` | Explains stream-table duality and co-partitioning invariants. |
| **62** | Real-Time Aggregation | Phase 61 | Implement 10-second tumbling window event count aggregator | `tumbling_window_aggregator.py` | Explains time windowing, watermarks, and late-arriving event handling. |
| **63** | When Kafka is Wrong | Phase 62 | Evaluate anti-use cases: simple queues, key lookups, tiny volume | `evaluate_kafka_fit.py` | Enforces engineering trade-off discipline; prevents resume-driven architecture. |
| **64** | Kafka Anti-Patterns | Phase 63 | Catalog 14 catastrophic production mistakes and their remediations | `anti_patterns_analyzer.py` | Establishes a production readiness audit checklist. |
| **65** | Capstone 3: Production Lab | Phase 64 | Run 3-broker KRaft cluster with replication, chaos injection, and failover | `production_lab_runner.py` | Demonstrates complete operational and distributed resilience in practice. |
| **66** | System Design With Kafka | Phase 65 | Interrogate 10 real-world systems with the 20-Question Framework | `system_design_evaluator.py` | Masters technical justification and specification for system design reviews. |
| **67** | Final Mental Model | Phase 66 | Programmatically trace a single record from producer socket to commit | `trace_record_lifecycle.py` | Synthesizes complete mastery: Kafka is no longer a black box. |
