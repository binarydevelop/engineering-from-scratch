# Lesson 181: Project: Real-Time Chat Backend

> **Motto**: Build a scalable real-time chat backend with WebSockets, room broadcasting, message persistence, and presence tracking.

---

## Motto
"Build a scalable real-time chat backend with WebSockets, room broadcasting, message persistence, and presence tracking."

## Problem
Polling HTTP endpoints for new chat messages creates massive latency, battery drain, and server connection exhaustion.

## Prediction
Using WebSockets with in-memory connection registries and Redis pub/sub broadcasting delivers messages in single-digit milliseconds.

## Why this matters
Real-time chat backends power collaborative tools, customer support widgets, and interactive multiplayer applications.

## First principles
WebSocket Connect -> Auth -> Join Room. Message Sent -> Persist in SQL -> Broadcast to Room Connections via Redis Pub/Sub.

## Mental model
```text
Client A ──[WebSocket Frame: 'Hello']──> Server Node 1 ──[Redis Pub/Sub]──> Server Node 2 ──[WebSocket Frame]──> Client B
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Real-time WebSocket chat and collaboration backend.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/181-project-real-time-chat-backend/tests/ -v
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
- **Failure Injection**: Connect 4 concurrent WebSocket clients across 2 chat rooms; broadcast messages; verify room isolation.
- Execute the experiment script:
```bash
python phases/181-project-real-time-chat-backend/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Verify messages are persisted to SQL database for historical retrieval; verify presence updates on client disconnect.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Authenticate WebSocket connections during the initial HTTP upgrade handshake using secure query tokens or tickets.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Implement ping/pong heartbeat frames to detect dead client connections and clean up memory registries.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Scaling WebSockets across multiple server replicas requires broadcasting messages through a shared Redis Pub/Sub cluster.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. How does the WebSocket protocol provide persistent, full-duplex communication over a single TCP connection?
2. Why does scaling a real-time WebSocket backend across multiple server nodes require a shared message broker like Redis Pub/Sub?
3. How does a real-time server detect when a client connection drops silently without sending a close frame?

## What comes next
Having understood project: real-time chat backend, we next discover its inherent boundaries and transition to **Project: Rate Limiting Service**.
