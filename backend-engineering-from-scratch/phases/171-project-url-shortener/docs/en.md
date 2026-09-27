# Lesson 171: Project: URL Shortener

> **Motto**: Build a high-throughput, low-latency URL shortening service with Base62 encoding, caching, collision handling, and analytics.

---

## Motto
"Build a high-throughput, low-latency URL shortening service with Base62 encoding, caching, collision handling, and analytics."

## Problem
A URL shortener appears trivial, but handling millions of redirects requires sub-millisecond caching and collision resistance.

## Prediction
Implementing Base62 encoding, cache-aside read paths, and asynchronous click analytics builds a production-grade service.

## Why this matters
URL shorteners are the classic system design baseline testing hashing, caching, and read-heavy optimization.

## First principles
POST /shorten (URL) -> Base62 ID -> Store in SQL & Redis. GET /{code} -> Read from Redis (1ms) -> 301/302 Redirect.

## Mental model
```text
Client ──[GET /xyz123]──> Redis Cache ──[HIT in 0.5ms]──> HTTP 302 Redirect to https://destination.com/long-url
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: High-throughput URL redirection service implementation.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/171-project-url-shortener/tests/ -v
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
- **Failure Injection**: Create a short URL; redirect 1,000 times; verify 99% of redirects are served from cache in < 1ms.
- Execute the experiment script:
```bash
python phases/171-project-url-shortener/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Verify analytics click counter increments asynchronously without slowing down redirect responses.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Use HTTP 302 Found (temporary redirect) if you need to track analytics on every click; HTTP 301 is cached by browsers.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Collision handling: if a hash collision occurs on insert, append salt and re-hash until unique.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Rate limit URL creation to prevent spam and malicious link generation.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What is Base62 encoding and why is it preferred over Base64 for URL shortening?
2. Why should an analytics-tracking URL shortener return HTTP 302 Found instead of HTTP 301 Moved Permanently?
3. How does cache-aside with Redis achieve sub-millisecond redirect latency at scale?

## What comes next
Having understood project: url shortener, we next discover its inherent boundaries and transition to **Project: Todo / Task API**.
