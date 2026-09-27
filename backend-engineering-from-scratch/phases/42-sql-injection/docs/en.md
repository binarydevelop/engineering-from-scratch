# Lesson 42: SQL Injection

> **Motto**: SQL injection occurs when untrusted user input is concatenated directly into SQL command strings, altering query semantics.

---

## Motto
"SQL injection occurs when untrusted user input is concatenated directly into SQL command strings, altering query semantics."

## Problem
Concatenating user strings into SQL queries allows attackers to bypass authentication, dump databases, and wipe disks.

## Prediction
Using parameterized queries forces the database engine to treat user input strictly as literal values, never executable syntax.

## Why this matters
SQL injection remains one of the most destructive and prevalent vulnerabilities in backend history.

## First principles
Query String Concatenation = Code & Data Mixed -> Parameterized Query = Code Compiled First, Data Bound Separately.

## Mental model
```text
Vulnerable: `SELECT * WHERE user = '` + input + `'` -> Exploit: `' OR '1'='1` -> Parameterized: Safe parameter binding
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Parameterized query execution across SQLite and PostgreSQL drivers.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/42-sql-injection/tests/ -v
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
- **Failure Injection**: Submit input `' OR '1'='1` against the vulnerable endpoint and dump all user records.
- Execute the experiment script:
```bash
python phases/42-sql-injection/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Observe complete authentication bypass; then apply parameterized queries and observe attack fails safely.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Never use Python f-strings, `%` formatting, or `.format()` to construct SQL queries.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Second-Order SQL Injection occurs when tainted data is stored safely but later read and concatenated into a dynamic query.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: ORM tools use parameterized queries by default, but raw SQL queries inside ORM escapes must be reviewed vigilantly.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why do parameter placeholders (`?` or `%s`) completely eliminate SQL injection?
2. What is Second-Order SQL Injection?
3. Why are dynamic table names and column names in ORDER BY clauses dangerous in SQL queries?

## What comes next
Having understood sql injection, we next discover its inherent boundaries and transition to **CORS**.
