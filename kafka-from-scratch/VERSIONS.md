# Pinned Versions & Architectural Specifications

This document defines the exact, pinned software versions, protocol baselines, and architectural choices used throughout `kafka-from-scratch`.

---

## 1. Primary Engine & Infrastructure

| Component | Pinned Version | Rationale & Status |
| :--- | :--- | :--- |
| **Apache Kafka** | `3.8.0` | Production-stable Apache Kafka release featuring mature KRaft consensus as the standard architecture. |
| **Kafka Architecture** | **KRaft Mode** (KIP-500) | Pure KRaft metadata quorum. **ZooKeeper is not used as the runtime broker coordinator.** ZooKeeper is discussed strictly historically in Phase 24. |
| **Docker Engine** | `apache/kafka:3.8.0` | Official Apache Software Foundation (ASF) Docker image running KRaft out-of-the-box. |
| **Docker Compose** | Compose v2 / v5+ | Standard orchestration for single-broker and 3-broker KRaft clusters. |
| **Java Runtime** | OpenJDK 21 LTS | Packaged inside the official Kafka container image. |

---

## 2. Python Client Libraries & Tooling

| Package | Pinned Version | Role & Usage |
| :--- | :--- | :--- |
| **Python** | `3.12+` (Tested on 3.14) | Base language for all first-principles simulations, client scripts, and benchmarks. |
| **`kafka-python-ng`** | `2.2.3` | Modern, maintained pure-Python Kafka client for first-principles inspection and transparent packet tracing. |
| **`confluent-kafka`** | `2.15.1` | High-performance C-based (`librdkafka`) client for production throughput, batching, and exact transactional semantics. |
| **`pytest`** | `>= 8.0.0` | Test runner for automated curriculum validation suite. |
| **`rich`** | `>= 13.7.0` | Terminal formatting for partition distribution, ISR state, and log inspectors. |
| **`psutil`** | `>= 5.9.0` | OS page cache, memory, and process measurements. |

---

## 3. Public Semantics vs. 3.8.0 Implementation Details

To build deep system-design intuition, learners must distinguish between universal Kafka protocol semantics and specific implementation details of version 3.8.0:

### Universal Public Semantics (True Across All Kafka Versions)
* **Log Invariant:** Partitions are strictly ordered, immutable, append-only sequences of records.
* **Offset Semantics:** Offsets are sequential 64-bit integers scoped strictly to a single partition. Total topic-wide ordering does not exist across multiple partitions.
* **Consumer Group Contract:** Within a single consumer group, each partition is consumed by at most one consumer process at any point in time.
* **Producer Delivery Semantics:** `acks=0` (fire-and-forget), `acks=1` (leader local write), `acks=-1` / `acks=all` (quorum of in-sync replicas acknowledged).
* **Durability Primitives:** Replication factor $N$, minimum in-sync replicas ($M$), and leader election from the in-sync replica set (ISR).

### Version 3.8.0 Specific Implementation Details
* **KRaft Quorum:** Cluster metadata is stored directly in an internal Kafka topic (`@metadata`) managed by an active controller leader elected via a Raft-variant protocol (KIP-500 / KIP-595), eliminating the external ZooKeeper cluster.
* **Default Producer Idempotence:** Producers enable `enable.idempotence=true` by default since Kafka 3.0.0. In this repo we explicitly toggle and observe it.
* **Default Acks:** Producer defaults to `acks=all` since Kafka 3.0.0.
* **Log Format Version:** Record batch format v2 (introduced in Kafka 0.11 and refined in 3.x), utilizing varint encoding, CRC32C checksums, and relative offset deltas within batches.
* **Consumer Group Protocol:** Kafka 3.8 includes early access to KIP-848 (the next-generation consumer group protocol moving rebalance logic to the broker coordinator), alongside the classic client-side partition assignor protocol. We teach the established client-side protocol and contrast it with KIP-848.

---

## 4. Verification Check

Before beginning Phase 00, verify your host environment against these baselines:

```bash
cd kafka-from-scratch
make env-check
```
