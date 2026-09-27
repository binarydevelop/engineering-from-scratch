# Lesson 12: API Contracts

> **Motto**: An API contract is a stable, machine-readable agreement between client and server; it must never be coupled to database schemas.

---

## Motto
"An API contract is a stable, machine-readable agreement between client and server; it must never be coupled to database schemas."

## Problem
Directly returning database entities leaks internal columns, password hashes, and breaks clients on schema migrations.

## Prediction
Defining explicit Request and Response DTOs isolates public contracts from internal database changes.

## Why this matters
Independent API contracts allow internal database refactoring without breaking mobile apps or third-party consumers.

## First principles
An API is an external interface; the database schema is an internal storage optimization.

## Mental model
```text
Client Contract (Request DTO) -> Application Service -> Database Entity (SQL) -> Application Service -> Client Contract (Response DTO)
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: FastAPI response_model with Pydantic schemas enforcing output filtering and serialization.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/12-api-contracts/tests/ -v
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
- **Failure Injection**: Add an internal secret column to the database entity and verify it never appears in the API response.
- Execute the experiment script:
```bash
python phases/12-api-contracts/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Inspect serialized API output; confirm internal metadata and hidden fields are completely stripped.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Generate OpenAPI specifications automatically from validated contract schemas.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Mass Assignment Vulnerability: accepting arbitrary request dictionaries into database models allows attackers to overwrite admin flags.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Version API contracts deliberately; never modify existing fields in a backward-incompatible manner.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why should an internal database column name change NEVER break an external API response?
2. What is a Mass Assignment vulnerability and how do DTOs prevent it?
3. How does an explicit response schema prevent accidental data leakage?

## What comes next
Having understood api contracts, we next discover its inherent boundaries and transition to **Error Responses**.
