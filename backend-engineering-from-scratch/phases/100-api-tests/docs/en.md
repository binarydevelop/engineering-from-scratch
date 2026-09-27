# Lesson 100: API Tests

> **Motto**: API tests exercise the complete HTTP stack: routing, validation, middleware, authentication, and response status.

---

## Motto
"API tests exercise the complete HTTP stack: routing, validation, middleware, authentication, and response status."

## Problem
Unit testing handlers in isolation misses middleware ordering bugs, JSON deserialization failures, and CORS errors.

## Prediction
Sending real HTTP requests through an ASGI test client verifies end-to-end request-response contract compliance.

## Why this matters
API tests guarantee that the external interface delivered to frontend and mobile clients functions correctly.

## First principles
HTTP Client -> ASGI Transport -> Middleware -> Router -> Validation -> Service -> Response Serialization -> Assert Status/Headers.

## Mental model
```text
Test Client -> POST /orders (Headers, JSON) -> Full Application Pipeline -> Assert 201 Created & JSON Response DTO
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: FastAPI `TestClient` and HTTPX asynchronous ASGI test harnesses.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/100-api-tests/tests/ -v
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
- **Failure Injection**: Send an API request with an invalid Bearer token; assert that middleware catches error and returns HTTP 401.
- Execute the experiment script:
```bash
python phases/100-api-tests/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Send an API request with valid payload; assert response status is 201 Created and response headers match contract.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Test both the happy path and negative error cases (400, 401, 403, 404, 422) for every endpoint.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Assert on response header security: verify `X-Content-Type-Options` and `Content-Type` are correctly set.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: API tests should test against contract boundaries (DTOs), treating internal implementation as an opaque system.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What defects can an API test catch that isolated unit tests will completely miss?
2. How does `httpx.AsyncClient` test FastAPI applications in-memory without binding physical network ports?
3. Why should every endpoint have tests for both valid data (2xx) and malformed data (4xx)?

## What comes next
Having understood api tests, we next discover its inherent boundaries and transition to **Test Containers / Disposable Dependencies**.
