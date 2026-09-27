# kafka-from-scratch

> **Understand it. Build it. Measure it. Break it. Recover it. Scale it. Ship it.**

An experimental, first-principles curriculum that demystifies Apache Kafka for software engineers. Instead of memorizing Kafka CLI commands or treating Kafka as a magic "message queue," you will build append-only logs, partition routers, consumer groups, and replication loops from scratch in pure Python before mastering production-grade Kafka 3.8.0 in pure KRaft mode.

---

## The Core Philosophy: Replacing the Black Box

Most engineers treat Kafka as a mysterious black box:

```text
                  THE BLACK BOX (Cargo Cult Intuition)
   ┌────────────────────────────────────────────────────────┐
   │  "kafka-console-producer.sh"                           │
   │         │                                              │
   │         ▼                                              │
   │  ✨ Magic Enterprise Message Queue Land ✨             │
   │  (RabbitMQ on steroids? Cloud magic?)                  │
   │         │                                              │
   │  Everything works until:                               │
   │  - Consumer lag explodes without warning               │
   │  - Rebalance storm stops all message consumption       │
   │  - Broker dies and writes are rejected (NotEnoughReplicas)
   │  - Retries cause duplicate credit card billings        │
   │  - Messages arrive out of order                        │
   │         │                                              │
   │  Desperate solution: "Restart the consumer pods!"      │
   └────────────────────────────────────────────────────────┘
```

This repository systematically replaces that intuition with an accurate mechanical mental model:

```text
                 THE FIRST-PRINCIPLES REALITY
   ┌────────────────────────────────────────────────────────┐
   │  Kafka is a distributed, replicated, partitioned       │
   │  append-only log with producer, consumer, storage,     │
   │  and coordination semantics layered around it.         │
   ├────────────────────────────────────────────────────────┤
   │  • Storage:    Sequential disk appends + OS Page Cache  │
   │  • Order:      Guaranteed strictly per-partition       │
   │  • Reads:      Non-destructive sequential offset fetches│
   │  • Scale:      Partitions divide work across consumers  │
   │  • Safety:     ISR Quorum + min.insync.replicas         │
   │  • Control:    KRaft native Raft metadata quorum        │
   └────────────────────────────────────────────────────────┘
```

---

## What You Will Master

By completing this curriculum, you will answer every one of these questions from first principles:

* **Why does Kafka exist?** What failure mode of synchronous point-to-point microservices forced its creation?
* **What problem does an append-only log solve?** Why does sequential I/O make writing to disk as fast as memory?
* **What exactly is a topic? What is a partition?** Why is total ordering partition-scoped rather than global?
* **What is an offset?** Why does each partition have its own independent offsets, and why is Log Offset $\neq$ Consumer Position?
* **What is a broker?** What does a partition leader do vs. follower replicas?
* **What is the ISR?** What happens if a follower lags behind, and why is `acks=all` meaningless without `min.insync.replicas=2`?
* **What happens if a leader broker dies?** How does KRaft coordinate failover in under 100 milliseconds?
* **What is a consumer group?** Why can only one consumer in a group consume a given partition at a time?
* **What causes a consumer rebalance storm?** What is the difference between `session.timeout.ms` and `max.poll.interval.ms`?
* **Where are consumer offsets stored?** What happens if a consumer crashes before committing its offset?
* **What is the difference between at-most-once and at-least-once?** How do you build an Idempotent Consumer?
* **What does Kafka mean by "Exactly-Once Semantics"?** Where does that guarantee stop when external databases are involved?
* **How does Kafka store data on disk?** What are `.log`, `.index`, and `.timeindex` segment files?
* **What is the difference between retention and compaction?** When do tombstones matter?
* **What is Consumer Lag?** How do you diagnose and debug a slow consumer pipeline?
* **When should Kafka NOT be used?** When is Postgres, RabbitMQ, Redis Streams, or S3 a vastly superior choice?

---

## Architectural Progression

```text
       Append-Only Log (MiniLog on Disk)
                      │
                      ▼
        Offsets (Position vs Append Point)
                      │
                      ▼
         Topics (Named Logical Streams)
                      │
                      ▼
       Partitions (The Unit of Scalability)
                      │
                      ▼
       Key Partitioning (Per-Entity Order)
                      │
                      ▼
  Consumer Groups (Coordinated Work Allocation)
                      │
                      ▼
       Delivery Semantics & Idempotency
                      │
                      ▼
       Batching, Compression & Producer Acks
                      │
                      ▼
         Replication, Leaders & the ISR
                      │
                      ▼
       KRaft Quorum & Metadata Architecture
                      │
                      ▼
       Storage Internals & Page Cache Zero-Copy
                      │
                      ▼
          Retention, Compaction & Replay
                      │
                      ▼
       Lag, Backpressure & Little's Law
                      │
                      ▼
       Transactions & Exactly-Once Boundaries
                      │
                      ▼
      Resilience, Chaos & Capacity Planning
                      │
                      ▼
       Capstones & 20-Question System Design
```

---

## Pinned Versions & Environment Discipline

To ensure complete reproducibility and avoid confusing legacy ZooKeeper tutorials with modern production reality, all commands and configurations are strictly pinned:

* **Apache Kafka Engine:** `3.8.0` (Official ASF Docker image: `apache/kafka:3.8.0`)
* **Cluster Architecture:** **Pure KRaft Mode** (Kafka Raft Metadata Quorum, KIP-500). **No ZooKeeper.**
* **Python Runtimes:** Python `3.12+` (Tested through 3.14)
* **Python Clients:** `kafka-python-ng==2.2.3` (Pure Python inspection) & `confluent-kafka==2.15.1` (librdkafka C engine)
* **Orchestration:** Docker Compose v2 / v5

See [VERSIONS.md](VERSIONS.md) for detailed architectural specifications.

---

## The Learning Loop & Evidence Discipline

A lesson is **NOT** complete merely because shell commands ran without errors. Every lesson follows an 11-step execution loop:

```text
READ ──► PREDICT ──► BUILD ──► RUN ──► INSPECT ──► MEASURE ──► EXPLAIN ──► MODIFY ──► BREAK ──► RECOVER ──► REBUILD
```

1. **Predict First:** Write down your explicit hypothesis before executing commands.
2. **Build from Scratch:** Construct a pure Python prototype before touching real Kafka.
3. **Inspect Raw State:** Look directly at socket bytes, on-disk log segments, and `__consumer_offsets`.
4. **Measure Everything:** Capture records/sec, MB/sec, p50/p99 latency, and consumer lag.
5. **Break It Intentionally:** Kill the leader broker, pause a consumer, corrupt records, or inject key skew.
6. **Save Evidence:** Document observations in each phase's `outputs/evidence-template.md`.

Read [LEARNING.md](LEARNING.md) for the complete study methodology.

---

## Curriculum Overview (68 Phases)

| Module | Phases | Core Focus |
| :--- | :--- | :--- |
| **1. Foundations & Append-Only Logs** | 00 – 05 | Lab preflight, direct coupling collapse, `MiniLog`, offsets, TCP socket servers, multi-topic isolation. |
| **2. Kafka Clients, Partitions & Keying** | 06 – 09 | Python Kafka client, partition-local ordering, hash partitioning, and hot partition skew analysis. |
| **3. Consumer Groups & Delivery Semantics** | 10 – 15 | Range assignment, partition concurrency ceiling, rebalance storms, offset commits, at-least-once, idempotent consumers. |
| **4. Producer Performance & Durability** | 16 – 18 | Batching (`linger.ms`/`batch.size`), LZ4/ZSTD compression, and `acks=0/1/all` durability windows. |
| **5. Replication & Fault Tolerance** | 19 – 24 | Hardware mortality, partition leaders/followers, ISR dynamics, leader failover (<100ms), `min.insync.replicas=2`, KRaft metadata quorum. |
| **6. Storage Engine Internals** | 25 – 30 | `.log`/`.index`/`.timeindex` segments, page cache zero-copy (`sendfile`), segment rolling, retention, compaction, tombstones, and replay. |
| **7. Backpressure & Transactions** | 31 – 36 | Consumer lag monitoring, Little's Law backpressure, network retry duplicates, idempotent producers (PID/sequence), 2PC transactions, EOS boundaries. |
| **8. Event Design & Architecture** | 37 – 42 | Schema evolution, Event Notification vs State Transfer, causality ordering, Event Time vs Processing Time, Queue vs Log, multi-group fan-out. |
| **9. Resilience Patterns & Capacity** | 43 – 49 | Non-blocking retry topics, Dead-Letter Topics (DLT), Claim-Check pattern, capacity sizing math, partition count sizing, partition reassignment, broker addition. |
| **10. Failure Injection, Security & Ops** | 50 – 55 | Broker chaos injection, consumer poll timeouts, retriable vs fatal producer errors, TLS/SASL/ACL security, 6 Golden Metrics, performance benchmarking. |
| **11. Capstones & Advanced Patterns** | 56 – 62 | **Capstone 1: Mini-Kafka in Python**, **Capstone 2: Event-Driven App**, Event Sourcing, CDC (WAL capture), Transactional Outbox, Kafka Streams, Tumbling Windows. |
| **12. System Design & Final Mastery** | 63 – 67 | Anti-use cases, 14 Catastrophic Anti-Patterns, **Capstone 3: 3-Broker Production Lab**, 20-Question System Design Framework, Final Record Journey. |

See [ROADMAP.md](ROADMAP.md) for the complete 68-phase detailed syllabus with prerequisites and mastery checks.

---

## The Capstone Projects

* **Capstone 1: Build Mini-Kafka From Scratch in Pure Python ([projects/capstone-1-mini-kafka](projects/capstone-1-mini-kafka))**
  A complete educational broker supporting topics, partitions, length-prefixed binary append-only disk logs, monotonic offsets, key hashing, and consumer group offset tracking.
* **Capstone 2: Production-Grade Event-Driven Application ([projects/capstone-2-event-driven-app](projects/capstone-2-event-driven-app))**
  A multi-service e-commerce pipeline featuring an Order API, idempotent payment workers, email notification services, real-time analytics aggregation, retry topics, and dead-letter queues.
* **Capstone 3: Resilient 3-Broker Production Lab ([projects/capstone-3-production-lab](projects/capstone-3-production-lab))**
  A 3-broker KRaft cluster with replication factor 3, `min.insync.replicas=2`, automated chaos failure injection, leader failover measurement, and end-to-end telemetry.

---

## Quick Start: Launching the Lab

### 1. Preflight Check
Clone the repository and run the environment verifier:

```bash
cd kafka-from-scratch
make env-check
```

### 2. Launch the Single-Broker KRaft Lab
```bash
make up
```
This starts an official `apache/kafka:3.8.0` container in pure KRaft mode on port `9092` in ~2 seconds.

### 3. Verify Cluster Metadata
```bash
make cluster-info
```

### 4. Begin Lesson 00 & Lesson 01
Navigate to Phase 00:
```bash
cd phases/00-environment-and-kafka-lab
cat docs/en.md
./experiments/run_experiment.sh
```

---

## Verification & Test Suite

Run the automated validation suite across all 68 phases, unit tests, and Docker topologies:

```bash
make test
```

---

## Epilogue

> Kafka is no longer a black box.
>
> We started with a file that only knew how to append records. We added offsets, topics, partitions, consumers, replication, failure recovery, retention, batching, delivery semantics, transactions, and distributed coordination.
>
> Now when Kafka appears inside a system architecture, we can reason about why it is there, how records flow through it, what guarantees it provides, how it fails, and whether another design would be simpler.
