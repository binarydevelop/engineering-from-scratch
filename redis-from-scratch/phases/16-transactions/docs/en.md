# Lesson 16.1: Transactions: MULTI, EXEC, and Optimistic Locking (WATCH)

## Motto
"Redis transactions guarantee isolation and sequential execution, but they do NOT provide SQL-style rollback on runtime errors."

## Problem
Two concurrent clients attempt to transfer money between accounts. If both read balance 100, calculate new balances, and write back, race conditions corrupt the ledger.

## Prediction
If a command inside a MULTI block encounters a type error (e.g. INCR on a string), does Redis roll back earlier commands in the transaction?

## Why this matters
Understanding optimistic concurrency control (`WATCH`) is critical for coordinating shared state without pessimistic distributed database locks.

## First principles
MULTI queues commands in memory on the server. EXEC runs them all sequentially without interruption from other clients. WATCH implements Optimistic Concurrency Control (OCC): if a watched key changes before EXEC, the transaction aborts.

## Mental model
```text
  [ CLIENT WORKERS ] ── TCP Socket ──► [ REDIS ENGINE ] ──► [ LOCK / LOG / STREAM ]
```

## Build it
See [code/transactions_demo.py](../code/transactions_demo.py).

## Use Redis
Execute the lesson experiment:
```bash
./phases/16-transactions/experiments/run_experiment.sh
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
1. Why did Redis choose not to implement automatic rollback on runtime errors?
2. How does `WATCH` differ from a pessimistic mutex lock?

## When to use this
* Use MULTI/EXEC with WATCH when multiple keys need atomic mutation based on preconditions.

## When not to use this
* Do not assume Redis transactions provide ACID durability or relational rollback semantics.

## What comes next
Proceed to the next phase in the curriculum progression.
