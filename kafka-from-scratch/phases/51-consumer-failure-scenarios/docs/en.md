# Lesson 51: Consumer Failure Scenarios

## Motto
"A dead consumer is easy to spot; a slow consumer that starves its peers is insidious."

## Problem
What goes wrong inside consumer groups during production incidents?
1. **Crash before commit:** Causes duplicate processing upon restart.
2. **Crash after commit:** Causes lost events if external database write failed.
3. **Slow processing deadlock:** A thread hangs on a database lock for 6 minutes. Because `max.poll.interval.ms` (5 min) expires, the coordinator evicts the consumer, triggering a stop-the-world rebalance!
How do you diagnose and recover from these consumer failure modes?

## Prediction
What happens to partition assignments across a consumer group when one consumer thread hangs?

## Why this matters
Diagnosing slow consumers, rebalance storms, and offset commit failures is the primary operational skill required for streaming engineers.

## Mental model
```text
The Slow Consumer Death Spiral:
1. Consumer 1 encounters slow 6-minute external database lock.
2. Poll loop fails to invoke poll() within max.poll.interval.ms (5 min).
3. Broker Coordinator assumes Consumer 1 died -> TRIGGERS REBALANCE!
4. Consumer 1's partitions revoked and handed to Consumer 2.
5. Consumer 2 encounters the exact same slow DB lock!
6. Consumer 2 also times out -> TRIGGERS ANOTHER REBALANCE!
Result: Cluster rebalance storm! Entire consumer group grinds to a halt!
```

## Build it
See [chaos_consumer_failure.py](../code/chaos_consumer_failure.py).
We simulate slow consumer poll timeouts and diagnose rebalance events.

## Use Kafka
Inspect consumer group status under failure using `kafka-consumer-groups.sh`.

## Inspect it
Observe `CommitFailedException` in consumer logs.

## Measure it
Measure consumer lag accumulation during a rebalance storm.

## Break it
Simulate a 60-second processing block when `max.poll.interval.ms=30000`.

## Recover it
Offload heavy processing to worker thread pools; keep Kafka consumer loop dedicated exclusively to polling and heartbeating.

## Modify it
Tune `max.poll.records` to a smaller batch size (e.g. 50 records) so batches finish well within timeouts.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does offloading processing to a worker thread pool solve `max.poll.interval.ms` timeouts but complicate manual offset committing?
2. What is the difference between `session.timeout.ms` and `max.poll.interval.ms`?

## Guarantees
* The group coordinator automatically evicts dead or non-responsive consumers.

## Non-guarantees
* The coordinator cannot distinguish between a consumer that is dead and a consumer that is stalled on a slow database query.

## When to use this
* Consumer group stability tuning and rebalance debugging.

## When not to use this
* Setting `max.poll.interval.ms` to hours to paper over broken consumer application code.

## What comes next
In Phase 52, we study Producer Failure Scenarios and error handling.
