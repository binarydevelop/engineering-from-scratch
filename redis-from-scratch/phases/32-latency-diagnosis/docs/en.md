# Lesson 32.1: Latency Diagnosis: SLOWLOG, LATENCY DOCTOR, and Root Causes

## Motto
"When Redis latency spikes, the single-threaded engine means one slow command blocks every client connected to the server."

## Problem
An API suddenly times out with 500 errors. Redis CPU is at 100%. How do you identify which specific command or client is freezing the event loop?

## Prediction
Does `SLOWLOG` measure the network round-trip time or only the execution time inside the Redis engine?

## Why this matters
Diagnosing production latency spikes requires knowing the exact sequence of commands to execute without guessing.

## First principles
Redis `SLOWLOG` records commands whose execution time (excluding network I/O) exceeds `slowlog-log-slower-than`. `LATENCY DOCTOR` provides automated diagnostic recommendations.

## Mental model
```text
  [ CLIENT ] ── TCP Socket ──► [ REDIS ENGINE CORE ] ──► [ SYSTEM SUBSYSTEM ]
```

## Build it
See [code/latency_diagnosis.py](../code/latency_diagnosis.py).

## Use Redis
Execute the lesson experiment:
```bash
./phases/32-latency-diagnosis/experiments/run_experiment.sh
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
1. What is the default threshold for `slowlog-log-slower-than` in microseconds?
2. Why should `MONITOR` never be used on a busy production Redis instance?

## When to use this
* Use SLOWLOG and LATENCY DOCTOR as your first step when investigating latency spikes.

## When not to use this
* Do not leave `slowlog-log-slower-than 0` permanently enabled in production, as logging every command wastes memory.

## What comes next
Proceed to the next phase in the curriculum progression.
