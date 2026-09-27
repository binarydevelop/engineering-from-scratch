# Lesson 04.1: Redis Protocol / RESP

## Motto
"In RESP, length prefixes make arbitrary binary data completely safe to frame."

## Problem
How does Redis parse arbitrary binary payloads, image bytes, JSON blobs, and nested arrays without delimiters conflicting with user data?

## Prediction
What does the raw byte string for `SET foo bar` look like on the wire in RESP2?

## Why this matters
Understanding RESP allows you to write custom high-performance clients, debug network sniffers (Wireshark/tcpdump), and understand how Redis pipelines commands.

## First principles
RESP encodes data using type prefixes: `+` Simple String, `-` Error, `:` Integer, `$` Bulk String (length-prefixed), `*` Array (element count). Bulk strings are framed as `$<len>\r\n<data>\r\n`.

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
See [code/resp_codec.py](../code/resp_codec.py).

## Use Redis
Execute the lesson experiment:
```bash
./phases/04-redis-protocol-resp/experiments/run_experiment.sh
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
1. How does RESP distinguish between an empty string and a non-existent (null) key?
2. What are the key additions introduced in RESP3 compared to RESP2?

## When to use this
* Use RESP directly when building lightweight proxy layers, connection pools, or language drivers.

## When not to use this
* Do not manually parse RESP strings in application code; use established client libraries like `redis-py`.

## What comes next
Proceed to the next phase to build upon these systems primitives.
