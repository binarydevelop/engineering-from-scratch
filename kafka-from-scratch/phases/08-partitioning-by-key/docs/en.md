# Lesson 08: Partitioning by Key

## Motto
"The key determines the partition; same key equals same partition equals preserved ordering."

## Problem
In Phase 07, we saw that multiple partitions increase throughput, but total topic-wide ordering is lost.
What if your application requires strict ordering for specific entities?
For example, in banking, all transactions for `account-42` must be processed in exact chronological order (`deposit` before `withdrawal`).
How can we preserve per-entity ordering while still enjoying multi-partition throughput?

## Prediction
If you produce 100 messages with key `user-42` to a 5-partition topic, how many different partitions will receive those messages?

## Why this matters
Keys enable **deterministic routing**. All records sharing the same key are routed to the exact same partition, guaranteeing chronological processing order for that entity.

## Mental model
```text
Record Key: "user-42"
       │
       ▼
Murmur2 Hash / CRC32 Hash:  hash("user-42") = 0x8F14B2C1 (Integer: 2400490177)
       │
       ▼
Modulo Partition Count:      2400490177 % 3 Partitions = Partition 1
       │
       ▼
Guaranteed Destination:      Partition 1 (ALWAYS, as long as partition count is constant!)
```

## Build it
See [key_partitioning.py](../code/key_partitioning.py).
We test hashing algorithms and observe key-to-partition mapping.

## Use Kafka
Produce records with keys and inspect which partition they land on.

## Inspect it
Use `kafka-console-consumer.sh` with `--property print.partition=true` to verify partition mapping.

## Measure it
Measure distribution uniformity when using UUID keys vs sequential keys.

## Break it
Increase the partition count of the topic from 3 to 5 halfway through producing, and observe how `hash(key) % N` changes destination partitions, breaking ordering!

## Recover it
Never resize partitions dynamically if strict key-to-partition consistency across historical data is required without a re-keying migration plan.

## Modify it
Implement a custom partitioner that sends all VIP customers (`vip-*`) to a dedicated partition.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does altering the partition count of an existing topic break the key-to-partition mapping?
2. What partition routing strategy does Kafka use when the record key is `null`?

## Guarantees
* Records with the same non-null key always map to the same partition, provided partition count remains unchanged.

## Non-guarantees
* Key-based routing does NOT guarantee even distribution if the keys themselves are skewed.

## When to use this
* Whenever per-entity ordering matters (e.g. per user, per order, per IoT device).

## When not to use this
* When events have no natural entity identifier, or when keys would cause massive partition skew (Phase 09).

## What comes next
In Phase 09, we examine what happens when key distribution is skewed: Hot Partitions.
