# Lesson 05.1: Redis Command Execution Mental Model

## Motto
"Redis is fast because its event loop does not context switch between worker threads for data access."

## Problem
Why does Redis run single-threaded for command execution? How does a single thread handle 10,000 concurrent client connections without freezing?

## Prediction
What happens if a single client executes `KEYS *` on a dataset with 50,000,000 keys? What happens to other connected clients?

## Why this matters
Understanding the event loop (`ae.c`) and I/O multiplexing explains why Redis avoids locks, and why any long-running $O(N)$ command freezes every client on the server.

## First principles
The Reactor Pattern: an I/O multiplexer (`epoll`/`kqueue`) notifies the event loop when a socket has bytes. The single thread parses the command, executes it in RAM without thread contention, and queues the reply.

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
See [code/trace_command.py](../code/trace_command.py).

## Use Redis
Execute the lesson experiment:
```bash
./phases/05-command-execution-mental-model/experiments/run_experiment.sh
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
1. If Redis is single-threaded, how does it take advantage of multi-core servers?
2. What are I/O threads in Redis 6.0+, and do they execute data commands?

## When to use this
* Rely on Redis's single-threaded nature to achieve atomic operations without mutex contention.

## When not to use this
* Never execute unbounded blocking commands like `KEYS *` or CPU-intensive Lua loops on the main thread.

## What comes next
Proceed to the next phase to build upon these systems primitives.
