# Lesson 41.1: Observability: Metrics, Prometheus, and the Top 8 Signals

## Motto
"You cannot manage what you do not measure; monitor connections, memory, latency, and evictions."

## Problem
A production outage begins with subtle memory fragmentation and replica lag. Without observability, the team only notices when the entire site crashes.

## Prediction
Which single metric in `INFO stats` indicates whether keys are being evicted due to memory pressure?

## Why this matters
A production dashboard must surface key leading indicators before catastrophic failure occurs.

## First principles
The Top 8 Production Metrics: 1. `connected_clients`, 2. `instantaneous_ops_per_sec`, 3. `used_memory_rss`, 4. `mem_fragmentation_ratio`, 5. `evicted_keys`, 6. `rejected_connections`, 7. `master_repl_offset` (Replica Lag), 8. `latest_fork_usec`.

## Mental model
```text
  [ CLIENT ] ── TCP Socket ──► [ REDIS ENGINE CORE ] ──► [ SYSTEM SUBSYSTEM ]
```

## Build it
See [code/observability_collector.py](../code/observability_collector.py).

## Use Redis
Execute the lesson experiment:
```bash
./phases/41-observability/experiments/run_experiment.sh
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
1. Why is `rejected_connections` greater than 0 a critical emergency alert?
2. How is cache hit ratio calculated from `keyspace_hits` and `keyspace_misses`?

## When to use this
* Scrape Redis metrics via Prometheus `redis_exporter` and establish alerts on eviction spikes and memory RSS.

## When not to use this
* Do not poll `INFO` at excessive sub-second frequencies, as string parsing carries overhead.

## What comes next
Proceed to the next phase in the curriculum progression.
