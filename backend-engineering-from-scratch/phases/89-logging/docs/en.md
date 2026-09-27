# Lesson 89: Logging

> **Motto**: Structured JSON logging records timestamped events with rich contextual metadata, turning logs into searchable telemetry.

---

## Motto
"Structured JSON logging records timestamped events with rich contextual metadata, turning logs into searchable telemetry."

## Problem
Writing plain text logs like `print(f'User {id} logged in')` makes automated log parsing, indexing, and alerting impossible.

## Prediction
Emitting structured JSON logs with standardized fields allows centralized platforms (Elasticsearch, Loki) to filter instantly.

## Why this matters
Logs are the primary forensic audit trail for diagnosing production errors and security incidents.

## First principles
Unstructured: 'Error 500 in order' -> Structured: `{"timestamp": "...", "level": "ERROR", "request_id": "...", "user_id": 42}`.

## Mental model
```text
Application Event -> Log Formatter (JSON) -> Standard Out -> Log Collector (Fluentbit) -> Search Index
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Python standard library `logging` configured with JSON formatters and structlog.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/89-logging/tests/ -v
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
- **Failure Injection**: Log an event containing a user dictionary with a 'password' and 'credit_card' field.
- Execute the experiment script:
```bash
python phases/89-logging/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Verify that the secret redaction filter automatically scrubs sensitive fields to `[REDACTED]` before writing.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Always log to `stdout`/`stderr` in containerized environments; let container runtimes handle log shipping (12-Factor).
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Never log secrets, API keys, bearer tokens, passwords, or sensitive PII to application logs.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: High-volume logging can degrade CPU and disk I/O; use asynchronous logging handlers for high-throughput services.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why is structured JSON logging preferred over unstructured text logging in distributed systems?
2. How does automated secret redaction prevent accidental credential leakage in log aggregation platforms?
3. Why does the 12-Factor App methodology mandate writing logs to standard output (stdout)?

## What comes next
Having understood logging, we next discover its inherent boundaries and transition to **Correlation / Request IDs**.
