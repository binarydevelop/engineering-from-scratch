# Lesson 02.1: Build a Tiny Key-Value Store

## Motto
"Before it was a distributed server, Redis was a data structure in RAM."

## Problem
Before inspecting Redis commands, we must understand what a key-value store actually does at the data structure level: mapping arbitrary binary/string keys to values.

## Prediction
What fundamental capabilities does a standard Python dictionary lack that a database must provide?

## Why this matters
A raw hash table has no networking, persistence, concurrency safety, TTL expiration, or memory eviction limits. Redis is a hash table wrapped in operating system systems engineering.

## First principles
A key-value store provides CRUD primitives: SET (insert/update), GET (lookup), DELETE (remove), and EXISTS (membership check).

## Mental model
```text
CLIENT                     REDIS EVENT LOOP (ae.c)             MEMORY (dict.c)
  │                                   │                               │
  ├─ TCP Socket write() ─────────────►│                               │
  │                                   ├─ epoll/kqueue event fired     │
  │                                   ├─ readQueryFromClient()        │
  │                                   ├─ parse RESP command           │
  │                                   ├─ lookup & call() ────────────►├─ dictEntry insert
  │                                   ├─ addReply() buffer            │
  │◄─ TCP Socket read() ──────────────┤                               │
```

## Build it
See [code/mini_kv.py](../code/mini_kv.py).

## Use Redis
Execute the lesson experiment:
```bash
./phases/02-build-a-tiny-key-value-store/experiments/run_experiment.sh
```

## Inspect it
```bash
redis-cli INFO
```

## Measure it
Run quantitative benchmark and inspect execution latency.

## Break it
Stop the background Redis daemon or inject an invalid payload.

## Debug it
Observe error logs and connection socket diagnostic codes.

## Modify it
Adjust payload size or connection parameters and record shifts.

## Evidence
Record your findings in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. What happens when two threads call `kv.set()` simultaneously in Python? Is dict thread-safe?
2. How would you persist `self._store` to disk without blocking reads?

## When to use this
* Use process-local memory dictionaries when data never needs to outlive the process or be shared across instances.

## When not to use this
* Do not use process-local dictionaries when multiple service replicas must share a coherent state.

## What comes next
Proceed to the next phase to build upon these systems primitives.
