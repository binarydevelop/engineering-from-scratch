# Lesson 10.1: Sorted Sets: The Skiplist Leaderboard Engine

## Motto
"Sorted Sets combine an $O(1)$ hash table with an $O(\log N)$ Skip List to give instant ranking over millions of items."

## Problem
Determining user leaderboard ranks in SQL requires `COUNT(*) WHERE score > X`, which scans or locks tables under heavy concurrent gameplay.

## Prediction
Does `ZADD` allow two different members to share the exact same score? How are ties broken?

## Why this matters
Sorted Sets are the backbone of real-time gaming leaderboards, priority queues, rate limiters, and sliding-window event indices.

## First principles
A Redis Sorted Set (`ZSET`) pairs an internal hash table (for $O(1)$ member-to-score lookup) with a probabilistic multi-level Skip List (for $O(\log N)$ ordered insertion and rank queries).

## Mental model
```text
  [ CLIENT ] ── TCP Socket Command ──► [ REDIS ENGINE ] ──► [ INTERNAL MEMORY ]
```

## Build it
See [code/sorted_set_leaderboard.py](../code/sorted_set_leaderboard.py).

## Use Redis
Execute the lesson experiment:
```bash
./phases/10-sorted-sets/experiments/run_experiment.sh
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
1. Why does Redis use a Skip List instead of a Red-Black Tree or AVL Tree for Sorted Sets?
2. How can timestamps be used as scores to implement sliding window rate limiting?

## When to use this
* Use Sorted Sets for real-time leaderboards, priority queues, and timestamp-indexed event windows.

## When not to use this
* Do not use Sorted Sets if score ordering is unnecessary; standard Sets consume less memory.

## What comes next
Proceed to the next phase in the curriculum progression.
