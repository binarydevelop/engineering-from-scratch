# Exercise Q124: Q124 Social Network Influence Score

**Tier:** Advanced  
**Target Schema:** `social`  
**Concept Tags:** `Graph`, `Influence`  

---

## 1. Business Requirement

> Calculate PageRank-style simplified influence score: user's follower count + total likes received across all authored posts. Project user_id, username, score. Order by score DESC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: user_id, username, influence_score

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
python3 scripts/grade-query.py exercises/advanced/q124-social-network-influence-score.md
```
