# Drill 01: Basic Inner Join (Orders & Customers)

**Category:** 01-join-drills  
**Target Schema:** `ecommerce`  
**Concept:** Fluency Drill  

---

## Business Requirement

> Select order ID, customer email, and total_amount for all completed orders. Order by order ID ascending.

---

## 14-Question Thinking Anchor
- **What should one output row represent (Grain)?**  
  *One row per completed order.*

---

## Target Verification
When your query is ready, verify it against the test harness:

```bash
python3 scripts/grade-query.py drills/01-join-drills/drill-01.md
```
