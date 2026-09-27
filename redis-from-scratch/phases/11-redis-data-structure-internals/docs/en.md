# Lesson 11.1: Redis Data Structure Internals & Encodings

## Motto
"The public Redis command abstraction remains constant, but the underlying C memory encoding morphs as datasets expand."

## Problem
Engineers assume that a Redis Hash or List has a fixed memory overhead. In reality, Redis transparently changes data encodings at runtime to save RAM.

## Prediction
What happens to `OBJECT ENCODING` of a hash when you insert a field longer than 64 bytes?

## Why this matters
Memory is the most expensive resource in an in-memory database. Understanding compact encodings (`listpack`, `intset`, `embstr`) allows you to store 5x to 10x more data in the same RAM budget.

## First principles
Small collections are encoded in continuous memory byte buffers (`listpack`). When element count exceeds `hash-max-listpack-entries` (default 512) or element size exceeds `hash-max-listpack-value` (default 64), Redis automatically converts the encoding to a full hash table.

## Mental model
```text
  [ CLIENT ] ── TCP Socket Command ──► [ REDIS ENGINE ] ──► [ INTERNAL MEMORY ]
```

## Build it
See [code/inspect_encodings.py](../code/inspect_encodings.py).

## Use Redis
Execute the lesson experiment:
```bash
./phases/11-redis-data-structure-internals/experiments/run_experiment.sh
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
1. Why is a `listpack` more memory efficient than a hash table for small element counts?
2. Why doesn't Redis keep everything in a listpack indefinitely?

## When to use this
* Design key naming and data schemas to leverage compact encodings for massive datasets.

## When not to use this
* Avoid tuning listpack thresholds too high (> 2048 entries), as linear CPU search within the buffer degrades throughput.

## What comes next
Proceed to the next phase in the curriculum progression.
