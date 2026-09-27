# Lesson 25: Kafka Storage Model

## Motto
"A partition is not a file; a partition is a directory of immutable segments and sparse indexes."

## Problem
In Phase 02, our `MiniLog` wrote all events into a single `.dat` file.
In a production Kafka broker processing billions of events, a single file would quickly reach terabytes in size:
* Finding offset 4,500,210 would require scanning gigabytes of bytes from the start of the file ($O(N)$ lookup).
* Deleting old data past retention would require rewriting the entire multi-terabyte file.
How does Kafka store partition data on physical disk so that both appends and random offset lookups are fast ($O(1)$)?

## Prediction
How does Kafka locate a specific record at offset 52,000 without scanning the file from offset 0?

## Why this matters
Understanding Kafka's on-disk storage architecture (.log, .index, .timeindex) explains how Kafka achieves sub-millisecond seek times and zero-cost retention cleanup.

## First principles
* **Partition Directory:** Each topic partition maps to a directory on disk: `<topic>-<partition_id>`.
* **Segment Files:** The log is divided into chunks (segments) named after the segment's base offset (e.g. `00000000000000000000.log`).
* **Offset Index (`.index`):** A memory-mapped, sparse binary index mapping logical offsets to physical byte positions in the `.log` file.
* **Timestamp Index (`.timeindex`):** Maps event timestamps to logical offsets for time-based lookups.

## Mental model
```text
Partition Directory: /tmp/kraft-combined-logs/orders-0/
├── 00000000000000000000.log       <-- Raw binary RecordBatches
├── 00000000000000000000.index     <-- Sparse index: [Offset 400 -> Byte 16384]
├── 00000000000000000000.timeindex <-- Timestamp index: [Time 1790165596 -> Offset 400]
└── leader-epoch-checkpoint        <-- Leader epoch state
```

## Build it
See [inspect_storage_segments.py](../code/inspect_storage_segments.py).
We inspect the binary headers and segment structure of real Kafka logs.

## Use Kafka
Inspect on-disk log files inside the container:
```bash
docker exec -it kafka-lab-single ls -la /tmp/kraft-combined-logs/
```

## Inspect it
Dump the contents of a `.log` segment using `kafka-dump-log.sh`:
```bash
docker exec -it kafka-lab-single /opt/kafka/bin/kafka-dump-log.sh   --files /tmp/kraft-combined-logs/lab-orders-0/00000000000000000000.log   --print-data-log
```

## Measure it
Measure file sizes of `.log` vs `.index` files (indexes are tiny fraction of log size due to sparse indexing).

## Break it
Observe what happens if you manually delete an `.index` file; Kafka automatically reconstructs the index from the `.log` file upon restart!

## Recover it
Demonstrate index self-healing on broker restart.

## Modify it
Inspect `leader-epoch-checkpoint` and explain its fields.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does Kafka use a *sparse* index (indexing every 4KB of data) rather than a dense index (indexing every record)?
2. How does binary search on the sparse index achieve $O(1)$ offset lookups?

## Guarantees
* Historical segments are immutable and read-only. Only the active segment accepts writes.

## Non-guarantees
* Corrupting the `.log` file directly bypasses Kafka safeguards and requires log truncation.

## When to use this
* Investigating disk storage usage, data corruption, and segment rolling policies.

## When not to use this
* Never edit or modify Kafka `.log` files directly with text editors.

## What comes next
In Phase 26, we explore the mechanical reasons why Kafka achieves blazing speed despite writing to disk.
