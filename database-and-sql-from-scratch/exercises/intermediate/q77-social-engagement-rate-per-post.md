# Exercise Q77: Q77 Social Engagement Rate Per Post

**Tier:** Intermediate  
**Target Schema:** `social`  
**Concept Tags:** `Social`, `Ratios`  

---

## 1. Business Requirement

> For each post, calculate total likes and total comments. Compute engagement score: (likes * 2 + comments * 3). Project post_id, author_id, likes, comments, score. Order by score DESC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: post_id, user_id, likes_count, comments_count, engagement_score

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
python3 scripts/grade-query.py exercises/intermediate/q77-social-engagement-rate-per-post.md
```
