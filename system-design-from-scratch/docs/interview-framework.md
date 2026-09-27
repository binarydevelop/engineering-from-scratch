# The 45-Minute System Design Interview Framework

A structured guide for navigating standard 45-minute technical architecture interviews.

---

## 1. Pacing & Time Allocation

| Stage | Suggested Time | Core Objectives |
| :--- | :--- | :--- |
| **1. Requirements & Scope** | 00:00 – 05:00 (5 min) | Clarify ambiguity, establish functional & non-functional requirements, state non-goals. |
| **2. Scale & Estimations** | 05:00 – 10:00 (5 min) | Calculate QPS (read/write), storage growth, bandwidth, and cache sizing. |
| **3. API & Data Model** | 10:00 – 16:00 (6 min) | Define HTTP/gRPC interfaces, relational or NoSQL schema, primary keys, and indexes. |
| **4. High-Level Design** | 16:00 – 25:00 (9 min) | Draw the simplest end-to-end architecture (Client $\to$ Gateway $\to$ App $\to$ DB). |
| **5. Deep Dive & Bottlenecks** | 25:00 – 38:00 (13 min) | Scale the bottleneck: caching, sharding, replication, queues, concurrency handling. |
| **6. Resilience & Tradeoffs** | 38:00 – 45:00 (7 min) | Enumerate failure modes, single points of failure, consistency model, and explicit tradeoffs. |

---

## 2. Communication Best Practices

- **Treat it as a Collaborative Discussion**: Do not monologue for 10 minutes. Propose options, state the tradeoffs, and invite the interviewer's perspective:
  > *"We could partition the orders table either by `user_id` or `order_id`. Partitioning by `user_id` optimizes user order history queries, while partitioning by `order_id` balances write distribution. Given our read patterns, I recommend `user_id`. Does that align with our focus?"*
- **Never Draw 20 Boxes Upfront**: Start with the single-server baseline and evolve the architecture under pressure.
- **State the Numbers Explicitly**: Tie every architectural decision to your earlier estimations:
  > *"Because our write QPS is only 150 writes/second, a single primary PostgreSQL instance can easily sustain this. We do not need distributed sharding on Day 1."*

---

## 3. Interview Evaluation Rubric

1. **Problem Navigation**: Did the candidate clarify ambiguous constraints before designing?
2. **Quantitative Reasoning**: Did the candidate use back-of-the-envelope calculations to justify architectural decisions?
3. **Data & API Rigor**: Are schemas normalized/denormalized appropriately for access patterns?
4. **Distributed Systems Knowledge**: Does the candidate understand replication lag, split-brain, cache stampedes, and idempotency?
5. **Tradeoff Awareness**: Does the candidate acknowledge what is lost when choosing a technology?
