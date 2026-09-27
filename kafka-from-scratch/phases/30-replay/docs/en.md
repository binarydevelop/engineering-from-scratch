# Lesson 30: Replay

## Motto
"The superpower of an immutable log is the ability to travel backward in time."

## Problem
Your team deploys a critical bug in the payment reconciliation service at 9:00 AM.
For 4 hours, it miscalculated foreign exchange conversions on 100,000 transactions.
At 1:00 PM, the bug is identified and fixed.
In a traditional queue or direct HTTP architecture, those 100,000 requests are gone forever; recovering requires manual database surgery.
In Kafka:
* The 100,000 original events are still sitting immutably in the log!
How do you rewind the consumer group and recalculate the state correctly?

## Prediction
What happens to consumer group offset tracking when you execute `kafka-consumer-groups.sh --reset-offsets --to-earliest`?

## Why this matters
**Historical replay is Kafka's defining operational advantage over traditional message brokers.**
It enables zero-downtime state reconstruction, bug recovery, analytics backfills, and database re-indexing.

## First principles
* **Offset Rewind:** A consumer group's position in `__consumer_offsets` is simply an integer pointer. Resetting it to 0 instructs Kafka to re-serve historical records from the beginning.
* **Deterministic Event Sourcing:** If events are immutable, replaying them through deterministic logic recreates the exact state.
* **The Dangers of Replay:** Replaying events that trigger *external side effects* (e.g. sending real emails or charging Stripe credit cards) will duplicate real-world actions unless guarded by idempotency!

## Mental model
```text
T0: Buggy Consumer processes offsets 0 -> 1000 (Saved incorrect state)
T1: Fix deployed to consumer application
T2: Execute Offset Reset: Reset Group "reconcile-svc" offset -> 0
T3: Consumer restarts, re-reads offsets 0 -> 1000 from log
Result: Clean, 100% accurate recalculated state!
```

## Build it
See [replay_lab.py](../code/replay_lab.py).
We process events into a bank balance, simulate a corrupting calculation bug, reset offsets, and rebuild the correct balance from scratch.

## Use Kafka
Reset a consumer group's offset using official CLI:
```bash
docker exec -it kafka-lab-single /opt/kafka/bin/kafka-consumer-groups.sh   --bootstrap-server localhost:9092   --group bank-reconciliation-group   --reset-offsets --to-earliest   --topic bank-txns   --execute
```

## Inspect it
Observe `CURRENT-OFFSET` reset to 0 in `kafka-consumer-groups.sh --describe`.

## Measure it
Measure replay processing throughput (typically 10x-50x faster than real-time because records are pre-buffered).

## Break it
Replay a topic into a non-idempotent notification service and watch users receive duplicate push notifications!

## Recover it
Always isolate replay environments or guard side-effecting external adapters with idempotency keys.

## Modify it
Reset offsets to a specific timestamp (`--to-datetime 2026-09-23T10:00:00.000`) rather than the earliest offset.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does replay require downstream consumers to be idempotent?
2. How does log retention limit how far back in time a consumer can replay?

## Guarantees
* Kafka serves historical records in the exact original sequence stored in each partition.

## Non-guarantees
* Kafka cannot replay records that have already been purged by retention or compaction.

## When to use this
* Rebuilding read-model caches, fixing software bugs, training machine learning models, audit compliance.

## When not to use this
* Uncontrolled replays directly against non-idempotent third-party APIs.

## What comes next
In Phase 31, we enter Module 7 and study Consumer Lag and Backpressure mechanics.
