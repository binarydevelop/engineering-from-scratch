# Lesson 27.1: Build an Append-Only Event Log From Scratch

## Motto
"A stream is an immutable, ordered sequence of records, each identified by a monotonically increasing ID."

## Problem
Before using Redis Streams, we must understand the mechanics of message offsets, event replays, and consumer coordination problems.

## Prediction
What happens if two independent workers want to consume the same event log at different speeds?

## Why this matters
This first-principles implementation reveals why simple lists cannot solve distributed worker coordination.

## First principles
An event log assigns sequential IDs (`0, 1, 2...`). Consumers maintain their own `last_read_id`, enabling independent replay without deleting messages from the log.

## Mental model
```text
  [ CLIENT WORKERS ] ── TCP Socket ──► [ REDIS ENGINE ] ──► [ LOCK / LOG / STREAM ]
```

## Build it
See [code/event_log_scratch.py](../code/event_log_scratch.py).

## Use Redis
Execute the lesson experiment:
```bash
./phases/27-build-an-append-only-event-log/experiments/run_experiment.sh
```

## Inspect it
Inspect command return codes, internal data structures, and memory.

## Measure it
Quantify latency, concurrency race conditions, and throughput.

## Break it
Inject network delays, TTL expirations, or ungraceful client terminations.

## Debug it
Diagnose the failure using logs and atomic status returns.

## Modify it
Tune timeouts, concurrency levels, or batch sizes and observe shifts.

## Evidence
Record findings in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. How does an offset-based event log differ fundamentally from a pop-based FIFO queue?
2. What garbage collection problem arises when an event log grows indefinitely?

## When to use this
* Use event logs when multiple independent microservices must read the same stream of domain events.

## When not to use this
* Do not use event logs if events must be strictly deleted immediately upon first receipt.

## What comes next
Proceed to the next phase in the curriculum progression.
