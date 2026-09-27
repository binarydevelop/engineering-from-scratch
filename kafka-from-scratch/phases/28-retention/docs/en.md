# Lesson 28: Retention

## Motto
"Consumers read; retention deletes. The two mechanisms are completely independent."

## Problem
In a message queue (e.g. RabbitMQ or SQS), once a consumer reads and acknowledges a message, the broker destructively deletes it.
In Kafka:
* 10 different consumer groups can read the same records.
* Consumers can crash, restart, and replay records from 3 days ago.
If reading does not delete records, how does Kafka prevent disk storage from filling up and halting the cluster?

## Prediction
If a consumer has NOT yet read record at offset 50, but that record's segment exceeds the retention time limit, will Kafka delete the segment anyway?

## Why this matters
**Kafka decouples consumption from deletion.** Retention is governed strictly by time or storage size, completely independent of consumer positions. If a consumer lags beyond the retention window, it will lose data!

## First principles
* **Time-based Retention:** `retention.ms` or `log.retention.hours` (default: 7 days). Segments whose newest timestamp is older than this threshold are deleted.
* **Size-based Retention:** `retention.bytes` or `log.retention.bytes`. Total bytes per partition.
* **Segment-Level Deletion:** Kafka does *not* delete individual records. It deletes entire sealed segment files during background cleaner runs.
* **Active Segment Immunity:** The active segment is NEVER deleted, even if it exceeds retention limits.

## Mental model
```text
Partition Directory:
Segment 1 (0000.log) [Age: 10 days] ──► ELIGIBLE FOR DELETION! (Background thread deletes file)
Segment 2 (1000.log) [Age: 3 days]  ──► RETAINED (Within 7-day retention)
Segment 3 (2000.log) [Active]        ──► IMMUNE TO DELETION (Currently accepting writes)
```

## Build it
See [retention_lab.py](../code/retention_lab.py).
We configure a topic with a 5-second retention window and observe background segment deletion.

## Use Kafka
Set aggressive retention on a topic:
```bash
docker exec -it kafka-lab-single /opt/kafka/bin/kafka-topics.sh   --bootstrap-server localhost:9092   --create --topic retention-lab   --partitions 1 --replication-factor 1   --config segment.bytes=10240   --config retention.ms=5000
```

## Inspect it
Watch sealed segments disappear from the filesystem after 5 seconds while the active segment remains.

## Measure it
Measure reclaimed disk space after segment deletion.

## Break it
Simulate a slow consumer that falls behind retention; observe the consumer throw `OffsetOutOfRangeException`.

## Recover it
Handle `OffsetOutOfRangeException` by resetting consumer offset to `earliest`.

## Modify it
Configure size-based retention (`retention.bytes`) and verify behavior.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does Kafka delete entire segments rather than deleting individual expired records from within a file?
2. What is the operational risk if consumer lag exceeds topic retention time?

## Guarantees
* Data is retained up to the configured time or size boundary.

## Non-guarantees
* Kafka does not guarantee lagging consumers will finish reading before retention purges data.

## When to use this
* In all Kafka topics to bound disk consumption.

## When not to use this
* Do not set retention shorter than the maximum expected consumer recovery SLA.

## What comes next
In Phase 29, we examine Log Compaction: retaining the latest value per key rather than deleting by age.
