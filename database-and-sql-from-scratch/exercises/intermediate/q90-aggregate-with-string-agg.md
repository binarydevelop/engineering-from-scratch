# Exercise Q90: Q90 Aggregate With String Agg

**Tier:** Intermediate  
**Target Schema:** `ecommerce`  
**Concept Tags:** `PostgreSQL Specific`, `STRING_AGG`  

---

## 1. Business Requirement

> For each completed order, aggregate product names into a single comma-separated string aliased as product_list. Order by order_id ASC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: order_id, product_list

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
python3 scripts/grade-query.py exercises/intermediate/q90-aggregate-with-string-agg.md
```
