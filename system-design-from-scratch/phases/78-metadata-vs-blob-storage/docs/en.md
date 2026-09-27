# Phase 78: Metadata vs Blob Storage Separation

> **Motto**: Understand it. Derive it. Build it. Measure it. Break it. Scale it. Recover it. Ship it.

---

## 1. Problem
Storing structured file attributes in relational DB and binary bytes in object store.

## 2. Requirements

### Functional Requirements
- Accept client requests and execute core domain processing.
- Maintain consistent state transitions and report execution telemetry.
- Expose clear operational status and failure metrics.

### Non-Functional Requirements
- **Availability**: 99.9% baseline SLA.
- **Latency**: Sub-millisecond local in-memory simulation latency; p99 < 50ms under scaled architecture.
- **Resilience**: Survive simulated dependency failures without unhandled process crashes.

### Out of Scope
- Vendor-specific cloud managed service APIs and external infrastructure billing.

---

## 3. Prediction
Before executing experiments, hypothesize:
> *Under peak load or failure injection, what component will saturate or crash first?*

## 4. Estimates & Numbers
- **Target QPS**: 5,000 requests/sec.
- **Peak Factor**: 2.5x (12,500 peak requests/sec).
- **Network Inbound Bandwidth**: 12,500 req/s * 500 bytes = 6.25 MB/s (50 Mbps).
- **Storage Growth**: 25 GB / day; ~45.6 TB / 5 years with 3x replication.

---

## 5. Why This Matters
In production systems, architectural decisions dictate how systems degrade under stress. Understanding this phase ensures you can design systems that survive real-world constraints without premature over-engineering.

---

## 6. First Principles
Separation of concerns: fast structured SQL queries on metadata, scalable blob retrieval.

---

## 7. Simplest Design
Start with the minimal working architecture:

```text
[Client] ──▶ [App Server] ──▶ [Primary Datastore]
```
Description: Storing file metadata and bytes inside the same storage engine.

---

## 8. Build & Simulate It
The accompanying code in `code/main.py` models this subsystem:
- Enforces payload validation and domain constraints.
- Tracks operational metrics (throughput, error count, latency).
- Exposes chaos injection switches.

---

## 9. Measure It
Run baseline performance measurements using `python experiments/run_experiment.py`.
Observe baseline latency, throughput, and error rates.

---

## 10. Break It (Failure Injection)
Querying user file list requires scanning massive disk pages containing image bytes.
Simulate this failure using the chaos switch in `experiments/run_experiment.py`.

---

## 11. Bottleneck Observation
Where does saturation manifest?
- CPU, memory exhaustion, connection starvation, or lock contention.

---

## 12. Evolve the Architecture
To relieve the observed bottleneck, evolve the system:

```text
                               ┌──▶ [Worker Instance 1] ──┬──▶ [Cache]
[Client] ──▶ [Load Balancer] ──┼──▶ [Worker Instance 2] ──┤
                               └──▶ [Worker Instance 3] ──┴──▶ [Primary DB] ──▶ [Replicas]
```
Evolution applied: Relational DB: `(file_id, user_id, size, s3_key, created_at)` + S3: `s3://bucket/s3_key`.

---

## 13. Failure Modes
- New failure mode introduced by the evolved component.
- Mitigation: timeouts, retries with backoff, circuit breaking, or fallbacks.

## 14. Consistency Model
- Guarantees provided (Strong vs Eventual consistency).
- Tradeoffs between immediate consistency and high availability.

## 15. Observability
- **RED Metrics**: Rate (req/s), Errors (count), Duration (p50, p95, p99).
- **Structured Logs**: JSON logs tagged with correlation IDs.

## 16. Security
- Authentication boundaries, input validation, and least privilege access.

## 17. Cost Analysis
- Hardware and cloud resource impact of adding redundancy or caching.

## 18. Architectural Tradeoffs
Requires garbage collection to delete orphaned S3 blobs if metadata write fails.

---

## 19. Alternative Design
What simpler or alternative approach could be used, and why was it not selected?

---

## 20. Evidence
Record your empirical findings in `outputs/evidence-template.md`.

---

## 21. Questions for Mastery
1. What exact metric indicates that this component has reached saturation?
2. How does this architecture behave when a network partition isolates primary nodes?
3. What would you remove if the scale was reduced by 100x?

---

## 22. What Comes Next
Proceed to Phase 79 to build upon these principles.
