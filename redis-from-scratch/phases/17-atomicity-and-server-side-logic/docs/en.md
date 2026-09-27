# Lesson 17.1: Atomicity and Server-Side Logic: Lua & Functions

## Motto
"Moving application logic to the data is faster and more correct than moving data back and forth to the client."

## Problem
An e-commerce flash sale has 1 item left in stock. 500 customers click 'Buy' simultaneously. Client-side checks (`GET stock` then `DECR stock`) cause overselling due to network race conditions.

## Prediction
Why does a Lua script executed via EVAL guarantee zero overselling without needing WATCH or retries?

## Why this matters
Lua scripts and Redis Functions allow developers to build complex atomic primitives (custom rate limiters, multi-resource locks) directly inside the database.

## First principles
Because Redis command execution is single-threaded, a Lua script runs completely uninterrupted from start to finish. All keys manipulated in the script are evaluated in a single atomic epoch.

## Mental model
```text
  [ CLIENT WORKERS ] ── TCP Socket ──► [ REDIS ENGINE ] ──► [ LOCK / LOG / STREAM ]
```

## Build it
See [code/lua_atomicity.py](../code/lua_atomicity.py).

## Use Redis
Execute the lesson experiment:
```bash
./phases/17-atomicity-and-server-side-logic/experiments/run_experiment.sh
```

## Inspect it
Inspect command return codes, internal data structures, and memory.

## Measure it
Quantify latency, concurrency race conditions, and throughput.

## Break it
Inject network delays, TTL expirations, or ungraceful client terminations.

## Debug it
Diagnose the failure using logs and atomic status returns.

## Modify it
Tune timeouts, concurrency levels, or batch sizes and observe shifts.

## Evidence
Record findings in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. What happens if a Lua script contains an infinite loop `while true do end`?
2. What are Redis Functions (introduced in Redis 7.0) and how do they improve upon ephemeral EVAL scripts?

## When to use this
* Use Lua scripts or Redis Functions for atomic multi-step mutations where conditional logic depends on current state.

## When not to use this
* Never execute slow, CPU-heavy data parsing inside Lua, as it blocks all other Redis clients.

## What comes next
Proceed to the next phase in the curriculum progression.
