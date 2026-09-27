# Lesson 13: Error Responses

> **Motto**: Predictable, structured error payloads turn baffling client bugs into actionable, machine-readable corrections.

---

## Motto
"Predictable, structured error payloads turn baffling client bugs into actionable, machine-readable corrections."

## Problem
Returning HTML error pages, inconsistent JSON structures, or empty bodies forces clients into brittle error handling.

## Prediction
A standardized error format (RFC 7807 / RFC 9457 Problem Details) gives clients machine-readable codes and human-readable messages.

## Why this matters
Clear error schemas reduce customer support friction, improve client observability, and enable automated retries.

## First principles
Errors are first-class data contracts returned by APIs when preconditions or invariants fail.

## Mental model
```text
Exception Occurs -> Global Error Handler -> Map to HTTP Status -> Construct Standard Problem Details JSON -> Emit Log with Request ID
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: FastAPI custom exception_handlers for HTTPException, RequestValidationError, and unhandled Exception.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/13-error-responses/tests/ -v
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
- **Failure Injection**: Trigger an unexpected unhandled ZeroDivisionError in a route handler.
- Execute the experiment script:
```bash
python phases/13-error-responses/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Handler intercepts 500 error, logs full traceback internally with request ID, and returns sanitized JSON without stack trace.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Include actionable field-level error pointers for validation failures.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Never leak database table names, SQL syntax errors, or server file paths in public error messages.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Error responses must increment monitoring error counters to trigger SLO alerting.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why is RFC 7807 Problem Details preferred over ad-hoc error formats?
2. Why must internal stack traces never be displayed to API clients in production?
3. What role does a request correlation ID play in debugging client-reported errors?

## What comes next
Having understood error responses, we next discover its inherent boundaries and transition to **Middleware From First Principles**.
