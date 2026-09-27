# Lesson 15.1: Pipelining: Amortizing Network Round-Trip Time

## Motto
"Redis can execute 500,000 operations per second, but a client doing one ping-pong per command will be lucky to reach 8,000."

## Problem
Network Round-Trip Time (RTT) dominates operational latency. If RTT is 1ms, a client can execute at most 1,000 commands/sec sequentially, regardless of how fast Redis CPU is.

## Prediction
How many times faster is executing 1,000 SET commands in a single pipelined TCP write compared to 1,000 individual blocking writes and reads?

## Why this matters
Pipelining is the single highest-impact optimization for batch data loading, bulk caching, and high-throughput microservices.

## First principles
TCP is full-duplex. A client can write 100 commands into its local socket buffer sequentially without blocking on each reply. The Redis server processes them all and writes 100 replies into the socket.

## Mental model
```text
  [ CLIENT WORKERS ] ── TCP Socket ──► [ REDIS ENGINE ] ──► [ LOCK / LOG / STREAM ]
```

## Build it
See [code/pipeline_demo.py](../code/pipeline_demo.py).

## Use Redis
Execute the lesson experiment:
```bash
./phases/15-pipelining/experiments/run_experiment.sh
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
1. Does pipelining guarantee that the batch of commands will execute atomically without other clients interleaving?
2. What happens to client and server memory if you pipeline 10,000,000 commands in a single buffer?

## When to use this
* Use Pipelining whenever a client needs to execute multiple independent commands concurrently.

## When not to use this
* Do not use Pipelining when subsequent commands depend on the return values of earlier commands.

## What comes next
Proceed to the next phase in the curriculum progression.
