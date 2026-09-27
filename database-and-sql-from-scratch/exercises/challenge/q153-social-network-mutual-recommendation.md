# Exercise Q153: Q153 Social Network Mutual Recommendation

**Tier:** Challenge  
**Target Schema:** `social`  
**Concept Tags:** `Graph`, `Recommendations`  

---

## 1. Business Requirement

> Generate follower recommendations for user 2: rank potential users to follow by the number of mutual followers they share with user 2. Project recommended_user_id, mutual_count. Order by mutual_count DESC, recommended_user_id ASC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: recommended_user_id, mutual_count

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
python3 scripts/grade-query.py exercises/challenge/q153-social-network-mutual-recommendation.md
```
