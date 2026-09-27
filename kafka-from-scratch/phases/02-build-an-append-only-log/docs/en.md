# Lesson 02: Build an Append-Only Log

## Motto
"A database modifies data in place; a log records the immutable passage of time."

## Problem
How do you store a continuous stream of events so that writes are fast, data is never accidentally overwritten, and consumers can read sequentially from any point in time?

## Prediction
If you only append bytes to the end of a file, what is the computational complexity $O(?)$ of writing a new record, and why does disk hardware favor this pattern?

## Why this matters
The append-only log is the conceptual seed of Apache Kafka. Every topic partition in Kafka is fundamentally an append-only log on disk. Understanding this primitive eliminates 90% of the confusion around offsets and immutability.

## First principles
* **Sequential Write:** Writing to the tail of a file avoids moving disk heads (on HDDs) and avoids block erase/re-write cycles (on SSDs).
* **Length Prefixing:** Prefixing each record with its byte length enables safe framing and sequential parsing without parsing delimiters.
* **Monotonic Offset:** Each record is identified by an ever-increasing integer index ($0, 1, 2, ...$).

## Mental model
```text
Disk File: mini_log.dat
Offset 0: [length: 12 bytes][data: user-created]
Offset 1: [length: 10 bytes][data: email-sent]
Offset 2: [length: 15 bytes][data: payment-started]
Offset 3: [length: 17 bytes][data: payment-completed] <--- Append point (Tail)
```

## Build it
See [mini_log.py](../code/mini_log.py).
We build a pure Python class `MiniLog` that supports:
1. `append(data: bytes) -> int` (returns monotonic offset)
2. `read(from_offset: int) -> list[tuple[int, bytes]]`

## Use Kafka
In Kafka, every partition is stored inside a directory named `<topic>-<partition>` containing `.log` files written using this exact append-only paradigm.

## Inspect it
Read the raw binary file created by `mini_log.py` using `hexdump` or Python `open(..., 'rb')`.

## Measure it
Measure write throughput of 10,000 appends.

## Break it
Simulate a partial write (corrupt the length header) and observe how sequential reading detects truncation or corruption.

## Recover it
Truncate the corrupted tail bytes back to the last valid record boundary.

## Modify it
Add a CRC32 checksum to each record header to detect payload corruption.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does an append-only log make concurrent reading and writing thread-safe without heavy locking?
2. Why can you not "delete" record #2 without rewriting the entire file?

## Guarantees
* Appends are strictly ordered and immutable.
* Historical records cannot be silently modified.

## Non-guarantees
* A single file cannot grow infinitely; it will eventually exhaust disk space (solved later by segment rolling and retention).

## When to use this
* Event streaming, financial audit ledgers, database write-ahead logs (WAL).

## When not to use this
* Workloads requiring frequent in-place updates of key-value pairs (use B-Trees or LSM-Trees instead).

## What comes next
In Phase 03, we explore the crucial distinction between the log's append offset and a consumer's reading position.
