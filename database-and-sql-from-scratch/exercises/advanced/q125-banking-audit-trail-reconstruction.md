# Exercise Q125: Q125 Banking Audit Trail Reconstruction

**Tier:** Advanced  
**Target Schema:** `banking`  
**Concept Tags:** `Audit`, `JSONB Diff`  

---

## 1. Business Requirement

> Reconstruct entity history from audit_log: for account table changes, extract old balance and new balance from JSONB states. Project record_id, action, timestamp. Order by timestamp ASC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: record_id, action, timestamp

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
python3 scripts/grade-query.py exercises/advanced/q125-banking-audit-trail-reconstruction.md
```
