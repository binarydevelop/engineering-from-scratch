# Exercise Q120: Q120 Hierarchical Tree Cycle Prevention

**Tier:** Advanced  
**Target Schema:** `ecommerce`  
**Concept Tags:** `Recursive CTE`, `Cycle Prevention`  

---

## 1. Business Requirement

> Write a recursive query with cycle detection tracking array of visited IDs to prevent infinite loops in bad graph data. Project id, name, cycle_detected.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: id, name, cycle_detected

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
python3 scripts/grade-query.py exercises/advanced/q120-hierarchical-tree-cycle-prevention.md
```
