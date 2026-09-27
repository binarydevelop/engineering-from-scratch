# Lesson 11: Consumer Parallelism Limits

## Motto
"You cannot have more active workers in a group than you have partitions in the topic."

## Problem
A junior engineer notices that consumer lag is accumulating on an `orders` topic.
The topic has **3 partitions**.
In an attempt to speed up consumption, they deploy **10 consumer pods** on Kubernetes.
To their bewilderment, consumer throughput does not increase by a single record.
Why?

## Prediction
If a topic has 3 partitions and 5 consumers join the group, what will the 4th and 5th consumers do?

## Why this matters
This is one of the most common capacity-planning mistakes in production.
$$\text{Max Active Parallelism in a Group} = \text{Number of Partitions}$$
Any consumers beyond the partition count sit 100% idle.

## Mental model
```text
Topic: 3 Partitions [ P0, P1, P2 ]
Consumer Group: 5 Consumer Pods

P0 ──► Consumer 1 (ACTIVE)
P1 ──► Consumer 2 (ACTIVE)
P2 ──► Consumer 3 (ACTIVE)
       Consumer 4 (IDLE - 0 Partitions Assigned)
       Consumer 5 (IDLE - 0 Partitions Assigned)
```

## Build it
See [parallelism_limits.py](../code/parallelism_limits.py).
We test partition assignment when $Consumers > Partitions$.

## Use Kafka
Start 5 consumer processes in the same group against a 3-partition topic and inspect them with `kafka-consumer-groups.sh`.

## Inspect it
Observe that 2 consumers report `PARTITION: -` and `CURRENT-OFFSET: -`.

## Measure it
Measure CPU utilization of the idle consumer processes.

## Break it
Kill one of the active consumers (e.g. Consumer 1) and watch an idle consumer instantly get assigned the orphaned partition!

## Recover it
Idle consumers serve as automatic hot-standbys for failover.

## Modify it
Increase partition count to 5 using `kafka-topics.sh --alter --partitions 5` and watch the 2 idle consumers immediately activate.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does Kafka make idle consumers hot-standbys rather than allowing multiple consumers to share a single partition?
2. If you need 50 parallel consumer threads, how many partitions must the topic have?

## Guarantees
* Active consumers within a group never exceed the partition count.

## Non-guarantees
* Adding consumers beyond the partition count will not reduce lag.

## When to use this
* Capacity planning and autoscaling configuration (HPA on Kubernetes).

## When not to use this
* Over-provisioning consumer replicas beyond partition count wastes memory and CPU.

## What comes next
In Phase 12, we study the mechanics of Consumer Rebalancing when members join or die.
