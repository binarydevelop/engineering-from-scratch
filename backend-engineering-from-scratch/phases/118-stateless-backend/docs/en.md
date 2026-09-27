# Lesson 118: Stateless Backend

> **Motto**: A stateless backend stores zero client session data in process memory, allowing any instance to handle any request.

---

## Motto
"A stateless backend stores zero client session data in process memory, allowing any instance to handle any request."

## Problem
Storing user login sessions or shopping carts in Python memory breaks as soon as a load balancer routes the user to a different server instance.

## Prediction
Offloading sessions, caches, and state to external shared datastores (Redis, PostgreSQL) makes backend instances completely interchangeable.

## Why this matters
Statelessness is the foundational prerequisite for effortless horizontal auto-scaling and cloud-native resilience.

## First principles
Instance A, B, C are completely interchangeable. All shared state lives in Redis / Database.

## Mental model
```text
Request 1 hits Instance A -> Reads state from Redis. Request 2 hits Instance B -> Reads identical state from Redis!
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Stateless FastAPI application integrated with Redis session backend.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/118-stateless-backend/tests/ -v
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
- **Failure Injection**: Send Request 1 to Server Node A (modifies state); send Request 2 to Server Node B (reads state).
- Execute the experiment script:
```bash
python phases/118-stateless-backend/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Assert Server Node B reads the updated state perfectly; demonstrate total instance interchangeability.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Eliminate all in-memory global state: no global user caches, no in-memory session dictionaries, no local file storage.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Stateless instances can be killed, restarted, or auto-scaled by container orchestrators at any second without user impact.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: The only persistent state in a cloud backend exists in databases, object stores, and message queues.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why does storing session state in process memory prevent horizontal scaling across multiple servers?
2. What does it mean for an application server to be 'share-nothing'?
3. Where should state be stored in a horizontally scaled production architecture?

## What comes next
Having understood stateless backend, we next discover its inherent boundaries and transition to **Containerize Backend**.
