# Lesson 61: External Event Broker

> **Motto**: An external event broker enables asynchronous communication and event distribution across independent distributed services.

---

## Motto
"An external event broker enables asynchronous communication and event distribution across independent distributed services."

## Problem
Calling remote microservices synchronously via HTTP for non-critical side effects creates tight coupling and latency chains.

## Prediction
Publishing events to a message broker (Redis Streams, RabbitMQ, Kafka) decouples services in time, space, and availability.

## Why this matters
Event brokers allow independent teams and services to consume data feeds at their own pace without impacting producers.

## First principles
Producer -> Publishes Event to Broker Topic -> Broker Persists -> Consumer A & Consumer B read independently.

## Mental model
```text
Order Service ──[OrderPlaced Event]──> External Broker (Redis Streams/RabbitMQ) ──┬──> Email Service
                                                                                   └──> Analytics Service
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Redis Streams / RabbitMQ publish-subscribe integration.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/61-external-event-broker/tests/ -v
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
- **Failure Injection**: Stop the Email Service consumer; publish 5 events; restart Email Service.
- Execute the experiment script:
```bash
python phases/61-external-event-broker/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Email Service starts up, reads all missed events from the broker topic, and catches up; zero events lost.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Implement consumer groups to allow load-balancing event processing across multiple worker replicas.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Schema evolution: use backward-compatible event schemas (Protobuf, JSON Schema) so old consumers do not crash.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: External brokers add operational overhead; do not introduce Kafka when a modular monolith or simple queue suffices.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. How does an external event broker decouple distributed services in both time and availability?
2. What is a Consumer Group in event streaming platforms like Redis Streams or Kafka?
3. What happens to events published while a consumer service is offline?

## What comes next
Having understood external event broker, we next discover its inherent boundaries and transition to **Transactional Outbox**.
