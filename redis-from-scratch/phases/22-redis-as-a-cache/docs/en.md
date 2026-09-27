# Lesson 22.1: Redis as a Cache: Cache-Aside vs. Write-Through

## Motto
"The fastest database query is the one you never execute against the database."

## Problem
Serving 50,000 read queries/sec directly against PostgreSQL or MySQL saturates connection pools and CPU disk queues.

## Prediction
What is the expected latency difference between a Cache Hit in Redis (<0.5ms) and a Cache Miss querying an indexed SQL database (~15-50ms)?

## Why this matters
Cache-Aside (Lazy Loading) is the dominant architecture pattern for high-scale web systems.

## First principles
In Cache-Aside: 1. Application checks Redis. 2. On hit, return data. 3. On miss, query primary DB. 4. Populate Redis with TTL. 5. Return data.

## Mental model
```text
  [ CLIENT WORKERS ] ── TCP Socket ──► [ REDIS ENGINE ] ──► [ LOCK / LOG / STREAM ]
```

## Build it
See [code/cache_aside_lab.py](../code/cache_aside_lab.py).

## Use Redis
Execute the lesson experiment:
```bash
./phases/22-redis-as-a-cache/experiments/run_experiment.sh
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
1. What are the trade-offs of Cache-Aside versus Write-Through caching?
2. What happens if the cache is populated with an infinite TTL and the database row is updated directly via an external script?

## When to use this
* Use Cache-Aside for read-heavy workloads where stale data for the duration of a TTL is acceptable.

## When not to use this
* Do not cache data that is written more frequently than it is read (cache churn wastes memory).

## What comes next
Proceed to the next phase in the curriculum progression.
