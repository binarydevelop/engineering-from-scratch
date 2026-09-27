# Lesson 18.1: Persistence: Why Memory Is Not Enough

## Motto
"Volatile memory is transient; without persistence, a single power flicker turns your database into a blank slate."

## Problem
An application stores 1,000,000 user sessions in Redis. A server kernel panic occurs. What state survives reboot?

## Prediction
If Redis is killed with SIGKILL (kill -9) while persistence is disabled, how much data can be recovered?

## Why this matters
Architects must evaluate durability guarantees: can your application afford to lose the last 1 second, 1 hour, or zero data during an infrastructure crash?

## First principles
In-memory datasets reside entirely in volatile DRAM. To survive process death, the state must be materialized into non-volatile block storage via snapshots (RDB) or write-ahead transaction logs (AOF).

## Mental model
```text
  [ CLIENT WORKERS ] ── TCP Socket ──► [ REDIS ENGINE ] ──► [ LOCK / LOG / STREAM ]
```

## Build it
See [code/persistence_crash.py](../code/persistence_crash.py).

## Use Redis
Execute the lesson experiment:
```bash
./phases/18-persistence-why-memory-is-not-enough/experiments/run_experiment.sh
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
1. Why is synchronous disk writing (`fsync always`) significantly slower than in-memory updates?
2. What happens if an operating system reboots before the kernel flushes dirty pages to physical NVMe storage?

## When to use this
* Use non-persistent mode for pure ephemeral caches that can be reconstructed seamlessly from primary databases.

## When not to use this
* Never run Redis without persistence if it holds authoritative user data, balances, or task queues.

## What comes next
Proceed to the next phase in the curriculum progression.
