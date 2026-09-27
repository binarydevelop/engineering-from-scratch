# Lesson 81: API Versioning

> **Motto**: API versioning manages breaking contract changes over time without stranding existing mobile apps or third-party integrations.

---

## Motto
"API versioning manages breaking contract changes over time without stranding existing mobile apps or third-party integrations."

## Problem
Modifying an existing endpoint's schema breaks all older mobile app versions currently running on users' phones.

## Prediction
Employing URI versioning (`/v1`, `/v2`) or header-based versioning allows new features while supporting legacy clients.

## Why this matters
Version management enables safe continuous deployment while maintaining backward compatibility guarantees.

## First principles
URI Versioning (`/v1/orders`) vs Header Versioning (`Accept: application/vnd.company.v1+json`) vs Query Param (`?v=1`).

## Mental model
```text
Client A (Legacy Mobile) -> GET /v1/users -> Returns V1 Schema
Client B (New Web App)   -> GET /v2/users -> Returns V2 Schema with new fields
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: FastAPI APIRouter prefix versioning (`prefix='/v1'`).
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/81-api-versioning/tests/ -v
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
- **Failure Injection**: Send requests to `/v1/users` and `/v2/users`; assert that legacy clients receive old schema and new clients receive new schema.
- Execute the experiment script:
```bash
python phases/81-api-versioning/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Verify that both versions delegate to the same underlying domain model without code duplication.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Define explicit deprecation lifecycles: include `Sunset` and `Deprecation` HTTP headers on aging API versions.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Avoid versioning reflexively: additive, non-breaking changes should not trigger a major API version bump.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Maintaining too many active API versions creates technical debt; support at most 2 concurrent major versions.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why do mobile applications make backward-incompatible API changes particularly hazardous?
2. What are the tradeoffs between URI path versioning (`/v1`) and Header-based versioning?
3. What standard HTTP response headers signal to clients that an API version is deprecated?

## What comes next
Having understood api versioning, we next discover its inherent boundaries and transition to **Backward Compatibility**.
