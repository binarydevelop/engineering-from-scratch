# Lesson 35.1: Replication Failure Modes: Backlog Overflow & Desync

## Motto
"Replication is not automatic failover: if the primary dies, replicas do not magically promote themselves."

## Problem
A replica temporarily loses its network connection for 30 seconds. When it reconnects, how does it catch up? What happens if the network outage lasts for hours?

## Prediction
What happens if the volume of writes during an outage exceeds the size of the circular `repl-backlog-size` buffer?

## Why this matters
Distinguishing between Partial Resynchronization (`PSYNC`) and catastrophic Full Resynchronization (disk fork + RDB network transfer) is essential for production resilience.

## First principles
The primary maintains a circular memory buffer (`repl-backlog`). If a replica reconnects and its offset is still within the backlog, a fast incremental sync (`PSYNC`) occurs. If the offset fell off the ring, a full RDB snapshot must be generated and transferred.

## Mental model
```text
  [ CLIENT ] ── TCP Socket ──► [ REDIS ENGINE CORE ] ──► [ SYSTEM SUBSYSTEM ]
```

## Build it
See [code/repl_failure_modes.py](../code/repl_failure_modes.py).

## Use Redis
Execute the lesson experiment:
```bash
./phases/35-replication-failure-modes/experiments/run_experiment.sh
```

## Inspect it
Inspect server status, telemetry counters, and internal diagnostic logs.

## Measure it
Quantify latency percentiles, throughput, memory allocation, and failure impact.

## Break it
Inject network partitions, process terminations, or invalid commands.

## Debug it
Diagnose the failure using evidence from diagnostic tools.

## Modify it
Tune configuration thresholds and measure behavioral changes.

## Evidence
Record findings in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why can a full resynchronization of a 30GB instance degrade network performance across the entire cluster?
2. What is `diskless-replication` and when should it be enabled?

## When to use this
* Size `repl-backlog-size` generously (e.g. 512MB-1GB) to survive brief network blips without triggering full RDB syncs.

## When not to use this
* Never assume replicas will automatically promote themselves when a primary dies without an external coordinator like Sentinel.

## What comes next
Proceed to the next phase in the curriculum progression.
