# Lesson 13.1: Memory and Eviction: Expiration != Eviction

## Motto
"Expiration is driven by time; eviction is driven by memory pressure."

## Problem
What happens when an application attempts to write to Redis when physical RAM is 100% full?

## Prediction
Under `noeviction` mode, what error does Redis return when memory exceeds `maxmemory`? Can GET requests still succeed?

## Why this matters
Misconfiguring eviction policies causes either silent data loss of critical sessions or hard application write outages (`OOM command not allowed`).

## First principles
When `used_memory >= maxmemory`, Redis triggers its eviction engine. Policies dictate which keys to sacrifice: `noeviction` (reject writes), `allkeys-lru` / `volatile-lru`, `allkeys-lfu` / `volatile-lfu`, or `volatile-ttl`.

## Mental model
```text
  [ CLIENT ] ── TCP Socket Command ──► [ REDIS ENGINE ] ──► [ INTERNAL MEMORY ]
```

## Build it
See [code/eviction_policies.py](../code/eviction_policies.py).

## Use Redis
Execute the lesson experiment:
```bash
./phases/13-memory-and-eviction/experiments/run_experiment.sh
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
1. If Redis is used as both a persistent datastore and an ephemeral cache, which eviction policy should be used?
2. Why does `volatile-lru` act identically to `noeviction` if no keys have TTLs assigned?

## When to use this
* Use `allkeys-lru` or `allkeys-lfu` when Redis operates as a dedicated caching layer.

## When not to use this
* Never use `allkeys-lru` when Redis stores authoritative data like user accounts or financial ledger records.

## What comes next
Proceed to the next phase in the curriculum progression.
