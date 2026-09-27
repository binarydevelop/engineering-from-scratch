# Lesson 43.1: Real Application: Global Real-Time Leaderboard

## Motto
"Scaling leaderboards from 1,000 to 10,000,000 players requires $O(\log N)$ skiplists, not SQL order-by scans."

## Problem
Calculating global ranks across millions of concurrent gaming players in real time without locking tables.

## Prediction
What is the time complexity of retrieving the top 100 players from a 10M-member Sorted Set?

## Why this matters
Demonstrates how specialized in-memory data structures solve computational bottlenecks that break relational databases.

## First principles
See [projects/02-leaderboard/](../../../projects/02-leaderboard/) for the full tournament leaderboard implementation.

## Mental model
```text
  [ CLIENT ] ── TCP Socket ──► [ REDIS ENGINE CORE ] ──► [ SYSTEM SUBSYSTEM ]
```

## Build it
See [code/leaderboard_app.py](../code/leaderboard_app.py).

## Use Redis
Execute the lesson experiment:
```bash
./phases/43-real-application-leaderboard/experiments/run_experiment.sh
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
1. How do you handle pagination when users are continuously gaining points and shifting ranks?
2. How can you partition a leaderboard across multiple Redis nodes if player count exceeds single-node memory?

## When to use this
* Use Redis Sorted Sets for live gaming rankings, dynamic priority queues, and top-selling product boards.

## When not to use this
* Do not use Sorted Sets if score modifications require multi-table relational joins or historical audit trails.

## What comes next
Proceed to the next phase in the curriculum progression.
