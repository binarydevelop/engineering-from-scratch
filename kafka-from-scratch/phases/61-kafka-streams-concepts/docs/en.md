# Lesson 61: Kafka Streams Concepts

## Motto
"Don't move data to the compute; move compute directly onto the log partitions."

## Problem
In earlier phases, we wrote individual producers and consumers.
What if you need to build complex streaming applications:
* Filter fraudulent transactions
* Enrich orders with user profiles
* Compute sliding window click counts
* Join two high-volume streams (`orders` and `shipments`)
Writing raw consumer poll loops, managing consumer group rebalances, state caches, and rockdb checkpoints by hand is overwhelming.
How does stream processing simplify this?

## Prediction
What is the difference between a `KStream` (record stream) and a `KTable` (changelog stream) in stream processing?

## Why this matters
**Stream processing operates directly on unbounded data streams.**
Kafka Streams (and Flink) provide high-level functional DSLs (`map`, `filter`, `groupBy`, `aggregate`, `join`) with managed, fault-tolerant local state.

## First principles
* **Streaming Topology:** A directed acyclic graph (DAG) of processing nodes: Source Node $\longrightarrow$ Processor Nodes $\longrightarrow$ Sink Node.
* **Stateless Operations:** `filter()`, `map()`, `branch()`. Zero memory state across records.
* **Stateful Operations:** Aggregations, windowing, joins. Requires a local **State Store** (backed by RocksDB on disk and backed up to an internal compacted Kafka topic).
* **The Dualism:**
  * **Stream as Table:** A stream of insert/update events represents the changelog of a table.
  * **Table as Stream:** A table snapshot represents the aggregated state of a stream.

## Mental model
```text
Stream Processing DAG Topology:
[ Source: "orders" ]
        │
        ▼
  [ filter(amount > 100) ]  <-- Stateless
        │
        ▼
  [ groupBy(customer_id) ]
        │
        ▼
  [ count(window=5min) ]   <-- Stateful (RocksDB State Store)
        │
        ▼
[ Sink: "vip-alerts" ]
```

## Build it
See [stream_processing_concepts.py](../code/stream_processing_concepts.py).
We implement the core abstractions of a stream processing topology in pure Python.

## Use Kafka
Understand stream processing architecture and state store changelogs.

## Inspect it
Observe state store backing topics (`<app-id>-state-store-changelog`).

## Measure it
Measure memory footprint of state stores vs streaming throughput.

## Break it
Kill a stream processing instance and observe state store recovery from the changelog topic.

## Recover it
Standby replicas allow instantaneous failover without rebuilding RocksDB state.

## Modify it
Implement a sliding window join between two event streams.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. What is the Stream-Table Duality, and why is it central to event processing?
2. How does Kafka Streams achieve fault tolerance for local RocksDB state stores?

## Guarantees
* Exactly-once stream processing when configured with EOS transactions.

## Non-guarantees
* Stateful stream joins require both topics to be co-partitioned (same partition count and same keying).

## When to use this
* Real-time analytics, continuous enrichment, streaming ETL pipelines.

## When not to use this
* Simple fire-and-forget message forwarding.

## What comes next
In Phase 62, we implement Real-Time Aggregation using sliding and tumbling time windows.
