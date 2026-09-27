# Exercise Q30: Q30 Multi Column Distinct

**Tier:** Beginner  
**Target Schema:** `ecommerce`  
**Concept Tags:** `DISTINCT`, `Multi-Column`  

---

## 1. Business Requirement

> Find all unique combinations of customer_id and status in orders. Order by customer_id ASC, status ASC.

---

## 2. Expected Output Shape

- **Result Grain:** 14 rows, 2 columns: customer_id, status

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
python3 scripts/grade-query.py exercises/beginner/q30-multi-column-distinct.md
```
