# Lesson 12.1: Expiration and TTL: Active vs. Passive Deletion

## Motto
"Setting a TTL does not mean Redis sets an OS hardware timer for each individual key."

## Problem
If Redis has 50,000,000 keys with expiration deadlines, setting individual OS timers or sorting a continuous priority queue would overwhelm the CPU.

## Prediction
If a key expires at timestamp T, is its memory reclaimed at exactly timestamp T?

## Why this matters
Memory leaks in production frequently occur when millions of keys expire but are never accessed again, depending entirely on the active expiration background cycle.

## First principles
Redis uses two complementary expiration algorithms: 1. Passive Expiration (lazy deletion upon attempted key read), and 2. Active Expiration (`serverCron` samples 20 random keys with TTL 10 times per second, deleting expired keys and repeating if > 25% were expired).

## Mental model
```text
  [ CLIENT ] ── TCP Socket Command ──► [ REDIS ENGINE ] ──► [ INTERNAL MEMORY ]
```

## Build it
See [code/expiration_engine.py](../code/expiration_engine.py).

## Use Redis
Execute the lesson experiment:
```bash
./phases/12-expiration-and-ttl/experiments/run_experiment.sh
```

## Inspect it
Use diagnostic commands to inspect internal representations and memory.

## Measure it
Quantify latency, operations/second, and memory allocations.

## Break it
Inject failure conditions and analyze server behavior.

## Debug it
Diagnose the failure using logs and error codes.

## Modify it
Tune parameters and observe the shift in operational behavior.

## Evidence
Record findings in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. What is the return value of `TTL` when a key exists without an expiration? What about when the key does not exist?
2. Why could a sudden spike in expired keys cause temporary latency in the main Redis event loop?

## When to use this
* Always set TTLs on temporary caches, authentication sessions, and rate-limiting buckets.

## When not to use this
* Never rely on Redis TTL as a strict sub-millisecond real-time scheduler guarantee.

## What comes next
Proceed to the next phase in the curriculum progression.
