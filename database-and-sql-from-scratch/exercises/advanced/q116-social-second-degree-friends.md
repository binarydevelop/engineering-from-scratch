# Exercise Q116: Q116 Social Second Degree Friends

**Tier:** Advanced  
**Target Schema:** `social`  
**Concept Tags:** `Social Graph`, `Graph Traversal`  

---

## 1. Business Requirement

> Find 'Friends of Friends' (second degree follows) for user 1: people followed by people user 1 follows, who user 1 does not already follow. Project recommended_user_id. Order by recommended_user_id ASC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: recommended_user_id

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
python3 scripts/grade-query.py exercises/advanced/q116-social-second-degree-friends.md
```
