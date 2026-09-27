# Lesson 14: At-Most-Once and At-Least-Once

## Motto
"You cannot avoid failures in a distributed system; you can only choose whether failures cause data loss or duplicate processing."

## Problem
Every software engineer wishes for magic "exactly-once" delivery without thinking.
In the physical world of networks and separate processes, failures happen between operations.
Consider the two operations:
1. `write_to_database(record)`
2. `commit_offset_to_kafka(record.offset)`

Which one do you execute first?
* If you commit offset **before** writing to the database, and the database crashes $\implies$ **Data is permanently lost (At-Most-Once)**.
* If you write to database **before** committing offset, and the consumer crashes $\implies$ **Record is processed a second time upon restart (At-Least-Once)**.

## Prediction
Why is At-Least-Once the standard default across 99% of enterprise software?

## Why this matters
Understanding why At-Least-Once delivery produces duplicate events forces software engineers to design **Idempotent Consumers** (Phase 15).

## Mental model
```text
At-Most-Once (Commit BEFORE Processing)
[ Commit Offset: 5 ] ──► Crash! ──► (DB write never happens!)
Result: Event 5 was skipped forever. Lost data.

At-Least-Once (Process BEFORE Commit)
[ DB Write: Event 5 ] ──► Crash! ──► (Offset 5 was never committed!)
Restart: Fetches Event 5 again!
Result: Event 5 written to DB twice. Duplicate data.
```

## Build it
See [delivery_semantics_lab.py](../code/delivery_semantics_lab.py).
We inject simulated crashes before and after database writes to prove data loss vs duplicate insertion.

## Use Kafka
Observe consumer behavior under auto-commit (`at-most-once` if processing takes longer than commit interval) vs manual commit.

## Inspect it
Query the target SQLite database to count missing vs duplicate records.

## Measure it
Quantify the duplicate rate during simulated worker restarts.

## Break it
Simulate SIGKILL immediately after a database insert.

## Recover it
Implement database deduplication (idempotency).

## Modify it
Tune `auto.commit.interval.ms` to observe how it alters the failure window.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why is data loss usually considered catastrophic, while duplicate delivery is manageable?
2. Under what rare conditions is At-Most-Once acceptable?

## Guarantees
* At-Least-Once guarantees no event will be dropped, at the expense of potential duplicates.
* At-Most-Once guarantees no duplicate processing, at the expense of potential lost events.

## Non-guarantees
* Neither pattern alone guarantees exactly-once business side effects.

## When to use this
* Use At-Least-Once as the baseline for all business-critical event processing.

## When not to use this
* Never use At-Most-Once for financial, billing, or compliance systems.

## What comes next
In Phase 15, we build Idempotent Consumers to convert At-Least-Once duplicates into safe, exactly-once business results.
