# Lesson 56: Idempotent Jobs

> **Motto**: An idempotent job can be executed multiple times with the exact same inputs without producing duplicate side effects.

---

## Motto
"An idempotent job can be executed multiple times with the exact same inputs without producing duplicate side effects."

## Problem
In distributed networks, at-least-once message delivery guarantees that jobs will occasionally be delivered twice.

## Prediction
Building idempotency keys and state checks ensures that duplicate job executions do not charge customers twice.

## Why this matters
Idempotent worker execution is mandatory for financial correctness and safe distributed retry architectures.

## First principles
Idempotent: $f(f(x)) = f(x)$. Executing Job(id=42) five times produces the identical result as executing once.

## Mental model
```text
Job Arrives -> Check Execution Record(job_id) -> ALREADY PROCESSED? YES: Skip & ACK | NO: Process, Record ID & ACK
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Distributed idempotency key verification patterns using Redis and relational SQL unique constraints.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/56-idempotent-jobs/tests/ -v
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
- **Failure Injection**: Submit the exact same payment processing task twice to the worker queue simultaneously.
- Execute the experiment script:
```bash
python phases/56-idempotent-jobs/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: First task charges customer and records idempotency key; second task detects existing key and skips execution safely.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Enforce uniqueness at the database layer (UNIQUE constraint on `idempotency_key` or `transaction_id`).
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Race condition: two workers picking up duplicate messages simultaneously must rely on database unique constraints.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Idempotency keys should have a defined retention period (e.g. 24 hours to 7 days) depending on business requirements.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why does distributed network delivery inherently require jobs to be idempotent?
2. How does a UNIQUE database constraint prevent two workers from simultaneously executing a duplicate task?
3. What is the difference between an idempotency key and a primary key?

## What comes next
Having understood idempotent jobs, we next discover its inherent boundaries and transition to **Dead-Letter Queue**.
