# Lesson 09.1: Sets: Uniqueness, Memberships, and Set Algebra

## Motto
"Sets guarantee uniqueness in $O(1)$ and compute mathematical unions and intersections directly inside the database."

## Problem
Tracking unique visitors or calculating common interests between social network users in SQL requires expensive `DISTINCT` queries and `INNER JOIN` operations.

## Prediction
What happens if you SADD the exact same string 100 times to a set? What is the return value of SADD on the second attempt?

## Why this matters
Sets provide constant-time membership testing (`SISMEMBER`), tagging systems, and server-side set algebra (`SINTER`, `SUNION`, `SDIFF`).

## First principles
Redis Sets are represented internally as an `intset` (compact sorted array of integers) when all members are integers, upgrading to a full hash table (`dict`) when non-integer strings are added or size thresholds are crossed.

## Mental model
```text
  [ CLIENT ] ── TCP Socket Command ──► [ REDIS ENGINE ] ──► [ INTERNAL MEMORY ]
```

## Build it
See [code/set_operations.py](../code/set_operations.py).

## Use Redis
Execute the lesson experiment:
```bash
./phases/09-sets/experiments/run_experiment.sh
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
1. Why is SMEMBERS dangerous on sets with millions of members?
2. How does `SRANDMEMBER` differ from `SPOP`?

## When to use this
* Use Sets for unique item collections, tagging, access control lists, and graph relationship intersections.

## When not to use this
* Do not use Sets when element ordering or ranking matters (use Sorted Sets).

## What comes next
Proceed to the next phase in the curriculum progression.
