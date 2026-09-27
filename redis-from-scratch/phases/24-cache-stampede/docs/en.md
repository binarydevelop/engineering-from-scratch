# Lesson 24.1: Cache Stampede: The Thundering Herd Problem

## Motto
"When a hot cached key expires, 10,000 concurrent requests simultaneously experience a miss and hammer the database."

## Problem
A popular news article or product page receives 5,000 requests/sec. Its TTL expires. All 5,000 requests miss Redis at the same millisecond and query the SQL database simultaneously, crashing the database.

## Prediction
What happens to database CPU and connection pool usage during a cache stampede?

## Why this matters
Preventing cache stampedes is mandatory for large-scale e-commerce, media publishing, and high-concurrency APIs.

## First principles
Mitigations: 1. Mutex Locking / Single-Flight (only the first worker queries DB while others wait), 2. Probabilistic Early Expiration (XFetch algorithm refreshes before expiration), 3. TTL Jitter (adding random variance to avoid simultaneous key deaths).

## Mental model
```text
  [ CLIENT WORKERS ] ── TCP Socket ──► [ REDIS ENGINE ] ──► [ LOCK / LOG / STREAM ]
```

## Build it
See [code/stampede_simulator.py](../code/stampede_simulator.py).

## Use Redis
Execute the lesson experiment:
```bash
./phases/24-cache-stampede/experiments/run_experiment.sh
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
1. How does TTL Jitter prevent multiple related keys from expiring at the exact same second?
2. What is the XFetch probabilistic early expiration formula?

## When to use this
* Implement single-flight mutex locks on high-traffic, computationally expensive cached endpoints.

## When not to use this
* Do not add complex mutex locks to low-traffic keys where occasional misses do not threaten the database.

## What comes next
Proceed to the next phase in the curriculum progression.
