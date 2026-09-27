# Exercise Q46: Q46 Distinct On Postgres

**Tier:** Intermediate  
**Target Schema:** `ecommerce`  
**Concept Tags:** `PostgreSQL Specific`, `DISTINCT ON`  

---

## 1. Business Requirement

> Using PostgreSQL's DISTINCT ON, find each customer's single most expensive order. Project customer_id, order_id, total_amount. Order by customer_id ASC, total_amount DESC, id ASC.

---

## 2. Expected Output Shape

- **Result Grain:** 1 customer row per orderer: customer_id, id AS order_id, total_amount

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
python3 scripts/grade-query.py exercises/intermediate/q46-distinct-on-postgres.md
```
