# Lesson 04: Make the Log a Network Service

## Motto
"A local log is an embedded library; a network log is a distributed infrastructure service."

## Problem
In Phase 02 and 03, our `MiniLog` was accessed via direct in-process Python calls (`log.append()`).
In real distributed architectures, producers and consumers run on different machines across the network.
How do we expose the append-only log over TCP sockets without breaking sequentiality?

## Prediction
What happens to incoming concurrent append requests when multiple producer clients connect to a single TCP socket server?

## Why this matters
Understanding the client-server boundary separates protocol serialization from on-disk persistence. Kafka is fundamentally a TCP server accepting binary wire protocols.

## First principles
* **Framed TCP Protocol:** Streaming TCP is a byte stream, not a packet stream. Messages must be length-delimited.
* **Request Dispatching:** The server decodes client commands (`APPEND`, `FETCH`), interacts with the disk log, and returns structured responses.

## Mental model
```text
Producer Process                      Server Process (TCP Port 9999)
┌─────────────────┐  APPEND "hello"  ┌──────────────────────────────┐
│ MiniLog Client  │ ────────────────►│ TCP Socket Acceptor          │
└─────────────────┘                  │    │                         │
                                     │    ▼                         │
Consumer Process                     │ MiniLog Storage (mini_log.dat)
┌─────────────────┐   FETCH from 0   │    │                         │
│ MiniLog Client  │ ────────────────►│    ▼                         │
└─────────────────┘ ◄────────────────┤ Returns: [(0, "hello")]      │
```

## Build it
See [tcp_log_server.py](../code/tcp_log_server.py) and [tcp_log_client.py](../code/tcp_log_client.py).
We implement a lightweight TCP server supporting:
* `APPEND <payload>` -> replies `OFFSET <n>`
* `FETCH <start_offset>` -> replies `RECORDS <json_list>`

## Use Kafka
Kafka implements its own high-performance binary protocol (`ProduceRequest`, `FetchRequest`) over TCP port 9092.

## Inspect it
Use `nc` (netcat) or raw Python sockets to send text commands directly to the server.

## Measure it
Measure latency of network append over TCP vs. local in-process append.

## Break it
Kill the TCP server process while a client is in the middle of sending an append.

## Recover it
Restart the server; verify previous records were persisted to disk and new appends receive the next monotonic offset.

## Modify it
Add a `PING` command to the TCP server to implement a basic healthcheck.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does TCP framing require length prefixes rather than simple newline delimiters when payloads contain arbitrary binary data?
2. What happens if the server crashes after writing to disk but before sending the TCP response to the client?

## Guarantees
* Remote clients can append and fetch records concurrently over standard TCP sockets.

## Non-guarantees
* Our simple TCP server does not implement TLS security, authentication, or multi-broker replication.

## When to use this
* Whenever decoupling producers and consumers across process boundaries.

## When not to use this
* Single-process applications where IPC or in-memory queues have lower latency overhead.

## What comes next
In Phase 05, we expand our single log into multiple named logical streams: Topics.
