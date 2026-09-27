# Lesson 05: Topics

## Motto
"A topic is a named logical stream; multiplexing unrelated events into a single log creates chaos."

## Problem
In any real company, different business events occur simultaneously:
* User clicks (`pageviews`)
* Financial transactions (`payments`)
* Security logins (`auth_events`)
If all of these events are dumped into a single log file, every consumer must read and discard 95% of records they don't care about, wasting CPU, network, and disk I/O.
How do we organize events into discrete, isolated logical streams?

## Prediction
If topic `payments` has 10 records and topic `pageviews` has 10,000 records, should their offset sequences interfere with each other?

## Why this matters
In Kafka, a **Topic** is the primary organizational unit. It represents a named stream of records. Crucially, **each topic maintains its own independent offset space**.

## Mental model
```text
Broker Storage Root (/tmp/kafka-logs)
├── Topic: "orders"
│   └── mini_log_orders.dat   --> Offsets: 0, 1, 2, 3
├── Topic: "payments"
│   └── mini_log_payments.dat --> Offsets: 0, 1, 2
└── Topic: "notifications"
    └── mini_log_notifications.dat --> Offsets: 0, 1, 2, 3, 4, 5
```

## Build it
See [topic_log_manager.py](../code/topic_log_manager.py).
We implement a `TopicManager` that dynamically provisions independent `MiniLog` instances keyed by topic name.

## Use Kafka
Create and list topics on the real Kafka broker:
```bash
docker exec -it kafka-lab-single /opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic orders --partitions 1 --replication-factor 1
docker exec -it kafka-lab-single /opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --list
```

## Inspect it
Observe how appending to `orders` does not advance the offset of `payments`.

## Measure it
Compare consumer processing time when filtering events from a shared log vs reading from dedicated topics.

## Break it
Attempt to write to a non-existent topic when auto-topic creation is disabled.

## Recover it
Explicitly create the topic using administrative commands.

## Modify it
Implement topic deletion in `TopicManager` and observe disk cleanup.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does having separate topics eliminate consumer-side filtering overhead?
2. Why should production Kafka clusters disable `auto.create.topics.enable`?

## Guarantees
* Topics have completely independent offset spaces and physical files.

## Non-guarantees
* A topic alone does not provide horizontal scale across multiple servers; that requires partitions (Phase 07).

## When to use this
* Organizing discrete event types across business domains.

## When not to use this
* Creating a dynamic topic per user (e.g. `user-topic-1234`)—this creates thousands of tiny files and crashes broker OS file handles.

## What comes next
In Phase 06, we transition from our Python prototype to writing real Kafka producers and consumers with official client libraries.
