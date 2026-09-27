# Exercise Q93: Q93 Window Rank Vs Dense Rank Ties

**Tier:** Advanced  
**Target Schema:** `ecommerce`  
**Concept Tags:** `Window`, `RANK`, `DENSE_RANK`  

---

## 1. Business Requirement

> Demonstrate ties: rank products by price within category 2 using both RANK() and DENSE_RANK(). Project name, price, rnk, dense_rnk. Order by price DESC, name ASC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: name, price, rnk, dense_rnk

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
python3 scripts/grade-query.py exercises/advanced/q93-window-rank-vs-dense-rank-ties.md
```
