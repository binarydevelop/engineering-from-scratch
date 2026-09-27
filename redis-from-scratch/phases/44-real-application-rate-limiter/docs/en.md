# Lesson 44.1: Real Application: Distributed Rate Limiter

## Motto
"Correct rate limiting requires zero-race atomicity; Lua scripts ensure no request slips through concurrent gaps."

## Problem
Protecting a distributed microservices gateway from abusive traffic spikes while maintaining sub-millisecond overhead.

## Prediction
Why does a Token Bucket algorithm provide superior user experience compared to a hard Fixed Window cutoff?

## Why this matters
Demonstrates production gateway protection using atomic server-side Lua scripts.

## First principles
See [projects/03-rate-limiter/](../../../projects/03-rate-limiter/) for complete implementations of all three rate-limiting algorithms.

## Mental model
```text
  [ CLIENT ] ── TCP Socket ──► [ REDIS ENGINE CORE ] ──► [ SYSTEM SUBSYSTEM ]
```

## Build it
See [code/rate_limiter_app.py](../code/rate_limiter_app.py).

## Use Redis
Execute the lesson experiment:
```bash
./phases/44-real-application-rate-limiter/experiments/run_experiment.sh
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
1. How do you handle Redis connection failures inside rate-limiting middleware (Fail-Open vs Fail-Closed)?
2. What are the trade-offs of running rate limiters locally in app memory vs centralized in Redis?

## When to use this
* Deploy centralized Redis rate limiting for global API tiers, authentication endpoints, and payment gateways.

## When not to use this
* Do not use centralized Redis rate limiters if microservice network RTT exceeds total latency SLA budget.

## What comes next
Proceed to the next phase in the curriculum progression.
