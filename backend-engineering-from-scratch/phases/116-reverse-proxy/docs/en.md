# Lesson 116: Reverse Proxy

> **Motto**: A reverse proxy sits in front of application backends to handle TLS termination, request buffering, and static asset delivery.

---

## Motto
"A reverse proxy sits in front of application backends to handle TLS termination, request buffering, and static asset delivery."

## Problem
Exposing Python application servers directly to the public Internet leaves them vulnerable to slow-client attacks and SSL CPU overhead.

## Prediction
Placing Nginx or Caddy in front buffers slow requests, terminates SSL, enforces connection limits, and compresses responses.

## Why this matters
Reverse proxies shield application runtimes, allowing Python processes to focus purely on business logic.

## First principles
Client (Slow mobile Internet) -> Reverse Proxy (Fast RAM buffer) -> Python Backend (Blazing fast local loopback).

## Mental model
```text
Internet Clients ──[HTTPS / TLS 1.3]──> Reverse Proxy (Nginx) ──[HTTP Plaintext / Fast]──> Uvicorn / App Backends
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Nginx / Caddy reverse proxy configuration files.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/116-reverse-proxy/tests/ -v
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
- **Failure Injection**: Send a slow chunked request (Slowloris simulation); observe reverse proxy buffers the entire payload before forwarding to backend.
- Execute the experiment script:
```bash
python phases/116-reverse-proxy/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Inspect backend request headers; verify `X-Forwarded-For`, `X-Forwarded-Proto`, and `Host` headers are accurately set.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Configure `proxy_buffering on` in Nginx to prevent slow clients from tying up backend application worker processes.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Configure `client_max_body_size` in the reverse proxy to drop oversized uploads before they reach application servers.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: In modern cloud architectures, cloud load balancers (AWS ALB, Cloudflare) fulfill the reverse proxy role.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What is the difference between a forward proxy and a reverse proxy?
2. Why is slow-client request buffering in a reverse proxy critical for protecting backend application servers?
3. What purpose do the `X-Forwarded-For` and `X-Forwarded-Proto` headers serve?

## What comes next
Having understood reverse proxy, we next discover its inherent boundaries and transition to **Load Balancing**.
