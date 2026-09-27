# Lesson 23.1: Cache Invalidation: The Hardest Problem in Computer Science

## Motto
"There are only two hard things in Computer Science: cache invalidation and naming things."

## Problem
A user updates their email address in the database. Because the old email remains cached in Redis, other services continue reading obsolete data.

## Prediction
If you update the database and then delete the cache key, can a concurrent reader still re-populate the cache with stale data?

## Why this matters
Stale data anomalies create security vulnerabilities, incorrect financial balances, and user confusion.

## First principles
Cache invalidation strategies include: 1. Passive TTL expiration, 2. Explicit deletion on write (`DEL key`), 3. Write-Through cache update, and 4. Versioned keys (`user:profile:v2`).

## Mental model
```text
  [ CLIENT WORKERS ] ── TCP Socket ──► [ REDIS ENGINE ] ──► [ LOCK / LOG / STREAM ]
```

## Build it
See [code/cache_invalidation_lab.py](../code/cache_invalidation_lab.py).

## Use Redis
Execute the lesson experiment:
```bash
./phases/23-cache-invalidation/experiments/run_experiment.sh
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
1. Why is deleting the cache key (`DEL`) generally preferred over updating the cache key (`SET`) during database writes?
2. What is the Cache Invalidation Race Condition that occurs when a DB read and DB write interleave?

## When to use this
* Always implement explicit cache invalidation (`DEL key`) alongside TTL safety nets on write operations.

## When not to use this
* Never rely solely on long TTLs (hours/days) for mutable user or business settings.

## What comes next
Proceed to the next phase in the curriculum progression.
