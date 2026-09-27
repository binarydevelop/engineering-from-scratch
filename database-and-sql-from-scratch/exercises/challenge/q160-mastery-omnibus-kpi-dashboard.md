# Exercise Q160: Q160 Mastery Omnibus Kpi Dashboard

**Tier:** Challenge  
**Target Schema:** `ecommerce`  
**Concept Tags:** `Mastery`, `Omnibus Reporting`  

---

## 1. Business Requirement

> Final challenge: produce an executive KPI summary with: total_customers, total_orders, total_gross_revenue, total_refunded, net_revenue, average_order_value, repeat_customer_rate_pct.

---

## 2. Expected Output Shape

- **Result Grain:** 1 row: total_customers, total_orders, gross_revenue, total_refunded, net_revenue, aov, repeat_customer_rate_pct

---

## 3. Query Thinking Framework Checklist

Before writing SQL, answer these questions:
1. What should one row represent in your output?
2. Which tables hold the primary facts and attributes?
3. What is the join cardinality? (1:1, 1:N, N:M)
4. Are any rows eliminated by NULL handling or outer joins?
5. Is an explicit `ORDER BY` necessary for deterministic result verification?

---

## 4. Verification

Execute your query and grade it against the reference solution:

```bash
python3 scripts/grade-query.py exercises/challenge/q160-mastery-omnibus-kpi-dashboard.md
```
