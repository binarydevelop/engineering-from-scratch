# Drill 09: Set Operation: EXCEPT (Active Users with No Posts)

**Category:** 05-subquery-drills  
**Target Schema:** `social`  
**Concept:** Fluency Drill  

---

## Business Requirement

> Find users who have liked a post, EXCEPT users who have authored a post. Return user_id. Order by user_id ASC.

---

## 14-Question Thinking Anchor
- **What should one output row represent (Grain)?**  
  *One row per qualifying user.*

---

## Target Verification
When your query is ready, verify it against the test harness:

```bash
python3 scripts/grade-query.py drills/05-subquery-drills/drill-09.md
```
