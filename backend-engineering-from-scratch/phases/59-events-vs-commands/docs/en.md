# Lesson 59: Events vs Commands

> **Motto**: Commands request an action with an expected outcome; Events publish an immutable fact about something that has already occurred.

---

## Motto
"Commands request an action with an expected outcome; Events publish an immutable fact about something that has already occurred."

## Problem
Conflating commands and events couples services tightly, making asynchronous architectures brittle and confusing.

## Prediction
Using commands for directed actions (`SendEmailCommand`) and events for notifications (`OrderPlaced`) clarifies intent.

## Why this matters
Clear semantics allow microservices to react to domain state changes without knowing who produced them.

## First principles
Command: Directed to one recipient, can be rejected. Event: Broadcast to zero or more listeners, immutable history.

## Mental model
```text
Command: [Client] ──> DoThisCommand ──> [Target Service] | Event: [Order Service] ──> OrderPlaced ──> [Multiple Observers]
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Event-driven architecture messaging schemas in Python services.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/59-events-vs-commands/tests/ -v
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
- **Failure Injection**: Send a Command to multiple handlers (semantic error) vs broadcast an Event to multiple subscribers.
- Execute the experiment script:
```bash
python phases/59-events-vs-commands/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Observe that commands must target exactly one handler, while events cleanly support multiple decoupled subscribers.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Name events in the past tense (`OrderCreated`, `PaymentCaptured`, `UserRegistered`).
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Never include sensitive credentials or raw passwords inside broadcast domain event payloads.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Events enable decoupled event-driven architectures where new features can be added without modifying publishers.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What is the mechanical and conceptual difference between a Command and a Domain Event?
2. Why should domain events always be named in the past tense (e.g. `OrderPlaced`)?
3. Why must a Command have exactly one designated recipient while an Event can have many?

## What comes next
Having understood events vs commands, we next discover its inherent boundaries and transition to **Domain/Application Events**.
