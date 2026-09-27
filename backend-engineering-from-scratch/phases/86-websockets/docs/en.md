# Lesson 86: WebSockets

> **Motto**: WebSockets provide full-duplex, persistent TCP communication over a single connection initiated via an HTTP Upgrade handshake.

---

## Motto
"WebSockets provide full-duplex, persistent TCP communication over a single connection initiated via an HTTP Upgrade handshake."

## Problem
Polling an HTTP endpoint every 500ms for chat messages wastes massive bandwidth, battery, and server connection overhead.

## Prediction
Upgrading to a WebSocket connection allows the server to push real-time events to the client with single-digit millisecond latency.

## Why this matters
WebSockets power real-time collaborative editors, live chat systems, trading dashboards, and multiplayer applications.

## First principles
Client sends HTTP Upgrade Request -> Server responds 101 Switching Protocols -> Connection becomes bi-directional binary frame stream.

## Mental model
```text
Client ──[HTTP GET Upgrade: websocket]──> Server ──[101 Switching Protocols]──> Persistent Full-Duplex TCP Socket
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: FastAPI `WebSocket` endpoints and connection manager.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/86-websockets/tests/ -v
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
- **Failure Injection**: Connect 3 concurrent WebSocket clients to a chat room; broadcast a message from one client to all others.
- Execute the experiment script:
```bash
python phases/86-websockets/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Verify all connected clients receive the message instantly; measure frame transmission latency (< 2ms).
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Implement ping/pong heartbeat frames to detect silent TCP half-open connection drops and dead clients.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Authenticate WebSockets during the initial HTTP upgrade handshake before accepting the connection.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Scaling WebSockets across multiple server replicas requires a shared pub/sub message broker (Redis Pub/Sub).
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. How does the HTTP 101 Switching Protocols handshake establish a WebSocket connection?
2. Why do WebSockets require ping/pong heartbeat frames to detect dropped connections?
3. How do multiple backend servers broadcast WebSocket messages to users connected to different server nodes?

## What comes next
Having understood websockets, we next discover its inherent boundaries and transition to **Server-Sent Events**.
