# Lesson 131: Audit Logging

> **Motto**: Audit logs provide an immutable, append-only historical record of who performed what action on which resource and when.

---

## Motto
"Audit logs provide an immutable, append-only historical record of who performed what action on which resource and when."

## Problem
Application debug logs are rotated and deleted; without audit logs, security investigations cannot determine who altered data.

## Prediction
Recording security-critical actions (privilege escalation, payment refunds, record deletions) in dedicated audit stores satisfies compliance.

## Why this matters
Audit logs establish non-repudiation and enable forensic reconstruction of data breaches and administrative abuse.

## First principles
Audit Record: Actor (Who), Action (What), Resource (Target), Timestamp (When), IP/Client (Origin), Result (Success/Fail).

## Mental model
```text
Admin Action (Refund $500) -> Emit Immutable Audit Event -> Append to Tamper-Evident Audit Log Table / S3 Archive
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Audit trail interceptors in application services.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/131-audit-logging/tests/ -v
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
- **Failure Injection**: Execute a sensitive administrative operation (role change); inspect the generated audit log record.
- Execute the experiment script:
```bash
python phases/131-audit-logging/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Verify audit record contains actor ID, target user ID, timestamp, IP address, and cryptographic integrity checksum.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Audit logs must be append-only: database permissions should prevent UPDATE and DELETE operations on audit tables.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Never log sensitive credentials (passwords, encryption keys) inside audit log payloads.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Ship audit logs to write-once-read-many (WORM) storage (AWS S3 Object Lock) for compliance with SOC2 and GDPR.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What is the mechanical difference between operational debug logs and security audit logs?
2. What essential fields must be present in every security audit log record?
3. Why should database permissions prohibit UPDATE and DELETE statements on audit log tables?

## What comes next
Having understood audit logging, we next discover its inherent boundaries and transition to **Multi-Tenancy**.
