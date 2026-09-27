# Lesson 60: Domain/Application Events

> **Motto**: In-process domain events decouple side effects from core entity mutations, keeping business logic clean and focused.

---

## Motto
"In-process domain events decouple side effects from core entity mutations, keeping business logic clean and focused."

## Problem
Adding email sending, analytics logging, and reward point allocation into an Order model creates massive bloat.

## Prediction
Publishing domain events inside the application allows independent event listeners to react without modifying the domain.

## Why this matters
Domain events maintain the Single Responsibility Principle and make extending application features trivial.

## First principles
Order.complete() -> Emits OrderCompletedEvent -> Listeners: EmailService, AnalyticsService, InventoryService.

## Mental model
```text
Order Aggregate -> Emits OrderPlaced -> Event Bus -> [Listener 1: Email] & [Listener 2: Analytics] & [Listener 3: Inventory]
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Domain event publishing integrated with application services.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/60-domain-application-events/tests/ -v
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
- **Failure Injection**: Register a new listener (e.g. AuditLogListener) without modifying a single line of Order domain code.
- Execute the experiment script:
```bash
python phases/60-domain-application-events/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Execute order creation; assert that all registered listeners receive the event and execute successfully.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Handle listener exceptions: decide whether a failing listener should roll back the primary operation or fail safely.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Ensure domain events are published only *after* the primary domain state transaction commits successfully.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: In-process event buses provide modular decoupling before introducing the complexity of external message brokers.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. How do domain events enforce the Single Responsibility Principle in business models?
2. What happens if an in-process event listener raises an unhandled exception?
3. Why should domain events be dispatched after database transaction commitment rather than before?

## What comes next
Having understood domain/application events, we next discover its inherent boundaries and transition to **External Event Broker**.
