# Exercise Q02: Q02 Project Customer Columns

**Tier:** Beginner  
**Target Schema:** `ecommerce`  
**Concept Tags:** `SELECT`, `Projection`  

---

## 1. Business Requirement

> Select id, email, and full name formatted as first_name || ' ' || last_name aliased as customer_name from customers. Order by id ASC.

---

## 2. Expected Output Shape

- **Result Grain:** 15 rows, 3 columns: id, email, customer_name

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
python3 scripts/grade-query.py exercises/beginner/q02-project-customer-columns.md
```
