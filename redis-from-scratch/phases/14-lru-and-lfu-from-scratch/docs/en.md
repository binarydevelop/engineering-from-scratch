# Lesson 14.1: LRU and LFU From Scratch: Exact vs. Approximated

## Motto
"Theoretical LRU requires 24 bytes of pointer overhead per key; Redis saves memory by approximating LRU with random sampling."

## Problem
Implementing exact textbook LRU requires a doubly linked list with forward and backward pointers for every key in the database. In a 50,000,000 key database, pointers alone consume > 1GB of pure RAM!

## Prediction
How close is Redis's sampled 5-key approximation to true theoretical LRU under Zipf-skewed workloads?

## Why this matters
Understanding approximated data structures is a fundamental systems engineering lesson: sacrificing 1% statistical perfection saves gigabytes of RAM.

## First principles
Redis stores a 24-bit timestamp in each object's `lru` header field. During eviction, it samples $N$ random keys (default `maxmemory-samples 5`), checks their idle time, and evicts the oldest candidate from that sample pool.

## Mental model
```text
  [ CLIENT ] ── TCP Socket Command ──► [ REDIS ENGINE ] ──► [ INTERNAL MEMORY ]
```

## Build it
See [code/lru_lfu_scratch.py](../code/lru_lfu_scratch.py).

## Use Redis
Execute the lesson experiment:
```bash
./phases/14-lru-and-lfu-from-scratch/experiments/run_experiment.sh
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
1. What happens to eviction accuracy when `maxmemory-samples` is increased from 5 to 10?
2. How does Redis LFU calculate key frequency using only an 8-bit logarithmic counter and a 16-bit decay timer in the same 24-bit field?

## When to use this
* Use LFU when access patterns follow a power-law (hot items accessed continuously over weeks).

## When not to use this
* Do not use LFU if recently published items need immediate high caching priority before accumulating frequency.

## What comes next
Proceed to the next phase in the curriculum progression.
