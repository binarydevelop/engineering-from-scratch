# Lesson 01: What Is a Backend?

> **Motto**: A backend is a reliable networked state machine that enforces business invariants and coordinates persistence across untrusted networks.

---

## Motto
"A backend is a reliable networked state machine that enforces business invariants and coordinates persistence across untrusted networks."

## Problem
Developers confuse knowing a web framework syntax with understanding backend engineering responsibilities.

## Prediction
A backend must accept untrusted input, enforce domain rules, manage state safely, and return predictable responses.

## Why this matters
Framework code changes frequently; the responsibility of state safety and reliability never changes.

## First principles
Clients are untrusted; databases are persistent; the backend is the authoritative arbiter of business correctness.

## Mental model
```text
Untrusted Client -> Network -> Backend Gateway -> Auth -> Domain Rules -> Storage
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: FastAPI router handling business transactions against a database repository.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/01-what-is-a-backend/tests/ -v
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
- **Failure Injection**: Client submits negative monetary amount or bypasses UI checks.
- Execute the experiment script:
```bash
python phases/01-what-is-a-backend/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Backend catches invariant failure and rejects with HTTP 422 / domain error.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Enforce invariants in pure domain entities independent of UI or client assumptions.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Never trust client-side validation; every rule must be re-verified at the backend boundary.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Stateless application servers scale horizontally; stateful persistence requires explicit coordination.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why can client-side validation never replace backend validation?
2. What distinguishes an application service from a domain invariant?
3. What happens when two backend replicas try to update state simultaneously?

## What comes next
Having understood what is a backend?, we next discover its inherent boundaries and transition to **Build a TCP Server**.
