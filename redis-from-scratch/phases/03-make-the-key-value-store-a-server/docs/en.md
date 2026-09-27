# Lesson 03.1: Make the Key-Value Store a Server

## Motto
"A database is a data structure accessible over a network socket."

## Problem
Process-local dictionaries cannot be shared across multiple web servers. We must expose our key-value store over a TCP socket server.

## Prediction
If a client sends 'SET name John Doe' using a simple space-delimited text protocol, how does the server distinguish between the key and a value containing spaces?

## Why this matters
Naive protocols break immediately when payloads contain spaces, newlines, or binary data. This creates the exact motivation for Redis's length-prefixed RESP protocol.

## First principles
TCP is a streaming byte protocol with no inherent message boundaries (framing). Protocols must use delimiters (like CRLF) or length prefixes to determine where messages begin and end.

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
See [code/tcp_kv_server.py](../code/tcp_kv_server.py).

## Use Redis
Execute the lesson experiment:
```bash
./phases/03-make-the-key-value-store-a-server/experiments/run_experiment.sh
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
1. Why does a space-separated protocol fail if the value being stored is a JSON blob containing spaces and newlines?
2. What happens if a TCP packet arrives fragmented into two separate network chunks?

## When to use this
* Use custom TCP socket servers only when exploring low-level networking primitives or embedded protocols.

## When not to use this
* Never invent custom text protocols for production databases when battle-tested binary-safe protocols like RESP exist.

## What comes next
Proceed to the next phase to build upon these systems primitives.
