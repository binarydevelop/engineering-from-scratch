# Lesson 06.1: Strings: Texts, Counters, and Binary-Safe Blobs

## Motto
"A Redis string is not a C string; it is an SDS buffer that can safely store arbitrary raw bytes including nulls."

## Problem
Traditional C strings use null terminators ('\0'), which means they cannot store binary data like protocol buffers or compressed images. Furthermore, finding their length requires an $O(N)$ string scan.

## Prediction
If we call INCR on a key that does not exist, what does Redis do? What happens if we call INCR on a key containing 'hello'?

## Why this matters
Redis Strings are the universal primitive for caching HTML pages, JSON blobs, atomic counters, bitfields, and rate limiters.

## First principles
Simple Dynamic Strings (SDS) store explicit buffer length (`len`), free capacity (`alloc`), and payload. Length checks are $O(1)$. In-place string appends avoid quadratic reallocation.

## Mental model
```text
  [ CLIENT ] ── TCP Socket Command ──► [ REDIS ENGINE ] ──► [ INTERNAL MEMORY ]
```

## Build it
See [code/string_internals.py](../code/string_internals.py).

## Use Redis
Execute the lesson experiment:
```bash
./phases/06-strings/experiments/run_experiment.sh
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
1. Why is INCR safe under 10,000 concurrent clients while `x = x + 1` in Python is not?
2. What is the maximum allowable size of a Redis string value?

## When to use this
* Use Strings for text caching, serialized objects, distributed counters, and bitwise flags.

## When not to use this
* Do not store giant multi-megabyte JSON arrays in a single string if you only need to read or update a single property.

## What comes next
Proceed to the next phase in the curriculum progression.
