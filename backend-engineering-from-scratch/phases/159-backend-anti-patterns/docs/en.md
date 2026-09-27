# Lesson 159: Backend Anti-Patterns

> **Motto**: Cataloging fatal backend anti-patterns provides a comprehensive diagnostic reference for preventing common architectural failures.

---

## Motto
"Cataloging fatal backend anti-patterns provides a comprehensive diagnostic reference for preventing common architectural failures."

## Problem
Repeating historical backend mistakes (business logic in controllers, N+1 queries, global connections) causes recurring outages.

## Prediction
Reviewing the top 25 backend anti-patterns and their verified remedies transforms engineers into defensive architects.

## Why this matters
Knowing what NOT to do is just as important as knowing what to build.

## First principles
Anti-Pattern -> Concrete Failure Mode under Load -> Verified Mechanical Remedy.

## Mental model
```text
Anti-Pattern: Global Unpooled DB Connection -> Failure: Crashes under 10 concurrent requests -> Remedy: Bounded Connection Pool
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Architectural review and code auditing guidelines.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/159-backend-anti-patterns/tests/ -v
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
- **Failure Injection**: Audit a codebase containing 5 deliberate anti-patterns (N+1 query, un-timeouted call, business logic in route, etc.).
- Execute the experiment script:
```bash
python phases/159-backend-anti-patterns/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Flag each anti-pattern, reproduce the specific failure mode under load, and apply the verified mechanical fix.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Never use global mutable state in web applications: process memory is not shared across replicas or thread-safe.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Never swallow exceptions silently with empty `except:` blocks; always log tracebacks with correlation IDs.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Never return HTTP 200 OK for requests that experienced an operational error.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What are the top 5 most destructive backend anti-patterns encountered in production?
2. Why is placing business rules directly inside route handlers considered an architectural anti-pattern?
3. Why is swallowing exceptions with empty `except Exception: pass` blocks catastrophic for production observability?

## What comes next
Having understood backend anti-patterns, we next discover its inherent boundaries and transition to **Debugging Lab: Slow API**.
