# Drill 10: Full Outer Join (Customers & Addresses)

**Category:** 01-join-drills  
**Target Schema:** `ecommerce`  
**Concept:** Fluency Drill  

---

## Business Requirement

> Perform a FULL OUTER JOIN between customers with id in (14, 15) and addresses. Select customer id, email, and address id. Order by customer id ascending nulls last, address id ascending nulls last.

---

## 14-Question Thinking Anchor
- **What should one output row represent (Grain)?**  
  *One row per combined customer and address record.*

---

## Target Verification
When your query is ready, verify it against the test harness:

```bash
python3 scripts/grade-query.py drills/01-join-drills/drill-10.md
```
