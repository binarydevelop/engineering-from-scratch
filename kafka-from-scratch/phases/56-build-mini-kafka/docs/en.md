# Lesson 56: Capstone 1 — Build Mini Kafka

## Motto
"What I cannot create, I do not understand." — Richard Feynman

## Problem
You have studied the individual components of Apache Kafka: topics, partitions, append-only logs, monotonic offsets, consumer groups, range assignment, and offset commits.
Now, bring them all together into a functioning, self-contained educational Kafka-like system in pure Python.

## Prediction
Can you build a functional distributed log with topics, partitions, and consumer groups in under 300 lines of pure Python?

## Why this matters
Building Mini-Kafka cements every abstract concept into concrete data structures: dictionaries of topics, arrays of partition logs, monotonic integer counters, and consumer group offset mappings.

## First principles
* **MiniBroker:** Manages a dictionary of Topics.
* **Topic:** Comprises $N$ Partitions.
* **Partition:** Manages an immutable append-only disk log file with local offset sequence.
* **Consumer Group:** Enforces that each partition is assigned to at most one worker, and tracks committed offsets per partition.

## Mental model
```text
MiniKafkaBroker
├── Topic: "orders"
│   ├── Partition 0: [ Offsets: 0, 1, 2 ] (mini_kafka_data/orders-0.log)
│   └── Partition 1: [ Offsets: 0, 1 ]    (mini_kafka_data/orders-1.log)
└── Consumer Groups Registry:
    └── Group "fulfillment":
        ├── Assigned Partitions: { "Worker-1": [0], "Worker-2": [1] }
        └── Committed Offsets:   { 0: 2, 1: 1 }
```

## Build it
See [mini_kafka.py](../code/mini_kafka.py).
We build the complete broker, producer, and consumer group engine.

## Use Kafka
Run the test suite verifying produce, consume, consumer group assignment, and offset persistence.

## Inspect it
Check the on-disk binary logs written by MiniKafka in `/tmp/mini_kafka_data`.

## Measure it
Measure append throughput of our pure Python implementation.

## Break it
Simulate worker failure and observe partition reassignment.

## Recover it
Restart the broker and verify historical state is restored from disk.

## Modify it
Add basic replication across two simulated MiniBroker instances.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. How does your MiniKafka broker ensure thread-safety during concurrent appends to different partitions?
2. What are the key differences between your MiniKafka implementation and Apache Kafka 3.8.0?

## Guarantees
* Fully functional educational subset of Kafka core mechanics.

## Non-guarantees
* Does not implement the real binary Kafka wire protocol.

## When to use this
* As the foundational educational artifact of this curriculum.

## When not to use this
* MiniKafka is an educational tool; never use it in production.

## What comes next
In Phase 57, we tackle Capstone 2: Building a resilient Event-Driven Application on real Kafka.
