# Drill 05: Distinct Count Inside Aggregation

**Category:** 02-group-by-drills  
**Target Schema:** `social`  
**Concept:** Fluency Drill  

---

## Business Requirement

> Count how many unique users have liked posts created by user_id = 1. Select post author user_id and unique_likers_count.

---

## 14-Question Thinking Anchor
- **What should one output row represent (Grain)?**  
  *One row for the author user.*

---

## Target Verification
When your query is ready, verify it against the test harness:

```bash
python3 scripts/grade-query.py drills/02-group-by-drills/drill-05.md
```
