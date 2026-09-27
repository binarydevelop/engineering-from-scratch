# Lesson 87: Server-Sent Events

> **Motto**: Server-Sent Events (SSE) provide lightweight, unidirectional text streaming from server to client over standard HTTP connections.

---

## Motto
"Server-Sent Events (SSE) provide lightweight, unidirectional text streaming from server to client over standard HTTP connections."

## Problem
Using WebSockets for simple one-way notification feeds introduces unnecessary protocol complexity and custom framing.

## Prediction
SSE streams plain text events (`text/event-stream`) over standard HTTP, with native browser auto-reconnect and firewall compatibility.

## Why this matters
SSE is the ideal, simple transport for LLM token streaming, live sports scores, and real-time status notifications.

## First principles
HTTP/1.1 200 OK \r\n Content-Type: text/event-stream \r\n\r\n data: hello \r\n\r\n data: world \r\n\r\n

## Mental model
```text
Client GET /events -> Server keeps HTTP connection open -> Streams 'data: {event}\n\n' -> Client EventSource receives
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: FastAPI StreamingResponse with `media_type='text/event-stream'`.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/87-server-sent-events/tests/ -v
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
- **Failure Injection**: Connect cURL to the SSE endpoint; observe real-time events stream line-by-line as they occur on the server.
- Execute the experiment script:
```bash
python phases/87-server-sent-events/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Disconnect client and reconnect with `Last-Event-ID` header; verify server resumes event stream from the missed event.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Include `id:` and `retry:` fields in SSE streams to enable automated browser client reconnection and stream resumption.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Unlike WebSockets, SSE works seamlessly through corporate proxies, firewalls, and standard HTTP/2 multiplexing.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: SSE is strictly unidirectional (server-to-client); client interactions must use standard HTTP POST requests.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What is the difference between Server-Sent Events (SSE) and WebSockets?
2. How does the `Last-Event-ID` header enable automatic stream resumption in SSE?
3. Why is SSE preferred over WebSockets for streaming AI / LLM token responses?

## What comes next
Having understood server-sent events, we next discover its inherent boundaries and transition to **Long Polling**.
