# Lesson 00.1: Environment and Redis Lab

## Motto
"The redis-cli command does not store data; it asks a background TCP server to store it."

## Problem
Engineers often treat Redis as a CLI utility or an opaque cloud service without realizing it is a standard user-space daemon listening on TCP port 6379. When connection timeouts or port conflicts occur, they cannot diagnose the failure.

## Prediction
If redis-server is stopped, what exact error does redis-cli PING return? How does redis-cli distinguish between an unreachable host and an authentication failure?

## Why this matters
Understanding the client-server boundary over TCP is the prerequisite for debugging connection pooling, firewall rules, Docker bridge networking, and TLS encryption in production.

## First principles
Redis is a client-server architecture running over TCP/IP sockets. By default, it binds to 127.0.0.1 on port 6379. Clients send command frames and receive response frames over persistent TCP connections.

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
See [code/verify_lab.py](../code/verify_lab.py).

## Use Redis
Execute the lesson experiment:
```bash
./phases/00-environment-and-redis-lab/experiments/run_experiment.sh
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
1. Why does Redis bind to 127.0.0.1 by default instead of 0.0.0.0?
2. What happens if two processes attempt to bind to TCP port 6379 simultaneously?

## When to use this
* Use standalone Redis when single-node sub-millisecond key-value operations satisfy your throughput and dataset size requirements.

## When not to use this
* Do not expose standalone Redis directly to the public internet without firewall rules, TLS, and strong ACLs.

## What comes next
Proceed to the next phase to build upon these systems primitives.
