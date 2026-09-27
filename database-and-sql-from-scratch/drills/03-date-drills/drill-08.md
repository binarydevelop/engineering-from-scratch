# Drill 08: Filtering with SARGable Date Boundaries

**Category:** 03-date-drills  
**Target Schema:** `ecommerce`  
**Concept:** Fluency Drill  

---

## Business Requirement

> Select orders created in February 2026 using an index-friendly (sargable) range comparison. Order by order_date ASC.

---

## 14-Question Thinking Anchor
- **What should one output row represent (Grain)?**  
  *One row per February order.*

---

## Target Verification
When your query is ready, verify it against the test harness:

```bash
python3 scripts/grade-query.py drills/03-date-drills/drill-08.md
```
