# Lesson 40: Time in Kafka

## Motto
"There is the time an event happened, the time Kafka wrote it, and the time you read it; never confuse the three."

## Problem
In distributed systems, clocks skew, consumers lag, and historical replays occur.
Consider three different timestamps for a single event:
1. `10:00:00 AM` — Sensor detects engine overheating in a car.
2. `10:05:00 AM` — Car re-enters cellular coverage; producer appends record to Kafka broker.
3. `02:00:00 PM` — Analytics consumer wakes up and processes the record.
If the analytics service alerts on "events that happened in the last 15 minutes" using `time.now()`, it alerts 4 hours late!
Which timestamp should you use?

## Prediction
What is the difference between `CreateTime` and `LogAppendTime` in Kafka topic configurations?

## Why this matters
**Time is the trickiest variable in stream processing.**
Confusing Event Time with Processing Time causes incorrect financial calculations, broken window aggregations, and invalid alerting.

## First principles
* **Event Time (`CreateTime`):** The timestamp set by the producer application when the real-world event occurred (`message.timestamp.type=CreateTime`, the default).
* **Log Append Time (`LogAppendTime`):** The timestamp assigned by the broker when it writes the record to its local log.
* **Processing Time:** The clock time of the consumer machine executing business logic.

## Mental model
```text
Event Occurs: 10:00:00 AM (Event Time / CreateTime)
      │
      ▼ (5 minute network/cellular delay)
Broker Writes: 10:05:00 AM (LogAppendTime)
      │
      ▼ (4 hours in retention buffer / consumer lag)
Consumer Reads: 02:00:00 PM (Processing Time)
```

## Build it
See [time_semantics_lab.py](../code/time_semantics_lab.py).
We inspect the differences between event timestamps and consumer processing timestamps.

## Use Kafka
Set `message.timestamp.type=LogAppendTime` on a topic and observe broker-assigned timestamps.

## Inspect it
Use `kafka-console-consumer.sh --property print.timestamp=true` to inspect record timestamps.

## Measure it
Measure the delta between `CreateTime` and `System.currentTimeMillis()` at consumption.

## Break it
Simulate a producer with an incorrectly configured system clock set to year 2035; observe how time-based retention misbehaves!

## Recover it
Synchronize server clocks using NTP (Network Time Protocol) or enforce `LogAppendTime`.

## Modify it
Query Kafka offsets by timestamp using `consumer.offsets_for_times()`.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does out-of-order stream processing require algorithms to operate on Event Time rather than Processing Time?
2. What happens to time-based retention if records are produced with timestamps far in the past or future?

## Guarantees
* Kafka preserves the 64-bit millisecond timestamp attached to each record batch.

## Non-guarantees
* Kafka does not validate whether producer clocks are synchronized with real UTC time.

## When to use this
* Windowed streaming aggregations, time-series telemetry, and historical replay.

## When not to use this
* Relying on `CreateTime` without NTP clock synchronization across producer servers.

## What comes next
In Phase 41, we contrast Kafka with traditional Message Queues (RabbitMQ, SQS).
