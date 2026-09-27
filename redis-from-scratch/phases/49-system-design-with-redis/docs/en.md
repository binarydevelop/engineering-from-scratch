# Lesson 49.1: System Design With Redis: Twelve Production Scenarios

## Motto
"True mastery means knowing when Redis is the perfect tool, and having the courage to say no when it is not."

## Problem
Evaluating Redis suitability across 12 real-world system design interview and production scenarios.

## Prediction
For a global session store, should Redis be configured with RDB, AOF, or no persistence?

## Why this matters
Prepares the learner for senior system design interviews and principal architecture decisions.

## First principles
For every design scenario, evaluate: 1. Why Redis? 2. Data structure choice, 3. Source of truth, 4. Durability SLA, 5. TTL strategy, 6. Eviction policy, 7. Hot key mitigation, 8. Consistency requirement, 9. Replication/Partitioning needs, 10. Technology alternatives.

## Mental model
```text
  [ CLIENT ] ── TCP Socket ──► [ REDIS ENGINE CORE ] ──► [ SYSTEM SUBSYSTEM ]
```

## Build it
See [code/system_design_cases.py](../code/system_design_cases.py).

## Use Redis
Execute the lesson experiment:
```bash
./phases/49-system-design-with-redis/experiments/run_experiment.sh
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
1. Why is Redis preferred over PostgreSQL for API rate limiting but NOT for financial balance ledgering?
2. How does HyperLogLog count 1,000,000,000 unique IP addresses using only 12 kilobytes of memory?

## When to use this
* Use the 10-question evaluation framework whenever evaluating Redis in architecture design reviews.

## When not to use this
* Never select Redis simply because 'it is fast' without analyzing durability and data loss risks.

## What comes next
Proceed to the next phase in the curriculum progression.
