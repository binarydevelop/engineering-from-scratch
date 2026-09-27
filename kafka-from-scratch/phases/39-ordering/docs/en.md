# Lesson 39: Ordering

## Motto
"Kafka does not guarantee global order; Kafka guarantees partition order. Design your keys accordingly."

## Problem
A user executes three operations on their bank account:
1. `Deposit $100` (Account: $100)
2. `Withdraw $80` (Account: $20)
3. `Withdraw $50` (Declined - Insufficient funds!)
If these three events are published without keys to a 3-partition topic:
* Event 1 lands on Partition 0.
* Event 2 lands on Partition 1.
* Event 3 lands on Partition 2.
Because different consumers read different partitions at different speeds, Event 3 is processed first!
The user's withdrawal is rejected even though they had $100 in their account!
How does Kafka preserve causality?

## Prediction
What happens to ordering when causally related events are scattered across multiple partitions?

## Why this matters
Total global ordering across a distributed system requires serializing all writes through a single thread on a single machine (Amdahl's Law). Kafka achieves massive scale by scoping ordering strictly to the partition.

## First principles
* **Partition Total Order:** Records within a partition are strictly sequential ($0, 1, 2, ...$).
* **Cross-Partition Interleaving:** No ordering guarantee exists across different partitions.
* **Keying for Causality:** To preserve order for an entity, all events for that entity must share the same partition key.

## Mental model
```text
Unkeyed (Scattered across partitions - Causality Broken!):
Partition 0: [ Deposit $100 ]
Partition 1: [ Withdraw $80 ]  <-- Consumer B processes this first!
Partition 2: [ Withdraw $50 ]  <-- Consumer C processes this second! (Overdrawn!)

Keyed by Account ID "acc-42" (Guaranteed Chronological Order!):
Partition 1: [ Deposit $100 (off 0) ──► Withdraw $80 (off 1) ──► Withdraw $50 (off 2) ]
Result: Deterministic, correct financial execution!
```

## Build it
See [ordering_guarantees_lab.py](../code/ordering_guarantees_lab.py).
We demonstrate order preservation via keying vs out-of-order interleaving without keys.

## Use Kafka
Produce sequential records to Kafka and verify partition-scoped arrival.

## Inspect it
Consume from multiple partitions and observe out-of-order interleaving in real-time.

## Measure it
Measure throughput cost of single-partition total ordering vs multi-partition key-based ordering.

## Break it
Send causally related events with `key=None` across a 4-partition topic and observe interleaved processing.

## Recover it
Key all related events by entity ID (`account_id`, `user_id`, `order_id`).

## Modify it
Implement a single-partition topic to observe true global FIFO order (and observe throughput limits).

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why is global FIFO ordering fundamentally incompatible with horizontal distributed scale?
2. If two events happen for *different* users, does your application actually care which one is processed first?

## Guarantees
* Strict, deterministic chronological order within any single partition.

## Non-guarantees
* Zero ordering guarantees between different partitions.

## When to use this
* Per-entity ordering for financial transactions, state machines, user actions.

## When not to use this
* Demanding global topic-wide order across independent entities (an architectural anti-pattern).

## What comes next
In Phase 40, we examine Time semantics in Kafka: CreateTime, LogAppendTime, and ProcessingTime.
