# Exercise Q136: Q136 Deduplicate Payments Keep Latest Valid

**Tier:** Challenge  
**Target Schema:** `ecommerce`  
**Concept Tags:** `Data Hygiene`, `Window ROW_NUMBER`  

---

## 1. Business Requirement

> Identify duplicate completed payments for the same order_id: keep the newest record (by created_at, id) and list all duplicate records that should be purged. Project id, order_id, created_at. Order by order_id ASC, id ASC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: id, order_id, created_at

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
python3 scripts/grade-query.py exercises/challenge/q136-deduplicate-payments-keep-latest-valid.md
```
