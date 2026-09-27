# Exercise Q134: Q134 Consecutive Active Days Islands

**Tier:** Challenge  
**Target Schema:** `analytics`  
**Concept Tags:** `Gaps and Islands`, `Mastery`  

---

## 1. Business Requirement

> Find all users who were active for at least 3 consecutive days in January 2026. Project user_id, streak_start, streak_end, streak_days. Order by user_id ASC, streak_start ASC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: user_id, streak_start, streak_end, streak_days

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
python3 scripts/grade-query.py exercises/challenge/q134-consecutive-active-days-islands.md
```
