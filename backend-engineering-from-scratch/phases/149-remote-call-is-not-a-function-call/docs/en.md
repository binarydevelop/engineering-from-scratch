# Lesson 149: Remote Call Is Not a Function Call

> **Motto**: A remote network call can hang, drop packets, time out, or fail partially; treating it like a local function call causes disaster.

---

## Motto
"A remote network call can hang, drop packets, time out, or fail partially; treating it like a local function call causes disaster."

## Problem
The Fallacies of Distributed Computing: assuming the network is reliable, latency is zero, and bandwidth is infinite.

## Prediction
Injecting latency, dropped packets, and HTTP 500 errors into remote calls proves why distributed calls require defensive design.

## Why this matters
Network calls fail in ways local memory never can: partial execution, silent drops, and ambiguous timeouts.

## First principles
Local Call: Memory pointer, instant, succeeds or raises exception. Remote Call: Packets traverse routers, switches, firewalls, and may disappear.

## Mental model
```text
Local: res = calculate() [Instant, Infallible] | Remote: res = http.post() [Can Hang 30s! Can Drop! Can Charge Twice!]
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Resilience patterns wrapping remote service calls.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/149-remote-call-is-not-a-function-call/tests/ -v
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
- **Failure Injection**: Simulate a network partition where the remote server executes the mutation but the response packet is dropped by a router.
- Execute the experiment script:
```bash
python phases/149-remote-call-is-not-a-function-call/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Observe that the caller experiences a timeout and cannot determine whether the remote operation succeeded or failed.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Every remote network call must have a timeout, error classification, and idempotency protection.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Never perform remote network calls inside tight loops: batch calls or redesign data access patterns.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Ambiguity is the fundamental challenge of distributed systems: did the request fail before or after execution?
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What are the 8 Fallacies of Distributed Computing?
2. Why does a network timeout create an ambiguous state where the caller cannot know if the operation succeeded?
3. How do idempotency keys resolve the ambiguity of remote call network timeouts?

## What comes next
Having understood remote call is not a function call, we next discover its inherent boundaries and transition to **Distributed Transaction Problem**.
