# Lesson 30.1: Distributed Locks: Safety, TTLs, and Fencing Tokens

## Motto
"A distributed lock is only as safe as its release token; releasing another worker's expired lock causes catastrophic data corruption."

## Problem
Two microservice workers attempt to generate an invoice for the same customer simultaneously. If both acquire a naive lock (`SET lock taken`), duplicate charges occur.

## Prediction
What catastrophic race occurs if Worker A takes a 10-second GC pause, its lock TTL expires, Worker B acquires the lock, and Worker A wakes up and executes `DEL lock`?

## Why this matters
Distributed locking is fraught with subtle failure modes (process pauses, network partitions, clock drift). Understanding safe implementation is paramount.

## First principles
A safe single-instance distributed lock requires: 1. `SET resource_key random_uuid NX PX ttl`, 2. Only releasing the lock if the stored UUID matches via an atomic Lua script, 3. Using monotonic fencing tokens to protect backend databases from paused workers.

## Mental model
```text
  [ CLIENT WORKERS ] ── TCP Socket ──► [ REDIS ENGINE ] ──► [ LOCK / LOG / STREAM ]
```

## Build it
See [code/distributed_lock_lab.py](../code/distributed_lock_lab.py).

## Use Redis
Execute the lesson experiment:
```bash
./phases/30-distributed-locks/experiments/run_experiment.sh
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
1. What is Martin Kleppmann's primary critique of the Redlock algorithm regarding asynchronous network pauses?
2. What is a Fencing Token and how does it prevent stale writes in backend storage?

## When to use this
* Use single-instance atomic locks with UUID tokens for non-critical coordination (e.g. deduplicating email sends).

## When not to use this
* Do not rely solely on Redis locks for financial settlement or data integrity where correctness demands linearizable distributed consensus (Raft/Paxos).

## What comes next
Proceed to the next phase in the curriculum progression.
