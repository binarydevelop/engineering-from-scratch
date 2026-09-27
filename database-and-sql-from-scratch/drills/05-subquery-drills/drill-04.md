# Drill 04: NOT EXISTS (Customers with No Orders)

**Category:** 05-subquery-drills  
**Target Schema:** `ecommerce`  
**Concept:** Fluency Drill  

---

## Business Requirement

> Find customers who have never placed any orders using NOT EXISTS. Project customer id, first_name, last_name, email. Order by id ASC.

---

## 14-Question Thinking Anchor
- **What should one output row represent (Grain)?**  
  *One row per customer without orders.*

---

## Target Verification
When your query is ready, verify it against the test harness:

```bash
python3 scripts/grade-query.py drills/05-subquery-drills/drill-04.md
```
