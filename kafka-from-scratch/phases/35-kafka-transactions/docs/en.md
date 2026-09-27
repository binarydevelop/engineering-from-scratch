# Lesson 35: Kafka Transactions

## Motto
"Transactions bind input offsets and output events in an atomic embrace."

## Problem
Consider a streaming pipeline that reads from `input-topic` and publishes to `output-topic`:
```text
1. Fetch record at Offset 100 ("Transfer $50 from Alice to Bob")
2. Produce transformed record to output topic
3. Commit offset 100
```
What if the process crashes after step 2, but before step 3?
Upon restart, it re-fetches Offset 100 and publishes a *second* transformed record to `output-topic`!
How can we make **producing output records** and **committing input offsets** occur **atomically** together?

## Prediction
What happens to uncommitted transactional records in Kafka if the producer process crashes mid-transaction?

## Why this matters
**Kafka Transactions enable Exactly-Once Processing (EOS) in Kafka-to-Kafka streaming workflows.**
They ensure that downstream consumers only see output records if the corresponding input offsets were successfully committed.

## First principles
* **Transaction Coordinator:** A specialized broker managing transaction state via an internal topic `__transaction_state`.
* **Two-Phase Commit (2PC):**
  1. Producer registers partitions and sends records marked as uncommitted.
  2. Producer sends input offsets to the transaction coordinator (`sendOffsetsToTxn`).
  3. Coordinator writes `PREPARE_COMMIT` marker, flushes, and writes `COMMIT` marker to all participating partitions.
* **Isolation Level:** Consumers configured with `isolation.level=read_committed` skip uncommitted or aborted transaction batches.

## Mental model
```text
Stream Processor (Transactional Loop)
   ├── 1. beginTransaction()
   ├── 2. Process record from Topic A (Offset 50)
   ├── 3. send(Topic B, "Transformed Output")   <-- Marked as transactional!
   ├── 4. sendOffsetsToTransaction(Offset 50)  <-- Ties offset commit to txn!
   └── 5. commitTransaction()                   <-- Atomic Commit Marker!
Downstream Consumer (isolation.level=read_committed)
   └── Sees output message ONLY after Commit Marker appears!
```

## Build it
See [transactional_processor.py](../code/transactional_processor.py).
We demonstrate the complete transactional consume-transform-produce cycle.

## Use Kafka
Execute transactional writes and inspect with `read_committed` consumer.

## Inspect it
Observe transaction commit markers using `kafka-dump-log.sh`.

## Measure it
Measure latency overhead of two-phase commit markers vs non-transactional writes.

## Break it
Abort a transaction (`abortTransaction()`) and verify downstream `read_committed` consumers never see the aborted messages.

## Recover it
Demonstrate clean rollback without orphan messages.

## Modify it
Compare output visible to `read_uncommitted` vs `read_committed` consumers.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why must the input offset commit be routed through the Transaction Coordinator rather than committed directly to `__consumer_offsets`?
2. What is an aborted transaction marker, and why does it still consume disk space in the log?

## Guarantees
* Atomicity across multiple topic-partitions and consumer offset commits.

## Non-guarantees
* Does NOT make external non-Kafka databases (e.g. Postgres) exactly-once.

## When to use this
* Stream processing applications reading from Kafka and producing to Kafka (Kafka Streams, Flink).

## When not to use this
* Simple ingestion pipelines where downstream consumers are already idempotent.

## What comes next
In Phase 36, we evaluate the real boundaries of Exactly-Once Semantics (EOS).
