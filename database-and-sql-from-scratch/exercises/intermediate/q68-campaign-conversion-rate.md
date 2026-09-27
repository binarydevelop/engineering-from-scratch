# Exercise Q68: Q68 Campaign Conversion Rate

**Tier:** Intermediate  
**Target Schema:** `analytics`  
**Concept Tags:** `Analytics`, `Marketing Attribution`  

---

## 1. Business Requirement

> Calculate total sessions initiated and total purchases driven by each marketing campaign. Join campaigns, sessions, events. Order by total_sessions DESC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: campaign_name, total_sessions, purchase_count

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
python3 scripts/grade-query.py exercises/intermediate/q68-campaign-conversion-rate.md
```
