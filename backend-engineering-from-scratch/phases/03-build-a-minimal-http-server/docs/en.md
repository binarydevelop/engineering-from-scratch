# Lesson 03: Build a Minimal HTTP Server

> **Motto**: HTTP/1.1 is plain text structured by CRLF delimiters framing a request line, headers, and an optional body.

---

## Motto
"HTTP/1.1 is plain text structured by CRLF delimiters framing a request line, headers, and an optional body."

## Problem
Frameworks hide the raw HTTP protocol, making status codes and headers feel arbitrary.

## Prediction
Reading raw bytes from a TCP socket and parsing the first line will extract the HTTP method and path.

## Why this matters
Debugging proxy errors and header corruptions requires seeing the raw ASCII protocol.

## First principles
HTTP is an application-layer request-response protocol defined in RFC 9110 and RFC 9112.

## Mental model
```text
Raw Socket Bytes -> Split on CRLF (\r\n\r\n) -> Request-Line + Headers + Body -> Formatted HTTP Response
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Python http.server and ASGI server raw scope translation.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/03-build-a-minimal-http-server/tests/ -v
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
- **Failure Injection**: Send malformed HTTP request without CRLF delimiters or invalid method.
- Execute the experiment script:
```bash
python phases/03-build-a-minimal-http-server/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Parser handles MalformedHTTPException and responds with HTTP 400 Bad Request.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Implement robust byte stream buffering and length verification.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Header injection: CRLF characters in untrusted input can split headers and inject rogue responses.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Reverse proxies normalize HTTP requests to protect application backends from smuggling attacks.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What is the exact purpose of the double CRLF (\r\n\r\n) sequence?
2. What happens if Content-Length does not match the actual byte count in the body?
3. What are the three components of an HTTP request line?

## What comes next
Having understood build a minimal http server, we next discover its inherent boundaries and transition to **HTTP Request Lifecycle**.
