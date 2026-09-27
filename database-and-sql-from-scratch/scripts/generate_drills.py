"""
Generator for all 50 SQL Fluency Drills and their matching Reference Solutions.
Categories:
  1. 10 JOIN drills (drills/01-join-drills/)
  2. 10 GROUP BY drills (drills/02-group-by-drills/)
  3. 10 Date/Time drills (drills/03-date-drills/)
  4. 10 Window Function drills (drills/04-window-drills/)
  5. 10 Subquery & CTE drills (drills/05-subquery-drills/)
"""

import os
from pathlib import Path

ROOT = Path("/Users/tushar/Desktop/private/repos/database-and-sql-from-scratch")

DRILLS = [
    # Category 1: JOIN Drills
    {
        "cat": "01-join-drills",
        "num": 1,
        "title": "Basic Inner Join (Orders & Customers)",
        "schema": "ecommerce",
        "req": "Select order ID, customer email, and total_amount for all completed orders. Order by order ID ascending.",
        "grain": "One row per completed order.",
        "sql": """SELECT
    o.id AS order_id,
    c.email,
    o.total_amount
FROM ecommerce.orders o
JOIN ecommerce.customers c ON o.customer_id = c.id
WHERE o.status = 'completed'
ORDER BY o.id ASC;"""
    },
    {
        "cat": "01-join-drills",
        "num": 2,
        "title": "Left Join (Preserving Zero-Order Customers)",
        "schema": "ecommerce",
        "req": "Select customer id, email, and order id for all customers. If a customer has no orders, order id must be NULL. Order by customer id ascending, order id ascending nulls last.",
        "grain": "One row per customer or order item relationship.",
        "sql": """SELECT
    c.id AS customer_id,
    c.email,
    o.id AS order_id
FROM ecommerce.customers c
LEFT JOIN ecommerce.orders o ON c.id = o.customer_id
ORDER BY c.id ASC, o.id ASC NULLS LAST;"""
    },
    {
        "cat": "01-join-drills",
        "num": 3,
        "title": "Multi-Table Join (Order -> Items -> Products)",
        "schema": "ecommerce",
        "req": "Select order_id, product name, quantity, and unit_price for order 1. Order by product name ascending.",
        "grain": "One row per line item in order 1.",
        "sql": """SELECT
    oi.order_id,
    p.name AS product_name,
    oi.quantity,
    oi.unit_price
FROM ecommerce.order_items oi
JOIN ecommerce.products p ON oi.product_id = p.id
WHERE oi.order_id = 1
ORDER BY p.name ASC;"""
    },
    {
        "cat": "01-join-drills",
        "num": 4,
        "title": "Self-Join (Category Hierarchy)",
        "schema": "ecommerce",
        "req": "Select child category name and its parent category name. Only include categories that have a parent. Order by child name ascending.",
        "grain": "One row per subcategory with a parent.",
        "sql": """SELECT
    c.name AS subcategory_name,
    p.name AS parent_category_name
FROM ecommerce.categories c
JOIN ecommerce.categories p ON c.parent_id = p.id
ORDER BY c.name ASC;"""
    },
    {
        "cat": "01-join-drills",
        "num": 5,
        "title": "Filtering on Left-Joined Table (Preserving Left Rows)",
        "schema": "ecommerce",
        "req": "Select customer email and completed order count. All customers must appear, even if count is 0. Order by order count descending, customer email ascending.",
        "grain": "One row per customer.",
        "sql": """SELECT
    c.email,
    COUNT(o.id) AS completed_order_count
FROM ecommerce.customers c
LEFT JOIN ecommerce.orders o
    ON c.id = o.customer_id
    AND o.status = 'completed'
GROUP BY c.id, c.email
ORDER BY completed_order_count DESC, c.email ASC;"""
    },
    {
        "cat": "01-join-drills",
        "num": 6,
        "title": "Social Mutual Follow Join",
        "schema": "social",
        "req": "Find all mutual follows (where user A follows user B and user B follows user A). Return user_a_id and user_b_id where user_a_id < user_b_id. Order by user_a_id, user_b_id.",
        "grain": "One row per mutual friendship pair.",
        "sql": """SELECT
    f1.follower_id AS user_a_id,
    f1.following_id AS user_b_id
FROM social.follows f1
JOIN social.follows f2
    ON f1.follower_id = f2.following_id
    AND f1.following_id = f2.follower_id
WHERE f1.follower_id < f1.following_id
ORDER BY user_a_id ASC, user_b_id ASC;"""
    },
    {
        "cat": "01-join-drills",
        "num": 7,
        "title": "Cross Join (All Categories x Product Statuses)",
        "schema": "ecommerce",
        "req": "Cross join root categories (parent_id IS NULL) with two statuses ('active', 'inactive'). Project category name and status. Order by category name, status.",
        "grain": "One row per category-status permutation.",
        "sql": """SELECT
    c.name AS category_name,
    s.status
FROM ecommerce.categories c
CROSS JOIN (VALUES ('active'), ('inactive')) AS s(status)
WHERE c.parent_id IS NULL
ORDER BY category_name ASC, status ASC;"""
    },
    {
        "cat": "01-join-drills",
        "num": 8,
        "title": "Left Anti-Join (Unsold Products)",
        "schema": "ecommerce",
        "req": "Find products that have NEVER been ordered. Select product id, sku, and name. Order by product id ascending.",
        "grain": "One row per unsold product.",
        "sql": """SELECT
    p.id,
    p.sku,
    p.name
FROM ecommerce.products p
LEFT JOIN ecommerce.order_items oi ON p.id = oi.product_id
WHERE oi.id IS NULL
ORDER BY p.id ASC;"""
    },
    {
        "cat": "01-join-drills",
        "num": 9,
        "title": "Join with Aggregated Subquery",
        "schema": "ecommerce",
        "req": "Join customers to their total lifetime spent on completed orders. Only include customers who spent > $500. Order by total spent descending.",
        "grain": "One row per customer spending > $500.",
        "sql": """SELECT
    c.id AS customer_id,
    c.email,
    tot.total_spent
FROM ecommerce.customers c
JOIN (
    SELECT customer_id, SUM(total_amount) AS total_spent
    FROM ecommerce.orders
    WHERE status = 'completed'
    GROUP BY customer_id
    HAVING SUM(total_amount) > 500
) tot ON c.id = tot.customer_id
ORDER BY tot.total_spent DESC;"""
    },
    {
        "cat": "01-join-drills",
        "num": 10,
        "title": "Full Outer Join (Customers & Addresses)",
        "schema": "ecommerce",
        "req": "Perform a FULL OUTER JOIN between customers with id in (14, 15) and addresses. Select customer id, email, and address id. Order by customer id ascending nulls last, address id ascending nulls last.",
        "grain": "One row per combined customer and address record.",
        "sql": """SELECT
    c.id AS customer_id,
    c.email,
    a.id AS address_id
FROM (SELECT * FROM ecommerce.customers WHERE id IN (14, 15)) c
FULL OUTER JOIN ecommerce.addresses a ON c.id = a.customer_id
ORDER BY customer_id ASC NULLS LAST, address_id ASC NULLS LAST;"""
    },

    # Category 2: GROUP BY Drills
    {
        "cat": "02-group-by-drills",
        "num": 1,
        "title": "Basic Count per Group",
        "schema": "ecommerce",
        "req": "Count number of products in each category_id. Project category_id and product_count. Order by product_count DESC, category_id ASC.",
        "grain": "One row per category_id.",
        "sql": """SELECT
    category_id,
    COUNT(*) AS product_count
FROM ecommerce.products
GROUP BY category_id
ORDER BY product_count DESC, category_id ASC;"""
    },
    {
        "cat": "02-group-by-drills",
        "num": 2,
        "title": "Multi-Column Aggregation (Sum and Avg)",
        "schema": "ecommerce",
        "req": "Calculate total revenue and average order amount for completed orders by customer_id. Order by total revenue DESC.",
        "grain": "One row per customer with completed orders.",
        "sql": """SELECT
    customer_id,
    SUM(total_amount) AS total_revenue,
    ROUND(AVG(total_amount), 2) AS avg_order_amount
FROM ecommerce.orders
WHERE status = 'completed'
GROUP BY customer_id
ORDER BY total_revenue DESC;"""
    },
    {
        "cat": "02-group-by-drills",
        "num": 3,
        "title": "Group By with HAVING Filter",
        "schema": "ecommerce",
        "req": "Find customers who have placed 2 or more completed orders. Return customer_id and order_count. Order by order_count DESC, customer_id ASC.",
        "grain": "One row per qualifying customer.",
        "sql": """SELECT
    customer_id,
    COUNT(*) AS order_count
FROM ecommerce.orders
WHERE status = 'completed'
GROUP BY customer_id
HAVING COUNT(*) >= 2
ORDER BY order_count DESC, customer_id ASC;"""
    },
    {
        "cat": "02-group-by-drills",
        "num": 4,
        "title": "Conditional Aggregation with CASE",
        "schema": "ecommerce",
        "req": "For each customer_id with orders, calculate total count of completed orders and count of cancelled/refunded orders. Order by customer_id ASC.",
        "grain": "One row per customer.",
        "sql": """SELECT
    customer_id,
    COUNT(CASE WHEN status = 'completed' THEN 1 END) AS completed_orders,
    COUNT(CASE WHEN status IN ('cancelled', 'refunded') THEN 1 END) AS bad_orders
FROM ecommerce.orders
GROUP BY customer_id
ORDER BY customer_id ASC;"""
    },
    {
        "cat": "02-group-by-drills",
        "num": 5,
        "title": "Distinct Count Inside Aggregation",
        "schema": "social",
        "req": "Count how many unique users have liked posts created by user_id = 1. Select post author user_id and unique_likers_count.",
        "grain": "One row for the author user.",
        "sql": """SELECT
    p.user_id AS author_id,
    COUNT(DISTINCT l.user_id) AS unique_likers_count
FROM social.posts p
JOIN social.likes l ON p.id = l.post_id
WHERE p.user_id = 1
GROUP BY p.user_id;"""
    },
    {
        "cat": "02-group-by-drills",
        "num": 6,
        "title": "SaaS Seat Usage by Organization",
        "schema": "saas",
        "req": "For each organization, calculate total active memberships and compare against seats purchased. Project org name, used_seats, purchased_seats. Order by org name ASC.",
        "grain": "One row per organization.",
        "sql": """SELECT
    o.name AS org_name,
    COUNT(m.user_id) AS used_seats,
    s.seats_purchased
FROM saas.organizations o
JOIN saas.subscriptions s ON o.id = s.organization_id
LEFT JOIN saas.memberships m ON o.id = m.organization_id
GROUP BY o.id, o.name, s.seats_purchased
ORDER BY org_name ASC;"""
    },
    {
        "cat": "02-group-by-drills",
        "num": 7,
        "title": "Min and Max per Category",
        "schema": "ecommerce",
        "req": "Find min price and max price of products in each category. Project category_id, min_price, max_price. Order by category_id ASC.",
        "grain": "One row per category.",
        "sql": """SELECT
    category_id,
    MIN(price) AS min_price,
    MAX(price) AS max_price
FROM ecommerce.products
GROUP BY category_id
ORDER BY category_id ASC;"""
    },
    {
        "cat": "02-group-by-drills",
        "num": 8,
        "title": "Group By Expression (Price Range Bucket)",
        "schema": "ecommerce",
        "req": "Group products into buckets: '< 100', '100-500', '> 500'. Count products per bucket. Order by product_count DESC.",
        "grain": "One row per price bucket.",
        "sql": """SELECT
    CASE
        WHEN price < 100 THEN '< 100'
        WHEN price <= 500 THEN '100-500'
        ELSE '> 500'
    END AS price_tier,
    COUNT(*) AS product_count
FROM ecommerce.products
GROUP BY 1
ORDER BY product_count DESC;"""
    },
    {
        "cat": "02-group-by-drills",
        "num": 9,
        "title": "Grouping on Multiple Attributes",
        "schema": "ecommerce",
        "req": "Select status, payment_method, count of orders, and sum of total amount from orders joined with payments. Order by status ASC, payment_method ASC.",
        "grain": "One row per status and payment_method combination.",
        "sql": """SELECT
    o.status,
    p.payment_method,
    COUNT(DISTINCT o.id) AS order_count,
    SUM(p.amount) AS total_paid
FROM ecommerce.orders o
JOIN ecommerce.payments p ON o.id = p.order_id
GROUP BY o.status, p.payment_method
ORDER BY o.status ASC, p.payment_method ASC;"""
    },
    {
        "cat": "02-group-by-drills",
        "num": 10,
        "title": "Filter with Filter Clause (Standard SQL FILTER)",
        "schema": "ecommerce",
        "req": "Using SQL standard FILTER (WHERE ...), calculate total count of orders, count of completed orders, and count of refunded orders by customer_id. Order by customer_id ASC.",
        "grain": "One row per customer.",
        "sql": """SELECT
    customer_id,
    COUNT(*) AS total_orders,
    COUNT(*) FILTER (WHERE status = 'completed') AS completed_orders,
    COUNT(*) FILTER (WHERE status = 'refunded') AS refunded_orders
FROM ecommerce.orders
GROUP BY customer_id
ORDER BY customer_id ASC;"""
    },

    # Category 3: Date/Time Drills
    {
        "cat": "03-date-drills",
        "num": 1,
        "title": "Date Truncation by Month",
        "schema": "ecommerce",
        "req": "Aggregate monthly order counts and total completed revenue using DATE_TRUNC('month', order_date). Order by order_month ASC.",
        "grain": "One row per calendar month.",
        "sql": """SELECT
    DATE_TRUNC('month', order_date)::DATE AS order_month,
    COUNT(*) AS total_orders,
    SUM(total_amount) AS total_revenue
FROM ecommerce.orders
WHERE status = 'completed'
GROUP BY 1
ORDER BY order_month ASC;"""
    },
    {
        "cat": "03-date-drills",
        "num": 2,
        "title": "Date Extraction (Day of Week)",
        "schema": "ecommerce",
        "req": "Extract day of week (0=Sunday to 6=Saturday) from order_date. Count orders per day of week. Order by day_of_week ASC.",
        "grain": "One row per day of week.",
        "sql": """SELECT
    EXTRACT(DOW FROM order_date) AS day_of_week,
    COUNT(*) AS order_count
FROM ecommerce.orders
GROUP BY 1
ORDER BY day_of_week ASC;"""
    },
    {
        "cat": "03-date-drills",
        "num": 3,
        "title": "Date Interval Arithmetic (Rolling 60 Days)",
        "schema": "ecommerce",
        "req": "Select all orders placed between '2026-01-01' and '2026-01-01'::date + INTERVAL '45 days'. Project order id, customer_id, order_date. Order by order_date ASC.",
        "grain": "One row per qualifying order.",
        "sql": """SELECT
    id AS order_id,
    customer_id,
    order_date
FROM ecommerce.orders
WHERE order_date >= '2026-01-01'
  AND order_date < '2026-01-01'::DATE + INTERVAL '45 days'
ORDER BY order_date ASC;"""
    },
    {
        "cat": "03-date-drills",
        "num": 4,
        "title": "Age and Interval Calculation",
        "schema": "social",
        "req": "Calculate the duration in hours between post created_at and the first comment created_at for post id = 1. Return post_id and duration_hours (rounded to 2 decimal places).",
        "grain": "One row for post 1.",
        "sql": """SELECT
    p.id AS post_id,
    ROUND(EXTRACT(EPOCH FROM (MIN(c.created_at) - p.created_at)) / 3600.0, 2) AS duration_hours
FROM social.posts p
JOIN social.comments c ON p.id = c.post_id
WHERE p.id = 1
GROUP BY p.id, p.created_at;"""
    },
    {
        "cat": "03-date-drills",
        "num": 5,
        "title": "Date Range Scaffolding with generate_series",
        "schema": "ecommerce",
        "req": "Generate all calendar days from '2026-01-01' to '2026-01-05'. Left join to completed orders on that day to show daily order count (0 if none). Order by day ASC.",
        "grain": "One row per calendar day.",
        "sql": """SELECT
    d.day::DATE AS calendar_day,
    COUNT(o.id) AS order_count
FROM generate_series('2026-01-01'::DATE, '2026-01-05'::DATE, '1 day'::INTERVAL) AS d(day)
LEFT JOIN ecommerce.orders o
    ON d.day::DATE = o.order_date::DATE
    AND o.status = 'completed'
GROUP BY d.day
ORDER BY calendar_day ASC;"""
    },
    {
        "cat": "03-date-drills",
        "num": 6,
        "title": "Time Difference Between Consecutive Events",
        "schema": "analytics",
        "req": "For session 'b0000000-0000-0000-0000-000000000001', calculate seconds elapsed between consecutive events. Select event_name, event_timestamp, and seconds_since_prev. Order by event_timestamp ASC.",
        "grain": "One row per event in session.",
        "sql": """SELECT
    event_name,
    event_timestamp,
    EXTRACT(EPOCH FROM (event_timestamp - LAG(event_timestamp) OVER (ORDER BY event_timestamp))) AS seconds_since_prev
FROM analytics.events
WHERE session_id = 'b0000000-0000-0000-0000-000000000001'
ORDER BY event_timestamp ASC;"""
    },
    {
        "cat": "03-date-drills",
        "num": 7,
        "title": "Year-over-Year / Year Selection",
        "schema": "ecommerce",
        "req": "Extract the year from order_date and count total orders by year. Project order_year and total_orders. Order by order_year ASC.",
        "grain": "One row per year.",
        "sql": """SELECT
    EXTRACT(YEAR FROM order_date)::INT AS order_year,
    COUNT(*) AS total_orders
FROM ecommerce.orders
GROUP BY 1
ORDER BY order_year ASC;"""
    },
    {
        "cat": "03-date-drills",
        "num": 8,
        "title": "Filtering with SARGable Date Boundaries",
        "schema": "ecommerce",
        "req": "Select orders created in February 2026 using an index-friendly (sargable) range comparison. Order by order_date ASC.",
        "grain": "One row per February order.",
        "sql": """SELECT
    id AS order_id,
    customer_id,
    order_date,
    total_amount
FROM ecommerce.orders
WHERE order_date >= '2026-02-01 00:00:00+00'
  AND order_date < '2026-03-01 00:00:00+00'
ORDER BY order_date ASC;"""
    },
    {
        "cat": "03-date-drills",
        "num": 9,
        "title": "Timezone Conversion Display",
        "schema": "ecommerce",
        "req": "Convert order_date for order 1 to 'America/New_York' timezone. Display UTC timestamp, NY timestamp, and total_amount.",
        "grain": "One row for order 1.",
        "sql": """SELECT
    id AS order_id,
    order_date AS utc_time,
    order_date AT TIME ZONE 'America/New_York' AS ny_time,
    total_amount
FROM ecommerce.orders
WHERE id = 1;"""
    },
    {
        "cat": "03-date-drills",
        "num": 10,
        "title": "Days Since Last Order per Customer",
        "schema": "ecommerce",
        "req": "Calculate days between customer's most recent order and '2026-03-20'::DATE. Project customer_id, latest_order_date, and days_since_last_order. Order by days_since_last_order ASC.",
        "grain": "One row per customer with orders.",
        "sql": """SELECT
    customer_id,
    MAX(order_date)::DATE AS latest_order_date,
    ('2026-03-20'::DATE - MAX(order_date)::DATE) AS days_since_last_order
FROM ecommerce.orders
GROUP BY customer_id
ORDER BY days_since_last_order ASC, customer_id ASC;"""
    },

    # Category 4: Window Function Drills
    {
        "cat": "04-window-drills",
        "num": 1,
        "title": "ROW_NUMBER (Latest Order per Customer)",
        "schema": "ecommerce",
        "req": "Find each customer's most recent order. Select customer_id, order_id, and order_date. Order by customer_id ASC.",
        "grain": "One row per customer.",
        "sql": """WITH ranked_orders AS (
    SELECT
        customer_id,
        id AS order_id,
        order_date,
        ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC, id DESC) AS rn
    FROM ecommerce.orders
)
SELECT
    customer_id,
    order_id,
    order_date
FROM ranked_orders
WHERE rn = 1
ORDER BY customer_id ASC;"""
    },
    {
        "cat": "04-window-drills",
        "num": 2,
        "title": "Running Total (Cumulative Revenue)",
        "schema": "ecommerce",
        "req": "Calculate running total revenue over completed orders ordered by order_date ASC. Project order_id, order_date, total_amount, running_revenue. Order by order_date ASC.",
        "grain": "One row per completed order.",
        "sql": """SELECT
    id AS order_id,
    order_date,
    total_amount,
    SUM(total_amount) OVER (
        ORDER BY order_date ASC, id ASC
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_revenue
FROM ecommerce.orders
WHERE status = 'completed'
ORDER BY order_date ASC, order_id ASC;"""
    },
    {
        "cat": "04-window-drills",
        "num": 3,
        "title": "DENSE_RANK (Top Products by Price)",
        "schema": "ecommerce",
        "req": "Assign dense price rank to products within each category_id. Project category_id, name, price, price_rank. Order by category_id ASC, price_rank ASC, name ASC.",
        "grain": "One row per product.",
        "sql": """SELECT
    category_id,
    name,
    price,
    DENSE_RANK() OVER (PARTITION BY category_id ORDER BY price DESC) AS price_rank
FROM ecommerce.products
ORDER BY category_id ASC, price_rank ASC, name ASC;"""
    },
    {
        "cat": "04-window-drills",
        "num": 4,
        "title": "LAG (Previous Order Amount)",
        "schema": "ecommerce",
        "req": "For customer 1, show order id, order_date, total_amount, and previous order amount. Order by order_date ASC.",
        "grain": "One row per order for customer 1.",
        "sql": """SELECT
    id AS order_id,
    order_date,
    total_amount,
    LAG(total_amount, 1) OVER (ORDER BY order_date ASC) AS prev_order_amount
FROM ecommerce.orders
WHERE customer_id = 1
ORDER BY order_date ASC;"""
    },
    {
        "cat": "04-window-drills",
        "num": 5,
        "title": "LEAD (Next Event Name)",
        "schema": "analytics",
        "req": "For session 'b0000000-0000-0000-0000-000000000001', select event_name, event_timestamp, and next event_name. Order by event_timestamp ASC.",
        "grain": "One row per event.",
        "sql": """SELECT
    event_name,
    event_timestamp,
    LEAD(event_name, 1) OVER (ORDER BY event_timestamp ASC) AS next_event_name
FROM analytics.events
WHERE session_id = 'b0000000-0000-0000-0000-000000000001'
ORDER BY event_timestamp ASC;"""
    },
    {
        "cat": "04-window-drills",
        "num": 6,
        "title": "Moving Average (3-Order Moving Window)",
        "schema": "ecommerce",
        "req": "Calculate 3-order moving average of completed order totals (current row and preceding 2 rows). Project order_id, order_date, total_amount, moving_avg. Order by order_date ASC.",
        "grain": "One row per completed order.",
        "sql": """SELECT
    id AS order_id,
    order_date,
    total_amount,
    ROUND(AVG(total_amount) OVER (
        ORDER BY order_date ASC, id ASC
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ), 2) AS moving_avg
FROM ecommerce.orders
WHERE status = 'completed'
ORDER BY order_date ASC, order_id ASC;"""
    },
    {
        "cat": "04-window-drills",
        "num": 7,
        "title": "Percent of Total Contribution",
        "schema": "ecommerce",
        "req": "For completed orders, calculate each order's percentage contribution to total completed revenue. Project order_id, total_amount, pct_of_total. Order by total_amount DESC.",
        "grain": "One row per completed order.",
        "sql": """SELECT
    id AS order_id,
    total_amount,
    ROUND((total_amount / SUM(total_amount) OVER ()) * 100.0, 2) AS pct_of_total
FROM ecommerce.orders
WHERE status = 'completed'
ORDER BY total_amount DESC, order_id ASC;"""
    },
    {
        "cat": "04-window-drills",
        "num": 8,
        "title": "FIRST_VALUE and LAST_VALUE in Partition",
        "schema": "banking",
        "req": "For account 1 ledger entries, display id, amount, entry_type, first entry amount, and last entry amount. Order by created_at ASC.",
        "grain": "One row per ledger entry for account 1.",
        "sql": """SELECT
    id,
    entry_type,
    amount,
    FIRST_VALUE(amount) OVER (
        PARTITION BY account_id ORDER BY created_at ASC
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS first_entry_amount,
    LAST_VALUE(amount) OVER (
        PARTITION BY account_id ORDER BY created_at ASC
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS last_entry_amount
FROM banking.ledger_entries
WHERE account_id = 1
ORDER BY created_at ASC;"""
    },
    {
        "cat": "04-window-drills",
        "num": 9,
        "title": "Top-2 Products per Category",
        "schema": "ecommerce",
        "req": "Find top 2 most expensive products in each category. Project category_id, product name, price, rank. Order by category_id ASC, price DESC, name ASC.",
        "grain": "One row per product qualifying for top 2.",
        "sql": """WITH ranked AS (
    SELECT
        category_id,
        name,
        price,
        ROW_NUMBER() OVER (PARTITION BY category_id ORDER BY price DESC, id ASC) AS rn
    FROM ecommerce.products
)
SELECT
    category_id,
    name,
    price,
    rn AS rank
FROM ranked
WHERE rn <= 2
ORDER BY category_id ASC, price DESC, name ASC;"""
    },
    {
        "cat": "04-window-drills",
        "num": 10,
        "title": "NTILE (Quartile Distribution)",
        "schema": "ecommerce",
        "req": "Divide products into 4 price quartiles using NTILE(4). Project name, price, quartile. Order by price ASC, name ASC.",
        "grain": "One row per product.",
        "sql": """SELECT
    name,
    price,
    NTILE(4) OVER (ORDER BY price ASC) AS quartile
FROM ecommerce.products
ORDER BY price ASC, name ASC;"""
    },

    # Category 5: Subquery & CTE Drills
    {
        "cat": "05-subquery-drills",
        "num": 1,
        "title": "Scalar Subquery in WHERE",
        "schema": "ecommerce",
        "req": "Find all products with price strictly higher than the average price across all products. Project name and price. Order by price DESC.",
        "grain": "One row per above-average priced product.",
        "sql": """SELECT
    name,
    price
FROM ecommerce.products
WHERE price > (SELECT AVG(price) FROM ecommerce.products)
ORDER BY price DESC;"""
    },
    {
        "cat": "05-subquery-drills",
        "num": 2,
        "title": "Correlated Subquery in WHERE",
        "schema": "ecommerce",
        "req": "Find products whose price is strictly greater than the average price of products in their OWN category. Project category_id, name, price. Order by category_id ASC, price DESC.",
        "grain": "One row per qualifying product.",
        "sql": """SELECT
    p1.category_id,
    p1.name,
    p1.price
FROM ecommerce.products p1
WHERE p1.price > (
    SELECT AVG(p2.price)
    FROM ecommerce.products p2
    WHERE p2.category_id = p1.category_id
)
ORDER BY p1.category_id ASC, p1.price DESC;"""
    },
    {
        "cat": "05-subquery-drills",
        "num": 3,
        "title": "EXISTS (Customers with Completed Orders)",
        "schema": "ecommerce",
        "req": "Find customers who have at least one completed order using EXISTS. Project customer id and email. Order by customer id ASC.",
        "grain": "One row per customer.",
        "sql": """SELECT
    c.id,
    c.email
FROM ecommerce.customers c
WHERE EXISTS (
    SELECT 1
    FROM ecommerce.orders o
    WHERE o.customer_id = c.id
      AND o.status = 'completed'
)
ORDER BY c.id ASC;"""
    },
    {
        "cat": "05-subquery-drills",
        "num": 4,
        "title": "NOT EXISTS (Customers with No Orders)",
        "schema": "ecommerce",
        "req": "Find customers who have never placed any orders using NOT EXISTS. Project customer id, first_name, last_name, email. Order by id ASC.",
        "grain": "One row per customer without orders.",
        "sql": """SELECT
    c.id,
    c.first_name,
    c.last_name,
    c.email
FROM ecommerce.customers c
WHERE NOT EXISTS (
    SELECT 1
    FROM ecommerce.orders o
    WHERE o.customer_id = c.id
)
ORDER BY c.id ASC;"""
    },
    {
        "cat": "05-subquery-drills",
        "num": 5,
        "title": "Subquery in FROM (Derived Table)",
        "schema": "ecommerce",
        "req": "From a derived table calculating customer completed order totals, calculate overall average customer spend. Return avg_spend rounded to 2 decimal places.",
        "grain": "Single scalar summary row.",
        "sql": """SELECT
    ROUND(AVG(customer_spend), 2) AS avg_customer_spend
FROM (
    SELECT customer_id, SUM(total_amount) AS customer_spend
    FROM ecommerce.orders
    WHERE status = 'completed'
    GROUP BY customer_id
) AS spend_summary;"""
    },
    {
        "cat": "05-subquery-drills",
        "num": 6,
        "title": "Multi-Stage CTE Pipeline",
        "schema": "ecommerce",
        "req": "Using two CTEs: 1. `order_totals` (customer_id, total_spent), 2. `ranked` (customer_id, total_spent, rank by spend). Return top 3 spenders. Order by rank ASC.",
        "grain": "One row per top 3 customer.",
        "sql": """WITH order_totals AS (
    SELECT customer_id, SUM(total_amount) AS total_spent
    FROM ecommerce.orders
    WHERE status = 'completed'
    GROUP BY customer_id
),
ranked AS (
    SELECT
        customer_id,
        total_spent,
        DENSE_RANK() OVER (ORDER BY total_spent DESC) AS rnk
    FROM order_totals
)
SELECT
    customer_id,
    total_spent,
    rnk AS rank
FROM ranked
WHERE rnk <= 3
ORDER BY rank ASC;"""
    },
    {
        "cat": "05-subquery-drills",
        "num": 7,
        "title": "Recursive CTE (Category Breadcrumb Tree)",
        "schema": "ecommerce",
        "req": "Using a recursive CTE, build full category path for all categories (e.g. 'Electronics > Audio & Headphones'). Return id, path. Order by id ASC.",
        "grain": "One row per category with hierarchical path.",
        "sql": """WITH RECURSIVE cat_tree AS (
    SELECT
        id,
        name,
        parent_id,
        name::TEXT AS path
    FROM ecommerce.categories
    WHERE parent_id IS NULL
    UNION ALL
    SELECT
        c.id,
        c.name,
        c.parent_id,
        (ct.path || ' > ' || c.name)::TEXT AS path
    FROM ecommerce.categories c
    JOIN cat_tree ct ON c.parent_id = ct.id
)
SELECT
    id,
    path
FROM cat_tree
ORDER BY id ASC;"""
    },
    {
        "cat": "05-subquery-drills",
        "num": 8,
        "title": "Set Operation: UNION ALL vs UNION",
        "schema": "social",
        "req": "Combine unique user IDs who have either authored a post or authored a comment. Return distinct user_id. Order by user_id ASC.",
        "grain": "One row per active content creator user.",
        "sql": """SELECT user_id FROM social.posts
UNION
SELECT user_id FROM social.comments
ORDER BY user_id ASC;"""
    },
    {
        "cat": "05-subquery-drills",
        "num": 9,
        "title": "Set Operation: EXCEPT (Active Users with No Posts)",
        "schema": "social",
        "req": "Find users who have liked a post, EXCEPT users who have authored a post. Return user_id. Order by user_id ASC.",
        "grain": "One row per qualifying user.",
        "sql": """SELECT user_id FROM social.likes
EXCEPT
SELECT user_id FROM social.posts
ORDER BY user_id ASC;"""
    },
    {
        "cat": "05-subquery-drills",
        "num": 10,
        "title": "Correlated NOT EXISTS with Date Filter",
        "schema": "saas",
        "req": "Find organizations that have NOT generated any telemetry events in March 2026. Project org id and org name. Order by org id ASC.",
        "grain": "One row per organization inactive in March 2026.",
        "sql": """SELECT
    o.id,
    o.name
FROM saas.organizations o
WHERE NOT EXISTS (
    SELECT 1
    FROM saas.events e
    WHERE e.organization_id = o.id
      AND e.created_at >= '2026-03-01 00:00:00+00'
      AND e.created_at < '2026-04-01 00:00:00+00'
)
ORDER BY o.id ASC;"""
    }
]

def main():
    print(f"Generating {len(DRILLS)} drills and solutions...")
    for d in DRILLS:
        cat_dir = ROOT / "drills" / d["cat"]
        sol_dir = ROOT / "solutions" / "drills" / d["cat"]
        cat_dir.mkdir(parents=True, exist_ok=True)
        sol_dir.mkdir(parents=True, exist_ok=True)

        drill_file = cat_dir / f"drill-{d['num']:02d}.md"
        sol_file = sol_dir / f"drill-{d['num']:02d}.sql"

        # Write drill markdown
        md_content = f"""# Drill {d['num']:02d}: {d['title']}

**Category:** {d['cat']}  
**Target Schema:** `{d['schema']}`  
**Concept:** Fluency Drill  

---

## Business Requirement

> {d['req']}

---

## 14-Question Thinking Anchor
- **What should one output row represent (Grain)?**  
  *{d['grain']}*

---

## Target Verification
When your query is ready, verify it against the test harness:

```bash
python3 scripts/grade-query.py drills/{d['cat']}/drill-{d['num']:02d}.md
```
"""
        drill_file.write_text(md_content, encoding="utf-8")

        # Write solution SQL
        sol_file.write_text(d["sql"] + "\n", encoding="utf-8")

    print("[+] All 50 drills and reference solutions written successfully!")

if __name__ == "__main__":
    main()
