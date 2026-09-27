# Problem: Design a Food Delivery Multi-Actor Workflow

> **Tier**: `ADVANCED`  
> **Scale Baseline**: Saga orchestration coordinating customer, kitchen, courier

---

## 1. Problem Statement & Ambiguous Prompt
Design design a food delivery multi-actor workflow that satisfies enterprise production reliability and operates efficiently under the given scale constraints.

---

## 2. Requirements Gathering & Clarification Questions
- **Clarification 1**: What is the primary user interaction pattern (synchronous API vs async processing)?
- **Clarification 2**: What is the acceptable latency SLA for reads and writes?
- **Clarification 3**: What consistency model does the domain require (Strong vs Eventual)?
- **Non-Goals**: Machine learning ranking algorithms, external billing gateway internals, and frontend rendering details.

---

## 3. Scale Estimations
- **Throughput**: Derive peak QPS using 2.5x multiplier.
- **Storage Growth**: Calculate daily ingestion and 5-year capacity planning.
- **Bandwidth**: Estimate network ingress and egress.
- **Cache Sizing**: Apply 80/20 rule to determine required memory footprint.

---

## 4. Changing Requirements (Mid-Interview Twist)
- *Twist 1*: Traffic suddenly surges by **10x**. What component breaks first and how do you adapt?
- *Twist 2*: The business mandates a strict **RPO = 0** zero-data-loss guarantee across datacenter failures.

---

## 5. Failure Scenarios to Defend Against
- Primary database crashes during peak traffic.
- Hot-key skew targets 25% of all traffic to a single partition.
- Network split-brain occurs between Availability Zones.
