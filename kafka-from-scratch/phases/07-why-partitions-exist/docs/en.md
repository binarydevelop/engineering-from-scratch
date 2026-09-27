# Lesson 07: Why Partitions Exist

## Motto
"A single log is bound to a single disk and a single thread; partitions are Kafka's unit of scalability."

## Problem
Imagine a high-traffic topic receiving 500,000 events/second (e.g. ad impressions or clickstreams).
If a topic consists of only a single append-only log file:
1. **Disk I/O Bottleneck:** A single log file can only reside on a single disk on a single broker machine.
2. **Network Bottleneck:** All traffic must enter through one network interface card (NIC).
3. **Consumer Bottleneck:** A single log cannot be safely consumed in parallel without complex locking.
How can a single logical topic scale horizontally across 10, 50, or 100 machines?

## Prediction
Can Kafka provide total ordering across all messages in a topic that has 10 partitions?

## Why this matters
**Partitions are the fundamental unit of parallelism, storage, and ordering in Kafka.**
Understanding that:
$$\text{Total Ordering} = \text{Partition-Scoped Only}$$
is the single most important mental leap in Kafka architecture.

## Mental model
```text
Topic: "user-clicks" (Divided into 3 Partitions)

Partition 0: [ 0 | 1 | 2 | 3 | 4 ]  ──► Stored on Broker 1 (Disk A)
Partition 1: [ 0 | 1 | 2 | 3 ]      ──► Stored on Broker 2 (Disk B)
Partition 2: [ 0 | 1 | 2 | 3 | 4 | 5]──► Stored on Broker 3 (Disk C)
```

## Build it
See [partitioned_log_sim.py](../code/partitioned_log_sim.py).
We implement a multi-partition log simulation that round-robins writes across multiple independent logs and demonstrates partition-local offset counting.

## Use Kafka
Create a topic with 3 partitions and produce records:
```bash
docker exec -it kafka-lab-single /opt/kafka/bin/kafka-topics.sh   --bootstrap-server localhost:9092   --create --topic multi-partition-topic --partitions 3 --replication-factor 1
```

## Inspect it
Inspect the partition distribution with `kafka-topics.sh --describe`.

## Measure it
Measure write throughput of 1 partition vs. 3 partitions.

## Break it
Assume that offset 4 in Partition 0 occurred "before" offset 3 in Partition 1; observe why timestamps, not offsets, must be used to compare across partitions.

## Recover it
Align partition keys so causally related events always land in the same partition.

## Modify it
Scale the topic partition count from 3 to 6 using `kafka-topics.sh --alter --partitions 6`.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does each partition have its own independent offset sequence starting from 0?
2. Why does Kafka NOT guarantee total global ordering across an entire topic?

## Guarantees
* Strict, deterministic ordering is guaranteed within any single partition.

## Non-guarantees
* No ordering guarantees exist between different partitions of the same topic.

## When to use this
* Always! Virtually every production Kafka topic uses multiple partitions.

## When not to use this
* Topics that strictly require global FIFO ordering across all events must use exactly 1 partition (and accept the throughput bottleneck).

## What comes next
In Phase 08, we learn how to control which record goes to which partition using Keys.
