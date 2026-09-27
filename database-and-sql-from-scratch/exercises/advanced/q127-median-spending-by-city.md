# Exercise Q127: Q127 Median Spending By City

**Tier:** Advanced  
**Target Schema:** `ecommerce`  
**Concept Tags:** `Window`, `Median`  

---

## 1. Business Requirement

> Calculate median order total per shipping city. Join orders, addresses. Project city, median_spent. Order by median_spent DESC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: city, median_spent

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
python3 scripts/grade-query.py exercises/advanced/q127-median-spending-by-city.md
```
