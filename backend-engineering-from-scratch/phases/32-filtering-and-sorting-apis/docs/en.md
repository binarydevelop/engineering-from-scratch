# Lesson 32: Filtering and Sorting APIs

> **Motto**: Filtering and sorting allow clients to query specific subsets of data without exposing the database to SQL injection.

---

## Motto
"Filtering and sorting allow clients to query specific subsets of data without exposing the database to SQL injection."

## Problem
Accepting raw column names from query parameters directly into SQL `ORDER BY` causes severe SQL injection.

## Prediction
Whitelisting sortable fields and validating filter operators prevents injection and guarantees query optimization.

## Why this matters
Well-designed query parameters provide powerful API ergonomics while protecting database performance.

## First principles
Untrusted Query Parameters -> Whitelist Validation -> Safe Query Builder -> Indexed SQL Execution.

## Mental model
```text
GET /items?sort=-created_at&status=active -> Validate 'created_at' in ALLOWED_FIELDS -> ORDER BY created_at DESC
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: FastAPI query parameter dependencies validating sort fields and filter criteria.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/32-filtering-and-sorting-apis/tests/ -v
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
- **Failure Injection**: Submit a query parameter containing SQL injection: `?sort=id;DROP TABLE users;`.
- Execute the experiment script:
```bash
python phases/32-filtering-and-sorting-apis/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Query builder detects unwhitelisted sort parameter and returns HTTP 422 / 400 Bad Request.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Map public API sort field names to internal database column names to avoid exposing internal schema details.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: SQL injection via ORDER BY cannot be stopped by parameter placeholders in standard SQL drivers; whitelisting is mandatory.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Allowing arbitrary filtering on non-indexed columns causes full table scans; index filtered columns.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why can SQL parameter placeholders (`?` or `%s`) NOT be used for table or column names in ORDER BY clauses?
2. How does a whitelist of allowed sort fields eliminate SQL injection vulnerabilities?
3. What performance problem occurs when clients filter by unindexed database columns?

## What comes next
Having understood filtering and sorting apis, we next discover its inherent boundaries and transition to **Search Basics**.
