# Exercise Q101: Q101 Gaps And Islands Consecutive Days

**Tier:** Advanced  
**Target Schema:** `analytics`  
**Concept Tags:** `Gaps and Islands`, `Date Arithmetic`  

---

## 1. Business Requirement

> Identify consecutive active login days for user 101: group consecutive days into islands by subtracting ROW_NUMBER() days from event date. Project island_start, island_end, streak_length. Order by island_start ASC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: island_start, island_end, streak_length

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
python3 scripts/grade-query.py exercises/advanced/q101-gaps-and-islands-consecutive-days.md
```
