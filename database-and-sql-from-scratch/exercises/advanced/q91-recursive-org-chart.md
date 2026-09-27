# Exercise Q91: Q91 Recursive Org Chart

**Tier:** Advanced  
**Target Schema:** `ecommerce`  
**Concept Tags:** `Recursive CTE`, `Tree Traversal`  

---

## 1. Business Requirement

> Traverse the category hierarchy recursively to calculate category depth (root = 0, child = 1). Return id, name, depth. Order by depth ASC, id ASC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: id, name, depth

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
python3 scripts/grade-query.py exercises/advanced/q91-recursive-org-chart.md
```
