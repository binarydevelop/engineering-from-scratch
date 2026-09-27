# Exercise Q114: Q114 Banking Optimistic Locking Verification

**Tier:** Advanced  
**Target Schema:** `banking`  
**Concept Tags:** `Concurrency`, `Optimistic Lock`  

---

## 1. Business Requirement

> Simulate optimistic lock verification: write a conditional query checking account balance >= 500 and version = 12 before allowing an update. Project id, balance, version, is_updatable.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: id, balance, version, is_updatable

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
python3 scripts/grade-query.py exercises/advanced/q114-banking-optimistic-locking-verification.md
```
