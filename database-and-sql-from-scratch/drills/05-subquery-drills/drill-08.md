# Drill 08: Set Operation: UNION ALL vs UNION

**Category:** 05-subquery-drills  
**Target Schema:** `social`  
**Concept:** Fluency Drill  

---

## Business Requirement

> Combine unique user IDs who have either authored a post or authored a comment. Return distinct user_id. Order by user_id ASC.

---

## 14-Question Thinking Anchor
- **What should one output row represent (Grain)?**  
  *One row per active content creator user.*

---

## Target Verification
When your query is ready, verify it against the test harness:

```bash
python3 scripts/grade-query.py drills/05-subquery-drills/drill-08.md
```
