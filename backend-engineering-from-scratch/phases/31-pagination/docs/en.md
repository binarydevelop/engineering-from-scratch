# Lesson 31: Pagination

> **Motto**: Returning unbounded lists from database endpoints exhausts server memory, bandwidth, and database disk I/O.

---

## Motto
"Returning unbounded lists from database endpoints exhausts server memory, bandwidth, and database disk I/O."

## Problem
Writing `SELECT * FROM orders` crashes the API when table rows grow from 100 to 1,000,000.

## Prediction
Implementing offset pagination for shallow browsing and keyset/cursor pagination for deep datasets keeps latency bounded.

## Why this matters
Pagination is mandatory for every list endpoint to enforce predictable memory usage and response times.

## First principles
Offset: `LIMIT x OFFSET y` ($O(N)$ scan overhead) vs Keyset: `WHERE id > last_seen_id ORDER BY id LIMIT x` ($O(1)$ index seek).

## Mental model
```text
Offset: DB scans and discards 100,000 rows to return 20 -> Keyset: DB seeks directly to index cursor and reads 20 rows.
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: FastAPI query parameters for `limit` and `cursor` returning structured paginated envelopes.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/31-pagination/tests/ -v
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
- **Failure Injection**: Request page 5,000 using OFFSET 100,000; observe database query duration jump from 2ms to 450ms.
- Execute the experiment script:
```bash
python phases/31-pagination/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Inspect EXPLAIN ANALYZE output; observe full index scan discarding 100,000 rows.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Implement Keyset pagination using indexed cursor IDs; observe query duration remains < 2ms at any depth.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Unbounded pagination requests (`limit=1000000`) allow attackers to trigger Out-Of-Memory denial of service.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Always enforce a hard maximum limit (e.g. `max_limit=100`) regardless of what the client requests.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why does OFFSET 1000000 LIMIT 20 force the database to read and discard 1,000,000 rows?
2. What is Keyset/Cursor pagination and why does it maintain constant-time $O(1)$ performance at any depth?
3. Why should an API always enforce a hard maximum page limit on client requests?

## What comes next
Having understood pagination, we next discover its inherent boundaries and transition to **Filtering and Sorting APIs**.
