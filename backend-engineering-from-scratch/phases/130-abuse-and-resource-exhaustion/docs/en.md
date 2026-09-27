# Lesson 130: Abuse and Resource Exhaustion

> **Motto**: Resource exhaustion occurs when clients abuse expensive endpoints, huge pagination sizes, or repeated intensive queries.

---

## Motto
"Resource exhaustion occurs when clients abuse expensive endpoints, huge pagination sizes, or repeated intensive queries."

## Problem
Allowing clients to request `limit=100000` or search single-character wildcards forces massive database table scans.

## Prediction
Imposing hard query bounds, pagination caps, and query timeouts prevents abusive queries from starving legitimate users.

## Why this matters
Defensive backend design assumes that clients will probe for expensive, resource-intensive operations.

## First principles
Client Abuse: `GET /search?q=%` or `GET /items?limit=500000` -> Guard Rails enforce limits -> Protects Database.

## Mental model
```text
Abusive Request -> Schema / Query Boundary Guards -> Caps `limit = min(req.limit, 100)` -> Safe Query Executed
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: FastAPI query parameter validation with hard bounds (`Query(le=100)`).
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/130-abuse-and-resource-exhaustion/tests/ -v
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
- **Failure Injection**: Request 50,000 items in a single query; verify API clamps the limit to the configured maximum of 100 items.
- Execute the experiment script:
```bash
python phases/130-abuse-and-resource-exhaustion/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Attempt an expensive unindexed wildcard search (`%`); verify API rejects search with HTTP 400 requiring minimum 3 characters.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Always set database statement timeouts (`statement_timeout = '3s'`) so runaway queries are terminated by PostgreSQL.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Rate-limit computationally expensive endpoints more aggressively than lightweight endpoints.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Protect account enumeration vectors: return identical response times and messages on password reset for existing vs non-existing users.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why should an API silently clamp or reject excessive pagination page size requests (`limit=100000`)?
2. How does configuring a database statement timeout protect against unindexed runaway queries?
3. What is an account enumeration vulnerability and how do you mitigate it on authentication endpoints?

## What comes next
Having understood abuse and resource exhaustion, we next discover its inherent boundaries and transition to **Audit Logging**.
