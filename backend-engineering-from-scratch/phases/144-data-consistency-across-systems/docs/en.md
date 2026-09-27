# Lesson 144: Data Consistency Across Systems

> **Motto**: Maintaining consistency across disparate datastores (SQL, Redis, Elasticsearch, Queues) requires clear source-of-truth semantics.

---

## Motto
"Maintaining consistency across disparate datastores (SQL, Redis, Elasticsearch, Queues) requires clear source-of-truth semantics."

## Problem
When an entity is updated, updating SQL, Redis, and Elasticsearch simultaneously across network boundaries leads to state divergence.

## Prediction
Designating a single authoritative source of truth and using asynchronous replication pipelines enforces eventual consistency.

## Why this matters
Mastering cross-system consistency is the hallmark of senior distributed systems engineering.

## First principles
Which system is authoritative? PostgreSQL. How are secondary systems updated? Asynchronously via committed events.

## Mental model
```text
PostgreSQL (Source of Truth) ──┬──> Redis (Cache: Derived)
                                 ├──> Elasticsearch (Search: Derived)
                                 └──> Kafka (Event Log: Derived)
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Event-driven eventual consistency architectures.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/144-data-consistency-across-systems/tests/ -v
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
- **Failure Injection**: Simulate a network split between PostgreSQL and the search index during an update.
- Execute the experiment script:
```bash
python phases/144-data-consistency-across-systems/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Consistency auditor flags discrepancy; healing worker reads authoritative PostgreSQL record and synchronizes search index.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Embrace Eventual Consistency: distributed systems cannot maintain immediate strict consistency across heterogeneous stores without 2PC.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Never allow secondary stores (Redis, Search) to write back to the primary database; data flows strictly in one direction.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Build automated consistency checkers (reconciliation jobs) that run nightly to detect and heal drifting data.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. In a system containing PostgreSQL, Redis, and Elasticsearch, which datastore must be the single source of truth?
2. Why is strict immediate consistency across heterogeneous datastores impossible without catastrophic performance degradation?
3. What is an automated reconciliation job and how does it maintain eventual consistency across distributed systems?

## What comes next
Having understood data consistency across systems, we next discover its inherent boundaries and transition to **Monolith First**.
