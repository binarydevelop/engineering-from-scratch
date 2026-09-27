# Lesson 07.1: Hashes: Structured Objects and Field-Level Access

## Motto
"Updating a single field in a hash costs $O(1)$, while updating a field in a JSON string requires deserializing the entire document."

## Problem
Storing a user profile as a serialized JSON string requires fetching the whole string over the network, parsing JSON in Python, modifying one field, serializing back to JSON, and writing it back, creating severe race conditions.

## Prediction
How does memory consumption differ between storing 10,000 users as JSON strings vs storing them as Redis Hashes?

## Why this matters
Hashes represent domain entities (users, sessions, carts) cleanly, allowing atomic field-level mutations (`HINCRBY`) without full-document serialization races.

## First principles
Redis Hashes use a two-tier internal representation: a memory-optimized `listpack` for small hashes, converting automatically to a standard hash table (`dict`) when field count or value size exceeds configuration thresholds.

## Mental model
```text
  [ CLIENT ] ── TCP Socket Command ──► [ REDIS ENGINE ] ──► [ INTERNAL MEMORY ]
```

## Build it
See [code/hash_mechanics.py](../code/hash_mechanics.py).

## Use Redis
Execute the lesson experiment:
```bash
./phases/07-hashes/experiments/run_experiment.sh
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
1. Why is HGETALL considered dangerous on very large hashes in production?
2. What command should you use instead of HGETALL to iterate through a hash with 500,000 fields?

## When to use this
* Use Hashes to represent domain objects where fields need to be independently read, updated, or incremented.

## When not to use this
* Do not use Hashes if you need nested sub-objects (hashes cannot nest other hashes in Redis core).

## What comes next
Proceed to the next phase in the curriculum progression.
