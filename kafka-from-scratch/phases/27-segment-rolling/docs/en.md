# Lesson 27: Segment Rolling

## Motto
"Close the old segment, seal it immutable, and open the new."

## Problem
A single partition log cannot grow as one infinite file.
If it did:
* Log compaction would have to scan the entire historical universe.
* Old data could not be pruned by retention without rewriting the file.
How does Kafka slice an infinite stream of records into manageable, immutable files on disk?

## Prediction
When an active segment file reaches its configured size limit (`segment.bytes`), what does Kafka do with the current `.log` file and the next incoming write?

## Why this matters
**Segment Rolling is the mechanism that transitions data from mutable append state to immutable historical storage.**
Understanding segment roll triggers (`segment.bytes` and `segment.ms`) is critical for log compaction and retention policies.

## First principles
* **Active Segment:** The single segment currently receiving appends.
* **Rolling Triggers:**
  * Size threshold reached: `segment.bytes` (default: 1 GB).
  * Time threshold reached: `segment.ms` (default: 7 days).
  * Index threshold reached: `segment.index.bytes` (default: 10 MB).
* When a roll occurs, the current segment is flushed and sealed read-only. A new active segment is created named after the next offset.

## Mental model
```text
Step 1: Active Segment (0000.log) reaches 10 KB limit
Step 2: Roll triggered!
        - 00000000000000000000.log SEALED IMMUTABLE
        - 00000000000000000000.index SEALED IMMUTABLE
Step 3: New Active Segment opened:
        - 00000000000000000150.log (Base offset: 150)
```

## Build it
See [segment_rolling_lab.py](../code/segment_rolling_lab.py).
We configure a topic with a tiny `segment.bytes=10240` (10 KB) and produce records to trigger segment rolls.

## Use Kafka
Create a topic with a 10KB segment limit:
```bash
docker exec -it kafka-lab-single /opt/kafka/bin/kafka-topics.sh   --bootstrap-server localhost:9092   --create --topic rolling-lab   --partitions 1 --replication-factor 1   --config segment.bytes=10240
```

## Inspect it
List the partition directory inside the container and observe multiple `.log` and `.index` segment pairs:
```bash
docker exec -it kafka-lab-single ls -la /tmp/kraft-combined-logs/rolling-lab-0/
```

## Measure it
Measure the exact byte size of sealed segments.

## Break it
Configure `segment.bytes` excessively small (e.g. 100 bytes) and observe the broker create thousands of tiny file descriptors, exhausting OS limits!

## Recover it
Restore sensible segment sizes (typically 100MB to 1GB in production).

## Modify it
Test time-based segment rolling using `segment.ms`.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why are historical (non-active) segment files immutable?
2. What naming convention does Kafka use for segment files, and why?

## Guarantees
* Sealed segments are guaranteed to never be modified by incoming producer appends.

## Non-guarantees
* Segment rolls do not happen at exact byte boundaries; Kafka rolls when the current batch exceeds the limit.

## When to use this
* Sizing segment files for log compaction and retention tuning.

## When not to use this
* Never configure microscopic segment sizes in production.

## What comes next
In Phase 28, we explore Retention policies and learn how Kafka safely purges expired segments.
