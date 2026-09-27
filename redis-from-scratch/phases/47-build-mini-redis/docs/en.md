# Lesson 47.1: Capstone 1: Build Mini-Redis From Scratch in Python

## Motto
"If you can build a working Redis-compatible server from raw sockets and a dictionary, Redis is no longer magic."

## Problem
Synthesizing all networking, protocol parsing, command execution, and expiration mechanics into a working server.

## Prediction
Can the official `redis-cli` connect to our custom Python TCP server and successfully execute `SET` and `GET`?

## Why this matters
Building the server engine connects the client socket, wire protocol, memory keyspace, and expiration into one coherent mental model.

## First principles
Mini-Redis implements: 1. Async/Threaded TCP socket server on port 6379, 2. Binary-safe RESP decoder/encoder, 3. Keyspace dictionary, 4. Command dispatch table (`SET`, `GET`, `DEL`, `EXISTS`, `INCR`, `EXPIRE`, `TTL`, `PING`), 5. Passive and active expiration loop, 6. Snapshot persistence (`SAVE`).

## Mental model
```text
  [ CLIENT ] ── TCP Socket ──► [ REDIS ENGINE CORE ] ──► [ SYSTEM SUBSYSTEM ]
```

## Build it
See [code/mini_redis_server.py](../code/mini_redis_server.py).

## Use Redis
Execute the lesson experiment:
```bash
./phases/47-build-mini-redis/experiments/run_experiment.sh
```

## Inspect it
Inspect server status, telemetry counters, and internal diagnostic logs.

## Measure it
Quantify latency percentiles, throughput, memory allocation, and failure impact.

## Break it
Inject network partitions, process terminations, or invalid commands.

## Debug it
Diagnose the failure using evidence from diagnostic tools.

## Modify it
Tune configuration thresholds and measure behavioral changes.

## Evidence
Record findings in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. How does Mini-Redis handle multiple concurrent connections using Python threading vs Redis's single-threaded event loop?
2. What changes would be required to support RESP3 in Mini-Redis?

## When to use this
* Build educational servers to achieve mastery over protocols, networking, and memory architectures.

## When not to use this
* Never deploy toy custom database servers into production.

## What comes next
Proceed to the next phase in the curriculum progression.
