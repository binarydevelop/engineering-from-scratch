# Lesson 160: Debugging Lab: Slow API

> **Motto**: Investigating an API where p99 latency doubled while CPU remains normal requires inspecting database table scans.

---

## Motto
"Investigating an API where p99 latency doubled while CPU remains normal requires inspecting database table scans."

## Problem
When an API slows down under low CPU, engineers guess blindly, optimizing Python code while the database is scanning millions of rows.

## Prediction
Using `EXPLAIN ANALYZE` and query logs isolates missing indexes and full table scans as the true root cause.

## Why this matters
Diagnosing slow APIs methodically restores performance in minutes rather than days of trial and error.

## First principles
Symptom: Latency p99 = 3.5s, CPU = 8%. Investigation: Trace -> Slow SQL query -> EXPLAIN ANALYZE -> Missing Index found!

## Mental model
```text
Alert: Slow API (p99 3.5s) -> Inspect Trace -> Slow Query: SELECT WHERE status='active' -> Seq Scan -> Add Index -> p99 drops to 4ms
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Database query profiling and index optimization.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/160-debugging-lab-slow-api/tests/ -v
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
- **Failure Injection**: Run load against the slow API; observe p99 latency exceeds 2,500ms while host CPU is < 10%.
- Execute the experiment script:
```bash
python phases/160-debugging-lab-slow-api/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Inspect SQL execution plan; identify `Seq Scan` on 200,000 rows; add B-Tree index; verify p99 latency drops to 5ms.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: High latency combined with low CPU is a classic signature of I/O wait, database lock contention, or network timeouts.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Never add indexes blindly: analyze query filter predicates and verify index selectivity.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Always verify query performance with realistic dataset sizes: queries that run in 1ms on 100 rows take 2s on 1M rows.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What operational conclusion should you draw when API latency is high but server CPU utilization is low?
2. How does `EXPLAIN ANALYZE` reveal whether a query is performing a sequential scan versus an index scan?
3. Why do database performance bottlenecks frequently escape detection during local development with small test datasets?

## What comes next
Having understood debugging lab: slow api, we next discover its inherent boundaries and transition to **Debugging Lab: 500 Errors**.
