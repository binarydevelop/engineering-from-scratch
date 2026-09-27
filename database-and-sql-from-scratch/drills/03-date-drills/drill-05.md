# Drill 05: Date Range Scaffolding with generate_series

**Category:** 03-date-drills  
**Target Schema:** `ecommerce`  
**Concept:** Fluency Drill  

---

## Business Requirement

> Generate all calendar days from '2026-01-01' to '2026-01-05'. Left join to completed orders on that day to show daily order count (0 if none). Order by day ASC.

---

## 14-Question Thinking Anchor
- **What should one output row represent (Grain)?**  
  *One row per calendar day.*

---

## Target Verification
When your query is ready, verify it against the test harness:

```bash
python3 scripts/grade-query.py drills/03-date-drills/drill-05.md
```
