# Lesson 29.1: Rate Limiting: Algorithms and Concurrency Races

## Motto
"A naive rate limiter with GET then INCR creates a race condition that lets attackers send 10x their allowed quota."

## Problem
An API allows 100 requests per minute. Under concurrent attacks, naive multi-command checks experience race conditions that breach limits.

## Prediction
What is the boundary flaw of the Fixed Window Counter algorithm at minute transitions?

## Why this matters
Rate limiting protects microservices against denial-of-service attacks, credential stuffing, and resource exhaustion.

## First principles
Fixed Window Counters can leak 2x traffic across boundaries. Sliding Window Logs via Sorted Sets provide perfect accuracy at high memory cost. Token Buckets implemented via atomic Lua scripts provide constant memory and smooth bursting.

## Mental model
```text
  [ CLIENT WORKERS ] ── TCP Socket ──► [ REDIS ENGINE ] ──► [ LOCK / LOG / STREAM ]
```

## Build it
See [code/rate_limiter_lab.py](../code/rate_limiter_lab.py).

## Use Redis
Execute the lesson experiment:
```bash
./phases/29-rate-limiting/experiments/run_experiment.sh
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
1. How does the Sliding Window Log algorithm calculate requests within the last 60 seconds?
2. Why does a Token Bucket algorithm provide smoother traffic shaping than a Fixed Window limiter?

## When to use this
* Use atomic Redis rate limiters at your API gateway to enforce quotas across distributed worker instances.

## When not to use this
* Do not implement rate limiters using non-atomic separate GET and SET commands.

## What comes next
Proceed to the next phase in the curriculum progression.
