# Lesson 12: Consumer Rebalancing

## Motto
"When membership changes, partitions must be redistributed; how gracefully that happens defines availability."

## Problem
In a dynamic cluster, consumers crash, deploy new code, or scale up with traffic.
When a consumer dies or joins, who decides which partitions move to which workers?
How does the cluster prevent two consumers from simultaneously reading and committing the same partition during a transition?
This coordination protocol is called a **Consumer Rebalance**.

## Prediction
What happens to active message consumption during an "eager" stop-the-world rebalance?

## Why this matters
Rebalance storms can stall consumption for seconds or minutes. Understanding heartbeat threads, `session.timeout.ms`, and rebalance assignors is essential for production stability.

## First principles
* **Group Coordinator:** One Kafka broker is elected to coordinate the group (determined by hashing group ID into `__consumer_offsets`).
* **Heartbeats:** Consumers send background heartbeats to the coordinator. If heartbeats cease for `session.timeout.ms`, the consumer is evicted.
* **JoinGroup & SyncGroup:** Consumers rejoin, a group leader computes the assignment, and the coordinator broadcasts it.

## Mental model
```text
Timeline of a Consumer Rebalance (Eager / Stop-the-World)
T0: Consumer 1 and Consumer 2 reading normally
T1: Consumer 3 sends JoinGroup request (Scaling up)
T2: Coordinator signals REBALANCE_IN_PROGRESS on next heartbeat
T3: ALL consumers pause consumption and revoke current partitions (STOP-THE-WORLD)
T4: Group leader computes new assignment
T5: Coordinator distributes SyncGroup response
T6: Consumers resume consumption on newly assigned partitions
```

## Build it
See [rebalance_observer.py](../code/rebalance_observer.py).
We implement a consumer with a `ConsumerRebalanceListener` that tracks partition assignment and revocation callbacks.

## Use Kafka
Run multiple consumers, then terminate one with SIGTERM and watch the remaining consumer rebalance.

## Inspect it
Observe the rebalance events printed in consumer console logs.

## Measure it
Measure the duration from SIGTERM until partition reassignment completes.

## Break it
Simulate a slow consumer that blocks the poll thread longer than `max.poll.interval.ms` and observe the coordinator evicting it.

## Recover it
Ensure long processing is offloaded to worker threads so `poll()` is invoked regularly.

## Modify it
Configure Cooperative Sticky Assignor (`CooperativeStickyAssignor`) to avoid stop-the-world pauses.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. What is the difference between `session.timeout.ms` and `max.poll.interval.ms`?
2. How does Cooperative Sticky Rebalancing improve upon classic Eager Rebalancing?

## Guarantees
* After rebalance completes, each partition is assigned to exactly one active group member.

## Non-guarantees
* During an eager rebalance, active consumption is paused across the group.

## When to use this
* Monitoring consumer group stability and sizing poll interval parameters.

## When not to use this
* Avoid triggering rebalances unnecessarily through poor timeout configuration.

## What comes next
In Phase 13, we examine Offset Commits and explore how commit timing dictates delivery guarantees.
