# Lesson 31.1: Performance and Benchmarking: Beyond Synthetic Claims

## Motto
"Never quote '100,000 ops/sec' without stating the payload size, concurrency, pipelining, and network RTT."

## Problem
Engineers run `redis-benchmark` on localhost and claim their production architecture can handle 200,000 requests/sec. In production across cloud VPCs, network latency drops throughput to 5,000 ops/sec.

## Prediction
How does increasing the payload size from 100 bytes to 100 kilobytes affect operations per second?

## Why this matters
Accurate capacity planning prevents catastrophic performance degradation under real-world production network conditions.

## First principles
Synthetic benchmarks running on loopback (`127.0.0.1`) bypass physical network switches and NIC packet processing. Latency must be measured as percentiles (p50, p95, p99), not merely mean averages.

## Mental model
```text
  [ CLIENT ] ── TCP Socket ──► [ REDIS ENGINE CORE ] ──► [ SYSTEM SUBSYSTEM ]
```

## Build it
See [code/benchmark_harness.py](../code/benchmark_harness.py).

## Use Redis
Execute the lesson experiment:
```bash
./phases/31-performance-and-benchmarking/experiments/run_experiment.sh
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
1. Why does `redis-benchmark -q` report unrealistically optimistic numbers compared to real application workloads?
2. What is the Coordinated Omission problem in client-side latency benchmarking?

## When to use this
* Benchmark with production payload distributions, realistic network topologies, and connection pools.

## When not to use this
* Never extrapolate production server sizing from a single localhost `redis-benchmark` run.

## What comes next
Proceed to the next phase in the curriculum progression.
