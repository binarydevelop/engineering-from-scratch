# Lesson 46.1: Redis Anti-Patterns: Ten Catastrophic Production Mistakes

## Motto
"Knowing what NOT to do in Redis is just as important as knowing how to use it."

## Problem
Teams repeatedly make identical architectural mistakes that take down production clusters under load.

## Prediction
What happens if a developer runs `KEYS *` on a production Redis instance with 20,000,000 keys?

## Why this matters
Auditing and eliminating anti-patterns prevents 90% of all Redis production incidents.

## First principles
The 10 Anti-Patterns: 1. `KEYS *` in production (blocks thread), 2. Giant values (> 1MB strings/blobs), 3. Unbounded keys with no TTL, 4. Synchronized TTL stampedes, 5. Unsafe distributed lock release, 6. Using Pub/Sub as a durable queue, 7. Storing everything as unindexed JSON blobs, 8. Giant single hash/set (> 100k items), 9. Assuming replicas are always in sync, 10. Assuming cluster operations behave like single-node Redis.

## Mental model
```text
  [ CLIENT ] ── TCP Socket ──► [ REDIS ENGINE CORE ] ──► [ SYSTEM SUBSYSTEM ]
```

## Build it
See [code/anti_patterns_lab.py](../code/anti_patterns_lab.py).

## Use Redis
Execute the lesson experiment:
```bash
./phases/46-redis-anti-patterns/experiments/run_experiment.sh
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
1. How does `SCAN` avoid blocking the server while iterating over millions of keys?
2. Why does adding random TTL Jitter (e.g. `300 + random(0, 30)`) eliminate synchronized expiration stampedes?

## When to use this
* Use this checklist during code reviews and architectural audits before shipping Redis code to production.

## When not to use this
* Never exempt 'internal test scripts' from these rules if they run against shared production clusters.

## What comes next
Proceed to the next phase in the curriculum progression.
