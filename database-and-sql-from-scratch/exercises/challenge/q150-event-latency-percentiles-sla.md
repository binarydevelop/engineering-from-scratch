# Exercise Q150: Q150 Event Latency Percentiles Sla

**Tier:** Challenge  
**Target Schema:** `saas`  
**Concept Tags:** `SLA`, `Latency Percentiles`  

---

## 1. Business Requirement

> Calculate p50, p95, and p99 deployment duration in seconds for 'deploy.succeeded' events from JSONB payload. Return p50_sec, p95_sec, p99_sec.

---

## 2. Expected Output Shape

- **Result Grain:** 1 row: p50_sec, p95_sec, p99_sec

---

## 3. Query Thinking Framework Checklist

Before writing SQL, answer these questions:
1. What should one row represent in your output?
2. Which tables hold the primary facts and attributes?
3. What is the join cardinality? (1:1, 1:N, N:M)
4. Are any rows eliminated by NULL handling or outer joins?
5. Is an explicit `ORDER BY` necessary for deterministic result verification?

---

## 4. Verification

Execute your query and grade it against the reference solution:

```bash
python3 scripts/grade-query.py exercises/challenge/q150-event-latency-percentiles-sla.md
```
