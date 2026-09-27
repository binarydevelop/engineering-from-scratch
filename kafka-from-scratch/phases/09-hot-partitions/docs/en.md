# Lesson 09: Hot Partitions

## Motto
"Having 100 partitions does not save you if 90% of your events carry the exact same key."

## Problem
An e-commerce platform keys all events by `merchant_id`.
99% of merchants are small mom-and-pop sellers with 5 orders/day.
One merchant is a global megastore (e.g. Amazon or Nike) generating 200,000 orders/minute.
What happens to the Kafka cluster?
The single partition mapped to that one giant merchant receives 95% of all traffic, saturating its broker's CPU and disk, while the remaining 31 partitions sit virtually idle.
This is a **Hot Partition**.

## Prediction
If one partition receives 10x more writes than others, can scaling consumer instances in a consumer group alleviate the bottleneck?

## Why this matters
Partitioning only scales horizontally if the key distribution is balanced. Key design is a critical system design responsibility.

## Mental model
```text
Topic: 4 Partitions (Skewed Workload)
Partition 0: [ Megastore orders... (90% of all data) ]  <-- HOT PARTITION (CPU 99%, Disk Bottleneck)
Partition 1: [ Small store A ]                          <-- IDLE
Partition 2: [ Small store B ]                          <-- IDLE
Partition 3: [ Small store C ]                          <-- IDLE
```

## Build it
See [hot_partition_analyzer.py](../code/hot_partition_analyzer.py).
We generate skewed workloads and calculate coefficient of variation ($CV$) across partitions.

## Use Kafka
Produce a skewed dataset to Kafka and analyze partition offsets.

## Inspect it
Check partition offset deltas using `kafka-consumer-groups.sh` or topic partition describe tools.

## Measure it
Measure latency and disk byte distribution across partitions under skewed keys.

## Break it
Send 99% of messages with key `"system"` and watch Partition 0 queue depth explode while Partition 1 and 2 remain empty.

## Recover it
Implement **Salted Keys** (e.g. `"merchant_id:salt_0"`, `"merchant_id:salt_1"`) to scatter the hot entity across multiple partitions when strict global per-entity order is not required.

## Modify it
Add salting to the hot key and measure the restoration of workload balance.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does consumer scaling fail to solve a hot partition bottleneck?
2. What are the trade-offs of key salting regarding per-entity event ordering?

## Guarantees
* The partitioner strictly follows its hashing algorithm.

## Non-guarantees
* Kafka does not automatically detect or rebalance hot partitions at runtime.

## When to use this
* During capacity planning, key schema design, and partition skew debugging.

## When not to use this
* Premature key salting when per-entity ordering is mandatory and throughput fits comfortably within a single partition's capacity.

## What comes next
In Phase 10, we build Consumer Groups from first principles to distribute partition workloads across multiple workers.
