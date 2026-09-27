# Lesson 41: Kafka as Queue vs Log

## Motto
"A queue is an ephemeral checklist; a log is an immutable historical ledger."

## Problem
Many software engineers begin by asking: *"Is Kafka better than RabbitMQ or SQS?"*
This question stems from a category error:
* A Queue manages transient work items, deleting them as soon as one worker completes the task.
* A Log records immutable facts in chronological order, preserving them for multiple independent consumers to read and replay.
When should you pick a Queue, and when should you pick Kafka?

## Prediction
If you need individual message acknowledgments, dead-letter routing per message, and tasks distributed to 100 workers regardless of partition count, is Kafka or a Queue more suitable?

## Why this matters
Choosing Kafka when you actually need a simple task queue introduces massive partition management, consumer group rebalances, and ordering complexity for zero benefit.
Choosing a queue when you need event replay, multi-team fan-out, and high throughput leads to queue collapse.

## First principles
| Dimension | Traditional Queue (RabbitMQ / SQS) | Distributed Log (Apache Kafka) |
| :--- | :--- | :--- |
| **Read Mechanism** | Destructive pop (`ack` deletes message) | Non-destructive offset read |
| **Multiple Consumers** | Competing consumers (divide work) | Independent Consumer Groups (broadcast/fanout) |
| **Replay** | Impossible (messages are deleted) | Trivial (rewind consumer offset) |
| **Ordering** | FIFO queue head only | Strict partition-scoped ordering |
| **Throughput** | 10k - 50k msgs/sec | 500k - 2M+ msgs/sec (via batching & page cache) |
| **Task Granularity** | Per-message ack and routing | Batch-level commits and partition-level locks |

## Mental model
```text
Work Queue (RabbitMQ / SQS):
[ Msg 1 | Msg 2 | Msg 3 ] ──► Worker A pops Msg 1 (DELETED!)
                          ──► Worker B pops Msg 2 (DELETED!)

Append-Only Log (Kafka):
[ Evt 1 | Evt 2 | Evt 3 ] ──► Service A reads Evt 1, 2, 3 (Track offset)
                          ──► Service B reads Evt 1, 2, 3 (Track offset)
                          ──► Auditor replays Evt 1, 2, 3 next week!
```

## Build it
See [queue_vs_log_comparison.py](../code/queue_vs_log_comparison.py).
We contrast destructive pop vs offset tracking in Python.

## Use Kafka
Demonstrate multiple consumer groups reading the same records simultaneously without interference.

## Inspect it
Observe that after consumer A finishes reading all records, consumer B can still read 100% of those records from offset 0.

## Measure it
Compare consumer memory usage between in-memory message queues and Kafka offset pointers.

## Break it
Try to ack individual messages out of order in Kafka; discover that Kafka can only commit sequential offsets up to the highest processed point!

## Recover it
Use application-level deduplication or out-of-order trackers.

## Modify it
Write an architectural decision record (ADR) comparing Kafka vs SQS for a background email sending service.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does a traditional queue struggle to support 10 independent downstream consumer services?
2. If your workload involves long-running, CPU-intensive tasks (e.g. 10 minutes per PDF render), why is a traditional work queue usually a better fit than Kafka?

## Guarantees
* Kafka guarantees non-destructive reads across multiple consumer groups.

## Non-guarantees
* Kafka does not support selective per-message acknowledgments (e.g. acknowledging message #5 while leaving message #4 unacknowledged).

## When to use this
* Architectural technology selection and system design interviews.

## When not to use this
* Blindly replacing existing task queues with Kafka without evaluating partition concurrency limits.

## What comes next
In Phase 42, we demonstrate Multiple Consumer Groups and fan-out architecture in practice.
