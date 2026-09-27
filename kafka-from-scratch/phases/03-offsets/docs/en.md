# Lesson 03: Offsets

## Motto
"The log offset belongs to the storage engine; the consumer position belongs to the application."

## Problem
A consumer starts reading a log from offset 0. It processes 10 records, and then its process crashes.
When the consumer restarts:
* Where does it resume?
* If it restarts from 0, it re-processes all 10 records (duplicates).
* If it forgets where it was, it might skip records (data loss).
How do we decouple the log's physical append position from each reader's processing position?

## Prediction
What happens if a consumer commits its offset to disk *before* executing the business logic, and crashes during processing?

## Why this matters
The core distinction between:
$$\text{Log Offset} \neq \text{Consumer Position}$$
is the foundation of Kafka's multi-consumer architecture, replay capabilities, and delivery semantics (at-most-once vs. at-least-once).

## Mental model
```text
Log on Disk:
Offsets:     0     1     2     3     4     5     6     7 (Log End Offset = 8)
          [ R0 | R1 | R2 | R3 | R4 | R5 | R6 | R7 ]
                                 ▲                 ▲
                                 │                 │
                Consumer Position│                 │Append Point (LEO)
                (Last Committed = 3)
                Next Fetch = 4
```

## Build it
See [offsets_experiment.py](../code/offsets_experiment.py).
We implement explicit consumer offset tracking on top of `MiniLog`:
1. Processing with commit-after-work (At-Least-Once).
2. Processing with commit-before-work (At-Most-Once).
3. Simulating crashes to observe duplicate processing vs lost events.

## Use Kafka
In Kafka, consumer offsets are stored as messages in an internal, compacted topic named `__consumer_offsets`.

## Inspect it
Check the saved consumer position file on disk and compare it with the log's next append offset.

## Measure it
Measure the performance cost of persisting consumer offsets after every record vs. batching offset commits.

## Break it
Kill the consumer process halfway through a batch of 100 records and observe what happens upon restart.

## Recover it
Restart the consumer and observe how it reads its saved offset to resume cleanly.

## Modify it
Change the crash point to occur *before* the offset save, and observe duplicate processing.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does Kafka allow multiple consumer groups to maintain completely independent offsets on the same partition?
2. What is the danger of committing offsets asynchronously in the background?

## Guarantees
* A consumer position is a deterministic pointer into an immutable sequence of records.

## Non-guarantees
* Saving an offset does not mean the downstream database write succeeded unless they are coordinated atomically.

## When to use this
* In every streaming architecture where progress must be saved across worker restarts.

## When not to use this
* Ephemeral fire-and-forget messaging where dropped messages are completely irrelevant (e.g. lossy audio streaming).

## What comes next
In Phase 04, we turn our local Python log into a network service accessible over TCP sockets.
