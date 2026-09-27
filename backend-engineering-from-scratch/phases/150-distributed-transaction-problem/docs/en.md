# Lesson 150: Distributed Transaction Problem

> **Motto**: ACID transactions cannot span independent network services; distributed consistency requires Sagas and compensating actions.

---

## Motto
"ACID transactions cannot span independent network services; distributed consistency requires Sagas and compensating actions."

## Problem
Attempting to update Service A and Service B atomically without distributed consensus leaves systems in permanently inconsistent states.

## Prediction
Implementing the Saga pattern (choreography or orchestration) executes sequential local transactions paired with compensating actions.

## Why this matters
Sagas provide eventual consistency across microservices without the blocking latency of two-phase commit (2PC).

## First principles
Service A (Local Tx: Create Order) -> Service B (Local Tx: Charge Card FAILS) -> Trigger Compensating Tx on A (Cancel Order).

## Mental model
```text
Step 1: Order Service (Created) -> Step 2: Payment Service (FAILED!) ──[Compensate]──> Order Service marks 'CANCELLED'
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Saga pattern orchestration in distributed Python architectures.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/150-distributed-transaction-problem/tests/ -v
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
- **Failure Injection**: Simulate a failure during the payment step of a multi-service checkout saga.
- Execute the experiment script:
```bash
python phases/150-distributed-transaction-problem/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Observe orchestrator intercepts failure and automatically triggers compensating cancellations across inventory and order services.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Compensating actions must be idempotent: compensating a step twice must leave the system in a consistent cancelled state.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Semantic rollback: compensating actions cannot undo physical time; they apply corrective business operations (e.g. refund).
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Avoid distributed transactions whenever possible by designing aggregate boundaries that fit within a single database.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why cannot standard database ACID transactions cross independent microservice network boundaries?
2. What is the Saga pattern and how do compensating actions simulate a distributed rollback?
3. Why must compensating actions in a Saga be strictly idempotent?

## What comes next
Having understood distributed transaction problem, we next discover its inherent boundaries and transition to **API Gateway Concept**.
