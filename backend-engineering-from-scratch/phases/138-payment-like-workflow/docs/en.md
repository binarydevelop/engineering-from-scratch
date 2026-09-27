# Lesson 138: Payment-Like Workflow

> **Motto**: Payment workflows require strict state machine modeling, idempotency keys, and explicit reconciliation transitions.

---

## Motto
"Payment workflows require strict state machine modeling, idempotency keys, and explicit reconciliation transitions."

## Problem
Treating payments as simple boolean operations causes double charges, lost payment records, and financial discrepancies.

## Prediction
Modeling payments as an explicit finite state machine (Pending -> Succeeded / Failed / Refunded) guarantees correctness.

## Why this matters
Correct payment architecture ensures financial integrity, supports asynchronous webhooks, and tolerates network drops.

## First principles
States: PENDING -> (Provider Webhook / Response) -> SUCCEEDED | FAILED. SUCCEEDED -> REFUNDED. Invalid transitions blocked.

## Mental model
```text
Create Payment (Pending) ──> Call Gateway with Idempotency Key ──> Webhook Confirms ──> Mark Succeeded (Immutable)
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Financial transaction state management in backend services.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/138-payment-like-workflow/tests/ -v
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
- **Failure Injection**: Attempt an invalid state transition (e.g. refunding a payment that is still in PENDING status).
- Execute the experiment script:
```bash
python phases/138-payment-like-workflow/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: State machine rejects transition with `InvalidStateTransitionError`; database transaction remains uncorrupted.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Financial records must be append-only: never delete or overwrite past payment records; record compensating entries.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Payment webhooks must be idempotent: receiving the same payment confirmation webhook twice must not double-fulfill orders.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Store currency amounts as integers in the smallest unit (e.g. cents) to eliminate floating-point rounding errors.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why should financial and payment amounts never be stored as floating-point numbers in databases?
2. What is an explicit finite state machine and why is it mandatory for payment workflows?
3. How does asynchronous webhook confirmation handle payment gateways that do not return immediate results?

## What comes next
Having understood payment-like workflow, we next discover its inherent boundaries and transition to **File Processing Pipeline**.
