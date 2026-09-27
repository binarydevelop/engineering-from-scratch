# Exercise Q32: Q32 Left Join Null Detection

**Tier:** Beginner  
**Target Schema:** `ecommerce`  
**Concept Tags:** `JOIN`, `LEFT JOIN`  

---

## 1. Business Requirement

> Left join customers to orders. Find rows where order id is NULL (customers with no orders). Project customer id, email. Order by customer id ASC.

---

## 2. Expected Output Shape

- **Result Grain:** 2 rows, 2 columns: id, email

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
python3 scripts/grade-query.py exercises/beginner/q32-left-join-null-detection.md
```
