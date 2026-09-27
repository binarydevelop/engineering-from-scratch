# Lesson 10: Introduce Web Framework

> **Motto**: A web framework is not new networking magic; it is ergonomic scaffolding over sockets, HTTP parsing, and routing.

---

## Motto
"A web framework is not new networking magic; it is ergonomic scaffolding over sockets, HTTP parsing, and routing."

## Problem
Learners start with frameworks and confuse framework conventions with networking fundamentals.

## Prediction
Having built sockets, parsing, and routing from scratch, framework code becomes transparent.

## Why this matters
Framework abstractions provide productivity, but debugging production anomalies requires knowing what lies beneath.

## First principles
Frameworks wrap ASGI/WSGI specifications, converting environment dictionaries to Python objects.

## Mental model
```text
Raw Socket -> ASGI Server (Uvicorn) -> Scope/Receive/Send -> Framework (FastAPI) -> Handler
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: FastAPI application demonstrating how high-level decorators map to ASGI events.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/10-introduce-web-framework/tests/ -v
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
- **Failure Injection**: Inspect raw ASGI scope dictionary directly; observe type, method, headers, and client IP.
- Execute the experiment script:
```bash
python phases/10-introduce-web-framework/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Verify that FastAPI handler arguments are populated directly from the ASGI scope.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Structure framework application cleanly with routers, settings, and life-cycle management.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Framework defaults often enable permissive features (docs in production, unconstrained CORS) that must be hardened.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Framework overhead is usually 1-5ms; the majority of backend latency is spent in DB queries and network I/O.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What is the ASGI specification and why does it use scope, receive, and send?
2. How does FastAPI map a path parameter to a function argument under the hood?
3. Why is framework convenience NOT a substitute for understanding HTTP?

## What comes next
Having understood introduce web framework, we next discover its inherent boundaries and transition to **Request Validation**.
