# Exercise Q108: Q108 Percentile Disc Cont Postgres

**Tier:** Advanced  
**Target Schema:** `ecommerce`  
**Concept Tags:** `PostgreSQL Specific`, `PERCENTILE_CONT`  

---

## 1. Business Requirement

> Compute the exact 50th percentile (median) and 90th percentile of completed order amounts using PostgreSQL's WITHIN GROUP clause.

---

## 2. Expected Output Shape

- **Result Grain:** 1 row: median_order_val, p90_order_val

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
python3 scripts/grade-query.py exercises/advanced/q108-percentile-disc-cont-postgres.md
```
