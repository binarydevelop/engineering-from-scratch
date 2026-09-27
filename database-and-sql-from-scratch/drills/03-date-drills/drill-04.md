# Drill 04: Age and Interval Calculation

**Category:** 03-date-drills  
**Target Schema:** `social`  
**Concept:** Fluency Drill  

---

## Business Requirement

> Calculate the duration in hours between post created_at and the first comment created_at for post id = 1. Return post_id and duration_hours (rounded to 2 decimal places).

---

## 14-Question Thinking Anchor
- **What should one output row represent (Grain)?**  
  *One row for post 1.*

---

## Target Verification
When your query is ready, verify it against the test harness:

```bash
python3 scripts/grade-query.py drills/03-date-drills/drill-04.md
```
