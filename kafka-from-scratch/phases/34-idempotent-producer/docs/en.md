# Lesson 34: Idempotent Producer

## Motto
"Sequence numbers turn blind retries into deduplicated no-ops."

## Problem
In Phase 33, we saw that retrying after a dropped ACK creates duplicate records on disk.
How can the broker recognize that a retried message is a duplicate of a message it already appended, and discard the duplicate without throwing an error to the producer?

## Prediction
If the producer tags every batch with a monotonic sequence number, what can the broker do when it receives sequence number #5 a second time?

## Why this matters
**The Idempotent Producer is one of Kafka's most elegant architectural features.**
It completely eliminates duplicate writes caused by producer retries, with zero performance penalty.

## First principles
When `enable.idempotence=true`:
1. **Producer ID (PID):** The broker assigns each producer a unique 64-bit PID during handshake (`InitProducerId`).
2. **Sequence Numbers:** The producer assigns an integer sequence number ($0, 1, 2, ...$) to every batch per topic-partition.
3. **Broker Deduplication:** The broker tracks the last committed sequence number for each `(PID, Partition)`.
   * If incoming sequence number == $\text{last} + 1$: **Append to log and increment sequence.**
   * If incoming sequence number $\le \text{last}$: **DUPLICATE! Discard write, but return SUCCESS to client!**
   * If incoming sequence number $> \text{last} + 1$: **GAP! Raise `OutOfOrderSequenceException` (potential missing data).**

## Mental model
```text
Producer (PID: 1001)                     Broker (Tracks PID 1001, Last Seq: 4)
   │                                              │
   ├─── 1. Send Batch (Seq: 5) ──────────────────►│ Seq 5 == Last(4) + 1 -> APPEND!
   │                                              │ Updates Last Seq = 5
   │◄── 2. Ack DROPPED by network! ───────────────┤
   │                                              │
   ├─── 3. Producer RETRIES Send Batch (Seq: 5) ─►│ Seq 5 <= Last(5) -> DUPLICATE!
   │                                              │ DOES NOT APPEND TO DISK!
   │◄── 4. Returns SUCCESS Ack! ──────────────────┘
Result: Exactly ONE write on disk! Zero duplicates!
```

## Build it
See [idempotent_producer_lab.py](../code/idempotent_producer_lab.py).
We configure and verify the idempotent producer.

## Use Kafka
In modern Kafka (3.0+), `enable.idempotence=true` is the default.
We explicitly verify this behavior.

## Inspect it
Use `kafka-dump-log.sh` to observe the `producerId` and `firstSequence` fields stored inside on-disk record batch headers.

## Measure it
Compare produce latency with idempotence enabled vs disabled (difference is negligible, < 1ms).

## Break it
Inject an artificial sequence number gap and observe `OutOfOrderSequenceException`.

## Recover it
Producer automatically refreshes PID state.

## Modify it
Verify that `max.in.flight.requests.per.connection` can safely be up to 5 without reordering when idempotence is active.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does the idempotent producer guarantee deduplication only within a single producer session and single partition?
2. What happens to the sequence number tracking if the producer application restarts?

## Guarantees
* Eliminates duplicate writes caused by producer network retries within a session.
* Preserves strict order even with up to 5 in-flight requests.

## Non-guarantees
* Does NOT prevent duplicate messages if the producer application restarts with a new PID and generates the same event twice.

## When to use this
* In all production Kafka producers (enabled by default).

## When not to use this
* Extremely legacy brokers (< v0.11) that do not support batch format v2.

## What comes next
In Phase 35, we extend idempotence across multiple partitions and consumers using Kafka Transactions.
