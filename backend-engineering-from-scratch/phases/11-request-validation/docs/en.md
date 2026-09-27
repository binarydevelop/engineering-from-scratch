# Lesson 11: Request Validation

> **Motto**: Validation at the network boundary protects domain logic from malformed, malicious, or nonsensical data.

---

## Motto
"Validation at the network boundary protects domain logic from malformed, malicious, or nonsensical data."

## Problem
Allowing invalid types or boundary violations into service layers causes obscure database crashes and corrupted records.

## Prediction
Validating request bodies against strict schemas guarantees that service logic receives trusted, typed data.

## Why this matters
Boundary validation is the primary line of defense against injection, unexpected nulls, and type confusion.

## First principles
The boundary layer transforms untrusted dynamic payloads into statically verified, typed structures.

## Mental model
```text
Untrusted JSON -> Schema Inspection -> Field Type & Constraint Check -> Validated Domain Input | 422 Error
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Pydantic schema validation using Field(gt=0, max_length=100) and custom validators.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/11-request-validation/tests/ -v
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
- **Failure Injection**: Submit negative quantity, string where integer expected, or missing required field.
- Execute the experiment script:
```bash
python phases/11-request-validation/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Validation catches error and returns HTTP 422 with field-specific failure messages.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Separate syntactic validation (schema format) from domain business validation (inventory available).
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Unbounded string fields can be exploited for database buffer overflows or Denial of Service attacks.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Schema validation should be fast; avoid expensive database queries inside synchronous validators.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What is the difference between syntactic validation and semantic business validation?
2. Why should an API return 422 Unprocessable Entity instead of 400 Bad Request for schema violations?
3. What security risk arises when string fields do not enforce maximum length limits?

## What comes next
Having understood request validation, we next discover its inherent boundaries and transition to **API Contracts**.
