# Lesson 29: N+1 Problem

> **Motto**: The N+1 problem occurs when an application executes 1 query for a parent list followed by N separate queries for related children.

---

## Motto
"The N+1 problem occurs when an application executes 1 query for a parent list followed by N separate queries for related children."

## Problem
Fetching 100 users and iterating to get their orders executes 101 separate database roundtrips, causing latency to skyrocket.

## Prediction
Detecting query counts and using SQL JOINs or eager loading reduces 101 queries to 1 or 2 queries.

## Why this matters
The N+1 query problem is the single most common cause of slow API endpoints in database-backed applications.

## First principles
1 Query for Parent Records + N Queries for Child Records = $O(N)$ Database Network Roundtrips.

## Mental model
```text
Parent: SELECT * FROM users (1 query) -> Loop: SELECT * FROM orders WHERE user_id = ? (N queries! 100 roundtrips!)
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: SQLAlchemy `joinedload` and `selectinload` relationship options.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/29-n-plus-one-problem/tests/ -v
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
- **Failure Injection**: Query an endpoint returning 50 parent entities with unoptimized relationships; count executed SQL statements.
- Execute the experiment script:
```bash
python phases/29-n-plus-one-problem/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Query counter asserts 51 queries executed; response latency exceeds 150ms.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Refactor with `selectinload` or manual JOIN; assert query count drops to 2 and latency drops to 8ms.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: N+1 queries multiply database connection pool checkouts, exhausting connection pools under moderate traffic.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Use query count assertion tools in integration test suites to catch N+1 regressions before deployment.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why does lazy loading relationships in a loop create N+1 database queries?
2. What is the mechanical difference between a joined load and a selectin load?
3. How does an N+1 query vulnerability degrade database connection pool availability?

## What comes next
Having understood n+1 problem, we next discover its inherent boundaries and transition to **Database Migrations**.
