# Lesson 105: Database Performance

> **Motto**: Database performance is governed by query execution plans, index usage, and lock contention; EXPLAIN ANALYZE reveals the truth.

---

## Motto
"Database performance is governed by query execution plans, index usage, and lock contention; EXPLAIN ANALYZE reveals the truth."

## Problem
Slow database queries cause 90% of backend latency spikes; writing queries without inspecting plans is flying blind.

## Prediction
Running `EXPLAIN ANALYZE` exposes full sequential table scans, slow nested loops, and missing indexes.

## Why this matters
Adding targeted B-tree or partial indexes transforms $O(N)$ full table scans into $O(\log N)$ index seeks in microseconds.

## First principles
Sequential Scan: Database reads every block on disk ($O(N)$) vs Index Scan: Database traverses B-Tree root to leaf ($O(\log N)$).

## Mental model
```text
Query: SELECT * WHERE user_id = 42 -> Seq Scan on 500,000 rows (350ms) -> CREATE INDEX -> Index Scan (0.2ms! 1750x speedup)
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: PostgreSQL `EXPLAIN (ANALYZE, BUFFERS)` inspection tooling.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/105-database-performance/tests/ -v
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
- **Failure Injection**: Query a table with 100,000 rows on an unindexed foreign key column; measure execution time.
- Execute the experiment script:
```bash
python phases/105-database-performance/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Execution plan shows `Seq Scan` taking 85ms; create B-Tree index; execution plan shows `Index Scan` taking 0.15ms.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Index only what you query: indexes speed up reads but slow down INSERTs and UPDATEs because indexes must be updated.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Over-indexing tables wastes disk storage and degrades write throughput; audit unused indexes periodically.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Use composite indexes for multi-column queries; column order in composite indexes matters (left-to-right matching).
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What is the difference between EXPLAIN and EXPLAIN ANALYZE in SQL databases?
2. Why does adding an index speed up SELECT queries while slowing down INSERT queries?
3. How does column ordering in a composite B-Tree index affect query matching?

## What comes next
Having understood database performance, we next discover its inherent boundaries and transition to **Application Profiling**.
