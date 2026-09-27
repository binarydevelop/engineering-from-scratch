# Lesson 29: Log Compaction

## Motto
"Time-based retention forgets history; log compaction remembers the latest truth."

## Problem
Consider a topic storing user profile states:
```text
Offset 0: key="user:1", val="Alice, Seattle"
Offset 1: key="user:2", val="Bob, New York"
Offset 2: key="user:1", val="Alice, Chicago"  <-- Update!
Offset 3: key="user:1", val="Alice, London"   <-- Update!
```
If we use standard time retention (e.g. 7 days), after 7 days Bob and Alice's profile states are completely deleted!
If we retain forever, the log grows infinitely with obsolete historical updates ("Seattle", "Chicago").
What if we only care about the **latest value for each key**?

## Prediction
If you write 5 updates for key `user:1` to a compacted topic, what will remain in the log after the cleaner thread runs?

## Why this matters
**Log Compaction transforms Kafka into a durable, key-addressable state store.**
It powers database CDC changelogs, KTable state stores in Kafka Streams, and disaster recovery caches.

## First principles
* **`cleanup.policy=compact`:** Kafka's log cleaner thread scans sealed segments and discards older records whose keys have newer values later in the log.
* **Tombstone Records:** To delete a key entirely in a compacted topic, the producer sends a record with the key and a `null` value. The cleaner removes all historical records and eventually purges the tombstone after `delete.retention.ms`.
* **Offset Preservation:** Compaction never changes record offsets. Offsets remain monotonically increasing, but non-contiguous (e.g. offsets 0, 1, 3).

## Mental model
```text
Before Compaction:
[ k1:v1 (off 0) | k2:v1 (off 1) | k1:v2 (off 2) | k1:v3 (off 3) | k2:null (off 4, tombstone) ]

After Compaction (Cleaner runs):
[ k2:v1 (off 1) | k1:v3 (off 3) ]   <-- k1:v1 and k1:v2 discarded! Offsets 1, 3 preserved!
```

## Build it
See [log_compaction_lab.py](../code/log_compaction_lab.py).
We produce multiple state updates and a tombstone to observe log compaction.

## Use Kafka
Create a compacted topic:
```bash
docker exec -it kafka-lab-single /opt/kafka/bin/kafka-topics.sh   --bootstrap-server localhost:9092   --create --topic compacted-users   --partitions 1 --replication-factor 1   --config cleanup.policy=compact   --config segment.bytes=10240   --config min.cleanable.dirty.ratio=0.01
```

## Inspect it
Read the topic using `kafka-console-consumer.sh` from the beginning to see state deduplication.

## Measure it
Measure storage reduction percentage before vs after compaction.

## Break it
Send updates with a `null` key on a compacted topic; observe that unkeyed records cannot be compacted!

## Recover it
Ensure all records destined for compacted topics carry explicit entity keys.

## Modify it
Send a tombstone (`value=None`) and observe key removal after deletion retention expires.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does log compaction never compact records currently residing in the active segment?
2. Why do offsets in a compacted partition become non-contiguous (e.g. jumping from 0 to 4)?

## Guarantees
* At least the last known value for each key is guaranteed to be retained indefinitely.

## Non-guarantees
* Compaction is not instantaneous; duplicates remain until the background log cleaner thread executes.

## When to use this
* Database changelogs (CDC), reference data caches, account balances, user profiles.

## When not to use this
* Immutable event series where every historical occurrence matters (e.g. audit logs, clickstreams).

## What comes next
In Phase 30, we study Replay: resetting consumer offsets to reconstruct state or recover from software bugs.
