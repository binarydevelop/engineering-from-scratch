# Lesson 42: Multiple Consumer Groups

## Motto
"One write, infinite independent readers; the ultimate decoupling engine."

## Problem
In a monolithic system, when an order is placed:
The code calls `payment()`, then `email()`, then `inventory()`, then `analytics()`.
When Marketing wants to add a new `loyalty_points()` system, the core checkout codebase must be touched, tested, and redeployed.
How does Kafka allow any number of independent teams to consume the `orders` stream without the checkout team ever knowing or caring?

## Prediction
If Group A commits offset 100 on Partition 0, what is Group B's offset on Partition 0?

## Why this matters
**Multiple Consumer Groups provide true organizational decoupling.**
Teams can build, deploy, scale, and crash their services independently without affecting any other team's consumption progress.

## Mental model
```text
Topic: "orders" (Partition 0)
Offsets: 0 ── 1 ── 2 ── 3 ── 4 ── 5 ── 6 (LEO)

Group 1: "payment-service"      ──► Offset 6 (Real-time, caught up!)
Group 2: "email-notifications"  ──► Offset 4 (Slightly lagging)
Group 3: "data-warehouse-etl"   ──► Offset 1 (Batching 10,000 records/hr)
Group 4: "new-loyalty-service"  ──► Offset 0 (Newly deployed! Replaying from beginning!)
```

## Build it
See [multi_group_fanout.py](../code/multi_group_fanout.py).
We launch three independent consumer groups against a single producer topic and verify independent offset tracking.

## Use Kafka
Run multiple consumers specifying different `--group` IDs:
```bash
# Group 1: fraud-service
docker exec -it kafka-lab-single /opt/kafka/bin/kafka-console-consumer.sh   --bootstrap-server localhost:9092 --topic multi-fanout-orders --group fraud-service

# Group 2: email-service
docker exec -it kafka-lab-single /opt/kafka/bin/kafka-console-consumer.sh   --bootstrap-server localhost:9092 --topic multi-fanout-orders --group email-service
```

## Inspect it
Describe both groups and observe completely independent `CURRENT-OFFSET` values:
```bash
docker exec -it kafka-lab-single /opt/kafka/bin/kafka-consumer-groups.sh   --bootstrap-server localhost:9092 --describe --group fraud-service
```

## Measure it
Measure broker CPU and memory impact when adding 5 additional consumer groups (virtually zero, thanks to page cache sharing!).

## Break it
Crash Group 2 (Email Service); observe that Group 1 (Fraud Service) continues processing without experiencing a single millisecond of disruption!

## Recover it
Restart Group 2; it resumes from its own saved offset and catches up.

## Modify it
Deploy a new Group 4 that starts from `earliest` to backfill historical analytics.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does having 10 consumer groups reading the same partition NOT multiply disk reads by 10x? (Hint: OS Page Cache).
2. How does independent consumer group offset storage prevent cross-team cascading outages?

## Guarantees
* Each consumer group maintains completely isolated, independent offset pointers.

## Non-guarantees
* A crashing consumer group does not affect other groups, but it will accumulate lag on disk.

## When to use this
* In every microservice architecture with multiple downstream consumers.

## When not to use this
* When workers are cooperating on the exact same task (use the *same* consumer group ID to divide work).

## What comes next
In Phase 43, we enter Module 9 and study Resilience Patterns: In-Process Retries vs Retry Topics.
