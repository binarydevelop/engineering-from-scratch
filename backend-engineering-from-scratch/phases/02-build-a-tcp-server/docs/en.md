# Lesson 02: Build a TCP Server

> **Motto**: Before HTTP exists, there is only a stream of ordered, reliable bytes delivered over a TCP socket.

---

## Motto
"Before HTTP exists, there is only a stream of ordered, reliable bytes delivered over a TCP socket."

## Problem
Engineers assume HTTP is a fundamental primitive rather than text framed over a raw TCP byte stream.

## Prediction
A raw socket server listening on a port can accept a connection, read bytes, and echo a response.

## Why this matters
Understanding the TCP stream explains why network packets can arrive fragmented or concatenated.

## First principles
TCP is a stream protocol, not a message protocol; there are no message boundaries in TCP.

## Mental model
```text
Client Socket -> TCP SYN/ACK -> Server socket.accept() -> recv(1024) -> sendall()
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Asyncio protocol / Uvicorn transport layer handling raw TCP connections.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/02-build-a-tcp-server/tests/ -v
```

## Inspect it
Observe state directly using operating system, network, or database inspection:
- Inspect raw bytes, socket buffers, or table schemas
- Verify that request transformations match protocol specifications

## Measure it
Quantify latency and resource consumption:
- Measure response latency percentiles (p50, p95, p99)
- Profile memory allocations and database connection usage under load

## Break it
Inject an intentional failure to observe divergence from expected behavior:
- **Failure Injection**: Client sends data in two separate packets or closes connection unexpectedly.
- Execute the experiment script:
```bash
python phases/02-build-a-tcp-server/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Server handles ConnectionResetError and detects zero-byte recv as EOF.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Implement structured byte framing (length prefix or delimiter) over the stream.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Slowloris attack: clients open sockets and send bytes at 1 byte/minute, exhausting file descriptors.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: OS file descriptor limits (`ulimit -n`) determine maximum concurrent TCP connections.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why does socket.recv(1024) not guarantee reading 1024 bytes?
2. What does socket.recv() returning b'' (empty bytes) signify?
3. What is the TCP 3-way handshake and when does accept() return?

## What comes next
Having understood build a tcp server, we next discover its inherent boundaries and transition to **Build a Minimal HTTP Server**.
