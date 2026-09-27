# Lesson Template: System Design From Scratch

# [Phase Number]: [Lesson Title]

> **Motto**: Understand it. Derive it. Build it. Measure it. Break it. Scale it. Recover it. Ship it.

---

## 1. Problem
*Describe the concrete architectural challenge or operational bottleneck that demands attention.*

## 2. Requirements
### Functional
- *What must the system do?*
### Non-Functional
- *Scale, latency SLAs, durability, availability target.*
### Out of Scope
- *What are we intentionally ignoring in this phase?*

## 3. Prediction
*State your hypothesis before running experiments or writing code: What component will fail first under load?*

## 4. Estimates & Back-of-the-Envelope
- **DAU / Users**:
- **Read / Write QPS**:
- **Storage per day / 5 years**:
- **Bandwidth (Ingress / Egress)**:
- **Memory / Cache Sizing**:

## 5. Why This Matters
*Why does this design decision matter in high-scale production systems?*

## 6. First Principles
*The foundational OS, networking, or database theorems (Little's Law, Amdahl's Law, CAP, PACELC, ACID).*

## 7. Simplest Design
*The minimal working architecture (usually one machine, one database).*

```text
[Client] ──▶ [App Server] ──▶ [Database]
```

## 8. Build / Simulate It
*Description of `code/main.py` implementation.*

## 9. Measure It
*Metrics, latency percentiles (p50, p95, p99), and throughput under baseline traffic.*

## 10. Break It
*Failure injection experiment: simulated network delay, server crash, or database lock contention.*

## 11. Bottleneck Observation
*Where did saturation appear first? (CPU, Memory, Disk IOPS, DB Connections, Network).*

## 12. Evolve the Architecture
*How we relieve the measured bottleneck by introducing a specific architectural mechanism.*

```text
[Client] ──▶ [Load Balancer] ──┬──▶ [App A] ──┬──▶ [Primary DB]
                               └──▶ [App B] ──┴──▶ [Cache]
```

## 13. Failure Modes
*What new failure mode did the added component introduce?*

## 14. Consistency Model
*What consistency guarantees are maintained? (Strong, Eventual, Read-Your-Writes).*

## 15. Observability
*RED metrics, structured logs, and distributed trace context required to monitor this system.*

## 16. Security
*Authentication, authorization, and data-in-transit / data-at-rest encryption boundaries.*

## 17. Cost Analysis
*Compute, memory, network transit, and storage financial tradeoffs.*

## 18. Tradeoffs
*List at least two architectural costs or drawbacks of this design.*

## 19. Alternative Design
*What simpler or alternative approach could be used, and why was it not chosen?*

## 20. Evidence
*Empirical output log recorded in `outputs/evidence-template.md`.*

## 21. Questions for Mastery
- *Deep situational questions verifying conceptual command.*

## 22. What Comes Next
*The logical transition to the next phase.*
