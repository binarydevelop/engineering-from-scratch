# Drill 06: Social Mutual Follow Join

**Category:** 01-join-drills  
**Target Schema:** `social`  
**Concept:** Fluency Drill  

---

## Business Requirement

> Find all mutual follows (where user A follows user B and user B follows user A). Return user_a_id and user_b_id where user_a_id < user_b_id. Order by user_a_id, user_b_id.

---

## 14-Question Thinking Anchor
- **What should one output row represent (Grain)?**  
  *One row per mutual friendship pair.*

---

## Target Verification
When your query is ready, verify it against the test harness:

```bash
python3 scripts/grade-query.py drills/01-join-drills/drill-06.md
```
