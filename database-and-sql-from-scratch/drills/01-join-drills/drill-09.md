# Drill 09: Join with Aggregated Subquery

**Category:** 01-join-drills  
**Target Schema:** `ecommerce`  
**Concept:** Fluency Drill  

---

## Business Requirement

> Join customers to their total lifetime spent on completed orders. Only include customers who spent > $500. Order by total spent descending.

---

## 14-Question Thinking Anchor
- **What should one output row represent (Grain)?**  
  *One row per customer spending > $500.*

---

## Target Verification
When your query is ready, verify it against the test harness:

```bash
python3 scripts/grade-query.py drills/01-join-drills/drill-09.md
```
