# Lesson 13: Offset Commits

## Motto
"An uncommitted offset is a promise of duplicate processing upon restart."

## Problem
A consumer fetches 500 records from Kafka.
How and when does Kafka know the consumer has finished processing them?
If the consumer process crashes, how does Kafka decide which offset to hand the replacement consumer?
This is governed by **Offset Commits**.

## Prediction
If `enable.auto.commit=true` (the default) commits offsets every 5 seconds, what happens if your application crashes 4 seconds after processing 1,000 records?

## Why this matters
Blindly relying on default auto-commits causes silent duplicate processing or data loss during crashes. Production systems require deliberate commit strategies (`commitSync` or `commitAsync`).

## First principles
* **The `__consumer_offsets` Topic:** Committed offsets are simply messages written to an internal, compacted topic: `(group, topic, partition) -> offset`.
* **Synchronous vs Asynchronous Commits:**
  * `commitSync()`: Blocks until the coordinator broker acknowledges the commit. High reliability, adds latency.
  * `commitAsync()`: Fire-and-forget commit. Fast, but cannot safely retry without sequence guards.

## Mental model
```text
Consumer Loop
┌────────────────────────────────────────────────────────┐
│ 1. records = consumer.poll()                           │
│ 2. for record in records:                              │
│       process_business_logic(record)                   │
│ 3. consumer.commitSync()  ─────────────────────────┐   │
└────────────────────────────────────────────────────┼───┘
                                                     ▼ (TCP Commit Request)
Kafka Coordinator Broker
┌────────────────────────────────────────────────────────┐
│ Writes to internal compacted topic:                    │
│   Key:   [Group: "order-svc", Topic: "orders", Part: 0]│
│   Value: [Committed Offset: 42, Timestamp: ...]        │
└────────────────────────────────────────────────────────┘
```

## Build it
See [commit_semantics_demo.py](../code/commit_semantics_demo.py).
We demonstrate manual offset commits using synchronous and batched approaches.

## Use Kafka
Inspect committed offsets using the CLI:
```bash
docker exec -it kafka-lab-single /opt/kafka/bin/kafka-consumer-groups.sh   --bootstrap-server localhost:9092   --describe --group commit-lab-group
```

## Inspect it
Observe the difference between `CURRENT-OFFSET` and `LOG-END-OFFSET`.

## Measure it
Compare loop throughput of committing after *every single record* vs committing once *per batch*.

## Break it
Process records but never call `commitSync()`; restart the consumer and observe it re-reading from the old offset forever.

## Recover it
Implement proper batch commit at the end of each poll loop.

## Modify it
Configure manual commit with explicit offset maps (`{TopicPartition: OffsetAndMetadata}`).

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does committing after every single message destroy consumer throughput?
2. What is the danger of `commitAsync()` if a later commit succeeds before an earlier retried commit?

## Guarantees
* A committed offset represents the position from which a restarting consumer will fetch.

## Non-guarantees
* Committing an offset does not guarantee the downstream database transaction committed unless two-phase commit or transactional outbox is used.

## When to use this
* In all production consumers where data loss or uncontrolled duplicates must be managed.

## When not to use this
* Trivial analytics or telemetry where duplicate or dropped counts are acceptable.

## What comes next
In Phase 14, we formalize At-Most-Once vs. At-Least-Once delivery semantics through controlled failure injection.
