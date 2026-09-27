# The System Design Learning Methodology

> **Motto**: Understand it. Derive it. Build it. Measure it. Break it. Scale it. Recover it. Ship it.

System design is not a catalog of famous architectures to be memorized for interviews. It is the disciplined engineering process of translating ambiguous requirements into interacting components, explicitly reasoning about constraints, state, communication, failure modes, consistency, operability, and tradeoffs.

---

## 1. The Core Learning Loop

Every system design inquiry in this curriculum follows the canonical empirical loop:

```text
Requirements
     ↓
Estimate (Numbers & Back-of-the-Envelope)
     ↓
Simple Design (One machine, one database)
     ↓
Build / Simulate (Executable prototype)
     ↓
Measure (Throughput, p50/p95/p99 latency)
     ↓
Break (Inject faults: drop connections, delay replicas)
     ↓
Find Bottleneck (Identify what saturates first)
     ↓
Scale (Introduce the minimal component to relieve pressure)
     ↓
State Tradeoffs (What does the new component cost?)
     ↓
Repeat
```

---

## 2. The Golden Rules of Architectural Thinking

1. **Never Start with the Scalable Architecture**:
   Never begin a whiteboard or design document with a CDN, 4 Microservices, Redis, Kafka, and a sharded database. Always start with **one application server and one database**. Ask: *What breaks first?*

2. **Calculate Before Drawing**:
   Before placing a single component, compute the orders of magnitude:
   - Daily Active Users (DAU) & Requests/user/day
   - Peak factor & Queries Per Second (QPS)
   - Read/write ratio
   - Bandwidth consumption (inbound and outbound)
   - Storage growth per day and per 5 years
   - Cache memory capacity (e.g. 20% of daily read volume)

3. **Every Box Must Justify Its Existence**:
   For every component added to a diagram, you must answer:
   - *Why does this exist?*
   - *What concrete problem appears without it?*
   - *What does it cost in money, memory, and operational burden?*
   - *What new failure mode does it introduce?*
   - *How do we detect when it is degraded?*
   - *What simpler alternative was rejected?*

4. **Distinguish Source of Truth from Derived State**:
   - The primary database is typically the source of truth.
   - Caches, search indexes (Elasticsearch), materialized views, and analytics warehouses are **derived state**.
   - If derived state is corrupted or lost, there must be a deterministic path to reconstruct it from the source of truth.

5. **Distinguish Synchronous from Asynchronous Requirements**:
   - Does the user waiting on the HTTP connection require the side-effect to finish immediately?
   - If yes: keep it on the synchronous critical path.
   - If no (e.g., email notification, analytics tracking, search indexing): decouple it immediately with a durable queue or outbox event.

6. **Treat Failure as Normal System Behavior**:
   Distributed systems do not fail exceptionally; they fail continuously. Networks partition, disks fill up, processes panic, and downstream APIs throttle. A design is incomplete until you can explain how it degrades gracefully under failure.

---

## 3. How to Study Each Phase

For each phase in `phases/`:
1. Read `docs/en.md` to internalize the problem, constraints, and mental model.
2. Review `diagrams/architecture.ascii` to visualize the before-and-after component interaction.
3. Run the prototype in `code/main.py` and inspect the behavior.
4. Execute `experiments/run_experiment.py` to trigger failure injection or benchmark performance.
5. Run `pytest phases/<phase>/tests/` to verify tests pass.
6. Complete `outputs/evidence-template.md` with your own empirical measurements and analysis.
