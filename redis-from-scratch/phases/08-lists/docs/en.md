# Lesson 08.1: Lists: Sequential Queues, Stacks, and Capped Collections

## Motto
"Redis lists are linked lists, not arrays: inserting at the head or tail is $O(1)$, but indexing into the middle is $O(N)$."

## Problem
Applications need simple FIFO queues or capped timelines (e.g., 'last 10 user activities'). Implementing this in SQL requires indexing and sorting timestamps.

## Prediction
Is LPUSH + RPOP faster or slower when the list grows from 1,000 items to 10,000,000 items?

## Why this matters
Lists provide fundamental queuing primitives (`LPUSH`/`RPOP`, `BLPOP` blocking pops) and sliding activity feeds (`LTRIM`).

## First principles
Redis Lists are implemented using `quicklist`, a doubly linked list of `listpack` memory buffers. Pushes and pops at the ends are strictly $O(1)$, while `LINDEX` or `LSET` at arbitrary offsets must traverse nodes.

## Mental model
```text
  [ CLIENT ] ── TCP Socket Command ──► [ REDIS ENGINE ] ──► [ INTERNAL MEMORY ]
```

## Build it
See [code/list_queues.py](../code/list_queues.py).

## Use Redis
Execute the lesson experiment:
```bash
./phases/08-lists/experiments/run_experiment.sh
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
1. Why is LPUSH followed by RPOP suitable for lightweight job queues, and why is it dangerous if workers crash unexpectedly?
2. What is the computational complexity of `LRANGE mylist 500000 500010` on a list with 1,000,000 elements?

## When to use this
* Use Lists for FIFO queues, LIFO stacks, activity logs, and capped feeds via LTRIM.

## When not to use this
* Do not use Lists for random index access by integer offset or when jobs require persistent acknowledgment (use Streams instead).

## What comes next
Proceed to the next phase in the curriculum progression.
