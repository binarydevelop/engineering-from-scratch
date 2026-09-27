# Exercise Q123: Q123 Funnel Drop Off Percentage

**Tier:** Advanced  
**Target Schema:** `analytics`  
**Concept Tags:** `Funnel`, `Drop-Off`  

---

## 1. Business Requirement

> Calculate the conversion percentage from page_view to purchase per acquisition campaign. Join campaigns, sessions, events. Order by conversion_rate DESC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: campaign_name, views, purchases, conversion_rate

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
python3 scripts/grade-query.py exercises/advanced/q123-funnel-drop-off-percentage.md
```
