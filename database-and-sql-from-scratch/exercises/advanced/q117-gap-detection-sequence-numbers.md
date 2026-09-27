# Exercise Q117: Q117 Gap Detection Sequence Numbers

**Tier:** Advanced  
**Target Schema:** `banking`  
**Concept Tags:** `Gaps`, `Sequence Integrity`  

---

## 1. Business Requirement

> Detect any missing IDs in a sequence: generate integer sequence from 1 to 10 and identify which IDs do not exist in accounts table. Return missing_id. Order by missing_id ASC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: missing_id

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
python3 scripts/grade-query.py exercises/advanced/q117-gap-detection-sequence-numbers.md
```
