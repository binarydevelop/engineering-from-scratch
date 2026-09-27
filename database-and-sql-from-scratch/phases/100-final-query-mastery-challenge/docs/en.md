# Phase 100: Final Query Mastery Challenge (50 Comprehensive Problems)

> **Motto:** Understand it. Model it. Query it. Inspect it. Measure it. Break it. Fix it. Optimize it. Ship it.

**Type:** Capstone Verification & Query Mastery  
**Primary Engine:** PostgreSQL 16.4  
**Target Schemas:** `ecommerce`, `social`, `saas`, `banking`, `analytics`  
**Prerequisites:** Phases 00 through 99  
**Estimated Time:** ~6 hours of independent query design  

---

## 1. Overview & Guidelines

This capstone challenge contains **50 realistic, rigorous business and engineering SQL problems**. Solutions are NOT provided inline in this document; you must independently apply the **14-Question Query Thinking Framework**, construct the queries, and verify them against the database.

Reference solutions for this challenge set can be inspected in [`solutions/challenge/`](../../../solutions/challenge/) and graded with `python3 scripts/grade-query.py`.

---

## 2. The 50 Mastery Requirements

1. **User First Purchase:** Find the timestamp and order ID of each user's very first completed order.
2. **Rapid Repurchase:** Find customers whose second completed order occurred within 30 days of their first order.
3. **Rolling 7-Day Revenue:** Calculate the 7-day rolling revenue window for every calendar day in January 2026 without gaps.
4. **Top 3 Products Monthly:** Find the top 3 highest revenue products for each product category during each calendar month.
5. **Consecutive Login Streaks:** Identify all users who were active for at least 5 consecutive calendar days.
6. **Monthly Cohort Retention:** Build a monthly cohort retention table tracking user activity in Month 0, Month 1, and Month 2.
7. **Sustained Spending Increase:** Find customers whose monthly spending increased for three consecutive months.
8. **Duplicate Payment Deduplication:** Identify duplicate completed payments for the same order, keeping only the newest valid record.
9. **Conversion Funnel Progression:** Calculate conversion rates through the funnel: `page_view` -> `sign_up` -> `add_to_cart` -> `purchase`.
10. **Median Order Value:** Calculate the 50th percentile (median) and 95th percentile order amounts across all completed transactions.
11. **Zero-Order Customers (Anti-Join):** Identify all registered customers who have never placed any orders.
12. **Unsold Inventory Analysis:** Find all products that have never appeared in any order item line.
13. **Customer Lifetime Revenue (LTV):** Rank all customers by their total completed order value using `DENSE_RANK()`.
14. **Average Order Value (AOV) by Category:** Compute average order value grouped by top-level product category.
15. **Payment Method Market Share:** Calculate the percentage of total gross merchandise value processed by each payment method.
16. **Refund Loss Percentage:** Determine the exact percentage of completed order revenue that was subsequently refunded.
17. **Top 2 Categories per Customer:** For each customer, determine the two product categories they have spent the most money on.
18. **Average Time Between Orders:** For customers with 3 or more orders, compute the average elapsed days between their successive orders.
19. **Social Mutual Follows:** Find all pairs of users who mutually follow each other without duplicate inverse pairs.
20. **Second-Degree Friend Recommendations:** Recommend users to follow based on "friends of friends" whom the user does not currently follow.
21. **Post Engagement Rate:** Compute an engagement score per post: `(likes * 2) + (comments * 3)`.
22. **Lurker User Percentage:** Calculate the percentage of total registered users who have never authored a post or comment.
23. **SaaS MRR by Plan Tier:** Aggregate Monthly Recurring Revenue (MRR) grouped by subscription plan tier (`starter`, `pro`, `enterprise`).
24. **SaaS Seat Utilization:** Identify organizations where member count exceeds 80% of purchased subscription seats.
25. **Churn Risk Detection:** Find active subscriptions where the organization has logged zero events in the last 30 days.
26. **JSONB Feature Extraction:** Extract deployment duration from `deploy.succeeded` events and compute the 99th percentile latency.
27. **Double-Entry General Ledger Balance:** Prove that total ledger debits exactly equal total ledger credits across all accounts.
28. **Running Account Balance Audit:** Recalculate each account's running balance from raw ledger history and verify against `accounts.balance`.
29. **Optimistic Locking Guard:** Write a conditional transaction query that verifies account `version` before executing a debit.
30. **High-Risk Financial Audits:** Find accounts with `risk_score > 75` holding checking balances exceeding $1,000.
31. **Category Breadcrumb Paths:** Using a Recursive CTE, build the full hierarchical taxonomy path for all categories.
32. **Category Tree Depth:** Compute the maximum depth of the category hierarchy tree.
33. **Monthly Active Users (MAU):** Calculate distinct active users per calendar month across all event streams.
34. **Session Duration Distribution:** Compute average session duration in minutes grouped by device type (`mobile`, `desktop`, `tablet`).
35. **Campaign Customer Acquisition Cost:** Join marketing campaigns, sessions, and orders to compute cost per acquiring customer.
36. **Multi-Touch Marketing Attribution:** Identify the first marketing campaign that touched each customer prior to their first order.
37. **High-Velocity Debits:** Detect accounts that experienced 2 or more debit transactions within a 15-minute window.
38. **Inventory Stockout Forecast:** Estimate days until stockout based on 30-day historical sales velocity.
39. **Customer Recency, Frequency, Monetary (RFM):** Build an RFM segmentation query bucketing customers into loyalty tiers.
40. **Pareto 80/20 Analysis:** Identify what percentage of top customers generate 80% of total company revenue.
41. **Pivoted Monthly Status Report:** Pivot order counts for 2026 into columns: `completed`, `refunded`, `cancelled`, and `pending`.
42. **Keyset Cursor Pagination Step:** Fetch the next 10 orders following cursor `(order_date, id)` in constant $O(\log N)$ time.
43. **Gaps and Islands (Machine Uptime):** Identify uninterrupted periods of consecutive daily event activity.
44. **Cross-Sold Product Affinity:** Determine which pairs of products are most frequently co-purchased in the same order.
45. **Day 1 and Day 7 Retention:** Calculate the percentage of new signups that return on Day 1 and Day 7.
46. **Safe Upsert Simulation:** Write an idempotent query that updates an existing user profile or inserts if absent.
47. **Order Size Bucketing:** Group orders into custom brackets (`< $50`, `$50-$250`, `$250-$1000`, `> $1000`) and sum revenue per bracket.
48. **Rank Shifters MoM:** Identify products whose revenue ranking improved the most from January to February 2026.
49. **Inactivity Interval Length:** Find the longest gap in days between purchases for every repeat customer.
50. **Executive KPI Omnibus Card:** Produce a single-row executive dashboard with total customers, orders, GMV, net revenue, and AOV.
