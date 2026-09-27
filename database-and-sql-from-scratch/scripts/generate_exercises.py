"""
Generator for 155+ SQL Exercises and matching separate solutions.
Categories:
  - exercises/beginner/     (q01 to q40) -> 40 exercises
  - exercises/intermediate/ (q41 to q90) -> 50 exercises
  - exercises/advanced/     (q91 to q130) -> 40 exercises
  - exercises/challenge/    (q131 to q160) -> 30 exercises
Total: 160 exercises!
"""

import os
from pathlib import Path

ROOT = Path("/Users/tushar/Desktop/private/repos/database-and-sql-from-scratch")

EXERCISES = []

# =====================================================================
# 1. BEGINNER EXERCISES (q01 - q40)
# =====================================================================
beginner_defs = [
    ("q01-select-constants", "ecommerce", "Beginner", ["SELECT", "Expressions"],
     "Select literal numbers and strings: return 42 as answer, 'PostgreSQL 16' as engine, and 100 * 1.05 as taxed_amount.",
     "1 row, 3 columns: answer (int), engine (text), taxed_amount (numeric)",
     "SELECT 42 AS answer, 'PostgreSQL 16' AS engine, 100 * 1.05 AS taxed_amount;"),

    ("q02-project-customer-columns", "ecommerce", "Beginner", ["SELECT", "Projection"],
     "Select id, email, and full name formatted as first_name || ' ' || last_name aliased as customer_name from customers. Order by id ASC.",
     "15 rows, 3 columns: id, email, customer_name",
     "SELECT id, email, first_name || ' ' || last_name AS customer_name FROM ecommerce.customers ORDER BY id ASC;"),

    ("q03-product-profit-margin", "ecommerce", "Beginner", ["SELECT", "Arithmetic"],
     "Calculate the absolute profit (price - cost) and markup percentage (ROUND(((price - cost) / cost) * 100, 2)) for each product. Return sku, name, profit, markup_pct. Order by profit DESC.",
     "12 rows, 4 columns: sku, name, profit, markup_pct",
     "SELECT sku, name, (price - cost) AS profit, ROUND(((price - cost) / cost) * 100, 2) AS markup_pct FROM ecommerce.products ORDER BY profit DESC, sku ASC;"),

    ("q04-filter-active-products", "ecommerce", "Beginner", ["WHERE", "Equality"],
     "Select sku, name, and price for all products where is_active is TRUE. Order by price DESC.",
     "11 rows, 3 columns: sku, name, price",
     "SELECT sku, name, price FROM ecommerce.products WHERE is_active = TRUE ORDER BY price DESC, sku ASC;"),

    ("q05-filter-price-range", "ecommerce", "Beginner", ["WHERE", "BETWEEN"],
     "Find all products with price between 100.00 and 500.00 inclusive. Project sku, name, price. Order by price ASC.",
     "3 rows, 3 columns: sku, name, price",
     "SELECT sku, name, price FROM ecommerce.products WHERE price BETWEEN 100.00 AND 500.00 ORDER BY price ASC, sku ASC;"),

    ("q06-filter-compound-or-and", "ecommerce", "Beginner", ["WHERE", "Boolean Logic"],
     "Find products where category_id is 2 OR category_id is 3, AND price is strictly under 500.00. Mind operator precedence! Order by id ASC.",
     "3 rows, 3 columns: id, category_id, name, price",
     "SELECT id, category_id, name, price FROM ecommerce.products WHERE (category_id = 2 OR category_id = 3) AND price < 500.00 ORDER BY id ASC;"),

    ("q07-null-identification", "ecommerce", "Beginner", ["NULL", "IS NULL"],
     "Find all root categories (categories that do not have a parent category). Return id, name, slug. Order by id ASC.",
     "3 rows, 3 columns: id, name, slug",
     "SELECT id, name, slug FROM ecommerce.categories WHERE parent_id IS NULL ORDER BY id ASC;"),

    ("q08-not-null-filter", "ecommerce", "Beginner", ["NULL", "IS NOT NULL"],
     "Find all subcategories that have an assigned parent_id. Return id, parent_id, name. Order by parent_id ASC, id ASC.",
     "5 rows, 3 columns: id, parent_id, name",
     "SELECT id, parent_id, name FROM ecommerce.categories WHERE parent_id IS NOT NULL ORDER BY parent_id ASC, id ASC;"),

    ("q09-coalesce-handling", "social", "Beginner", ["NULL", "COALESCE"],
     "Select username and a profile bio display. If bio is NULL, replace it with 'No bio provided.' aliased as display_bio. Order by id ASC.",
     "7 rows, 2 columns: username, display_bio",
     "SELECT username, COALESCE(bio, 'No bio provided.') AS display_bio FROM social.users ORDER BY id ASC;"),

    ("q10-nullif-division-safeguard", "ecommerce", "Beginner", ["NULL", "NULLIF"],
     "Calculate ratio of reorder_level to stock_quantity for inventory items. Use NULLIF to prevent division by zero when stock_quantity = 0. Project product_id, stock_quantity, reorder_level, ratio. Order by product_id ASC.",
     "12 rows, 4 columns: product_id, stock_quantity, reorder_level, ratio",
     "SELECT product_id, stock_quantity, reorder_level, ROUND(reorder_level::NUMERIC / NULLIF(stock_quantity, 0), 2) AS ratio FROM ecommerce.inventory ORDER BY product_id ASC;"),

    ("q11-deterministic-sorting", "ecommerce", "Beginner", ["ORDER BY", "Tie-Breaking"],
     "Select all orders sorted by status ascending, then by total_amount descending, and finally by id ascending as a deterministic tie-breaker.",
     "17 rows, 4 columns: id, customer_id, status, total_amount",
     "SELECT id, customer_id, status, total_amount FROM ecommerce.orders ORDER BY status ASC, total_amount DESC, id ASC;"),

    ("q12-nulls-ordering", "ecommerce", "Beginner", ["ORDER BY", "NULLS FIRST/LAST"],
     "Select category id, name, and parent_id. Order by parent_id ASC NULLS FIRST, then id ASC.",
     "8 rows, 3 columns: id, name, parent_id",
     "SELECT id, name, parent_id FROM ecommerce.categories ORDER BY parent_id ASC NULLS FIRST, id ASC;"),

    ("q13-limit-offset-pagination", "ecommerce", "Beginner", ["LIMIT", "OFFSET"],
     "Fetch page 2 of products when sorted by price descending with page size of 3 items (i.e. items 4, 5, 6). Project id, name, price. Order by price DESC, id ASC.",
     "3 rows, 3 columns: id, name, price",
     "SELECT id, name, price FROM ecommerce.products ORDER BY price DESC, id ASC LIMIT 3 OFFSET 3;"),

    ("q14-fetch-first-standard", "ecommerce", "Beginner", ["SQL Standard", "FETCH FIRST"],
     "Using standard SQL FETCH FIRST clause (instead of LIMIT), select the top 2 highest priced products. Order by price DESC, id ASC.",
     "2 rows, 3 columns: id, name, price",
     "SELECT id, name, price FROM ecommerce.products ORDER BY price DESC, id ASC FETCH FIRST 2 ROWS ONLY;"),

    ("q15-case-categorization", "ecommerce", "Beginner", ["CASE", "Conditional Logic"],
     "Classify each customer's status: if 'active' then 'Verified User', if 'suspended' then 'Action Required', else 'Unknown'. Return email, status, and status_label. Order by id ASC.",
     "15 rows, 3 columns: email, status, status_label",
     "SELECT email, status, CASE status WHEN 'active' THEN 'Verified User' WHEN 'suspended' THEN 'Action Required' ELSE 'Unknown' END AS status_label FROM ecommerce.customers ORDER BY id ASC;"),

    ("q16-case-tier-evaluation", "ecommerce", "Beginner", ["CASE", "Numeric Tiers"],
     "Categorize order totals into size tiers: >= 1000 is 'Enterprise', >= 250 is 'Mid-Market', else 'Standard'. Return id, total_amount, tier. Order by total_amount DESC, id ASC.",
     "17 rows, 3 columns: id, total_amount, tier",
     "SELECT id, total_amount, CASE WHEN total_amount >= 1000 THEN 'Enterprise' WHEN total_amount >= 250 THEN 'Mid-Market' ELSE 'Standard' END AS tier FROM ecommerce.orders ORDER BY total_amount DESC, id ASC;"),

    ("q17-string-transformations", "social", "Beginner", ["Strings", "LOWER/UPPER/LENGTH"],
     "Return full_name in uppercase, username in lowercase, and length of bio (or 0 if null) for all users. Order by id ASC.",
     "7 rows, 4 columns: id, upper_name, lower_username, bio_len",
     "SELECT id, UPPER(full_name) AS upper_name, LOWER(username) AS lower_username, COALESCE(LENGTH(bio), 0) AS bio_len FROM social.users ORDER BY id ASC;"),

    ("q18-string-pattern-matching", "ecommerce", "Beginner", ["Strings", "LIKE"],
     "Find all customers whose email ends with '@example.com' and whose first name starts with 'A' or 'B'. Order by id ASC.",
     "2 rows, 3 columns: id, first_name, email",
     "SELECT id, first_name, email FROM ecommerce.customers WHERE email LIKE '%@example.com' AND (first_name LIKE 'A%' OR first_name LIKE 'B%') ORDER BY id ASC;"),

    ("q19-string-ilike-postgres", "ecommerce", "Beginner", ["Strings", "ILIKE"],
     "Search products where name contains 'phone' case-insensitively using PostgreSQL ILIKE. Return id, name, sku. Order by id ASC.",
     "2 rows, 3 columns: id, name, sku",
     "SELECT id, name, sku FROM ecommerce.products WHERE name ILIKE '%phone%' ORDER BY id ASC;"),

    ("q20-date-extraction", "ecommerce", "Beginner", ["Dates", "EXTRACT"],
     "For all orders, extract order year and order month as integers. Return id, order_year, order_month. Order by id ASC.",
     "17 rows, 3 columns: id, order_year, order_month",
     "SELECT id, EXTRACT(YEAR FROM order_date)::INT AS order_year, EXTRACT(MONTH FROM order_date)::INT AS order_month FROM ecommerce.orders ORDER BY id ASC;"),

    ("q21-date-comparison-recent", "ecommerce", "Beginner", ["Dates", "Intervals"],
     "Find orders placed on or after '2026-02-01'. Return id, status, total_amount, order_date. Order by order_date ASC, id ASC.",
     "12 rows, 4 columns: id, status, total_amount, order_date",
     "SELECT id, status, total_amount, order_date FROM ecommerce.orders WHERE order_date >= '2026-02-01 00:00:00+00' ORDER BY order_date ASC, id ASC;"),

    ("q22-date-truncation", "ecommerce", "Beginner", ["Dates", "DATE_TRUNC"],
     "Truncate order_date to the first day of the month for each order. Return id, total_amount, and month_start. Order by id ASC.",
     "17 rows, 3 columns: id, total_amount, month_start",
     "SELECT id, total_amount, DATE_TRUNC('month', order_date)::DATE AS month_start FROM ecommerce.orders ORDER BY id ASC;"),

    ("q23-in-list-filter", "ecommerce", "Beginner", ["WHERE", "IN"],
     "Find all orders with status in ('paid', 'shipped', 'completed'). Project id, customer_id, status. Order by id ASC.",
     "14 rows, 3 columns: id, customer_id, status",
     "SELECT id, customer_id, status FROM ecommerce.orders WHERE status IN ('paid', 'shipped', 'completed') ORDER BY id ASC;"),

    ("q24-not-in-clean-filter", "ecommerce", "Beginner", ["WHERE", "NOT IN"],
     "Find products whose category_id is NOT IN (2, 3). Return id, category_id, name. Order by id ASC.",
     "8 rows, 3 columns: id, category_id, name",
     "SELECT id, category_id, name FROM ecommerce.products WHERE category_id NOT IN (2, 3) ORDER BY id ASC;"),

    ("q25-safe-update-returning", "banking", "Beginner", ["DML", "RETURNING"],
     "Write a SELECT showing what an account balance would look like after adding 500 interest to checking accounts (account_type = 'checking'). Project id, account_number, balance, new_balance. Order by id ASC.",
     "4 rows, 4 columns: id, account_number, balance, new_balance",
     "SELECT id, account_number, balance, (balance + 500.00) AS new_balance FROM banking.accounts WHERE account_type = 'checking' ORDER BY id ASC;"),

    ("q26-boolean-logic-matrix", "ecommerce", "Beginner", ["Logic", "Three-Valued"],
     "Inspect the truth table of NULL comparison: evaluate (NULL = NULL) IS NULL, (NULL IS NULL), (TRUE AND NULL IS NULL).",
     "1 row, 3 columns: col1, col2, col3",
     "SELECT ((NULL = NULL) IS NULL) AS col1, (NULL IS NULL) AS col2, (TRUE AND (NULL IS NULL)) AS col3;"),

    ("q27-numeric-rounding", "ecommerce", "Beginner", ["Numeric", "ROUND/CEIL/FLOOR"],
     "Calculate unit_price divided by 3 for order items in order 1. Show raw_val, rounded to 2 decimals, ceil_val, and floor_val. Order by id ASC.",
     "2 rows, 5 columns: id, raw_val, rounded_val, ceil_val, floor_val",
     "SELECT id, (unit_price / 3.0) AS raw_val, ROUND(unit_price / 3.0, 2) AS rounded_val, CEIL(unit_price / 3.0) AS ceil_val, FLOOR(unit_price / 3.0) AS floor_val FROM ecommerce.order_items WHERE order_id = 1 ORDER BY id ASC;"),

    ("q28-substring-extraction", "banking", "Beginner", ["Strings", "SUBSTRING"],
     "Extract the 3-letter account category code from account_number (e.g. 'CHK' from 'ACCT-CHK-10001'). Return id, account_number, acct_code. Order by id ASC.",
     "5 rows, 3 columns: id, account_number, acct_code",
     "SELECT id, account_number, SUBSTRING(account_number FROM 6 FOR 3) AS acct_code FROM banking.accounts ORDER BY id ASC;"),

    ("q29-distinct-simple", "ecommerce", "Beginner", ["DISTINCT", "Projection"],
     "Find all unique order statuses present in the orders table. Order by status ASC.",
     "4 rows, 1 column: status",
     "SELECT DISTINCT status FROM ecommerce.orders ORDER BY status ASC;"),

    ("q30-multi-column-distinct", "ecommerce", "Beginner", ["DISTINCT", "Multi-Column"],
     "Find all unique combinations of customer_id and status in orders. Order by customer_id ASC, status ASC.",
     "14 rows, 2 columns: customer_id, status",
     "SELECT DISTINCT customer_id, status FROM ecommerce.orders ORDER BY customer_id ASC, status ASC;"),

    ("q31-basic-inner-join", "ecommerce", "Beginner", ["JOIN", "INNER JOIN"],
     "Join products to their category name. Project product id, product name, category name, price. Order by product id ASC.",
     "12 rows, 4 columns: id, product_name, category_name, price",
     "SELECT p.id, p.name AS product_name, c.name AS category_name, p.price FROM ecommerce.products p JOIN ecommerce.categories c ON p.category_id = c.id ORDER BY p.id ASC;"),

    ("q32-left-join-null-detection", "ecommerce", "Beginner", ["JOIN", "LEFT JOIN"],
     "Left join customers to orders. Find rows where order id is NULL (customers with no orders). Project customer id, email. Order by customer id ASC.",
     "2 rows, 2 columns: id, email",
     "SELECT c.id, c.email FROM ecommerce.customers c LEFT JOIN ecommerce.orders o ON c.id = o.customer_id WHERE o.id IS NULL ORDER BY c.id ASC;"),

    ("q33-count-all-vs-count-col", "social", "Beginner", ["Aggregate", "COUNT"],
     "Demonstrate COUNT(*) vs COUNT(bio) in users table. Return total_users and users_with_bio.",
     "1 row, 2 columns: total_users, users_with_bio",
     "SELECT COUNT(*) AS total_users, COUNT(bio) AS users_with_bio FROM social.users;"),

    ("q34-sum-total-revenue", "ecommerce", "Beginner", ["Aggregate", "SUM"],
     "Calculate total gross revenue of all completed orders. Aliased as gross_revenue.",
     "1 row, 1 column: gross_revenue",
     "SELECT SUM(total_amount) AS gross_revenue FROM ecommerce.orders WHERE status = 'completed';"),

    ("q35-min-max-prices", "ecommerce", "Beginner", ["Aggregate", "MIN/MAX"],
     "Find the lowest and highest product prices. Return min_price, max_price.",
     "1 row, 2 columns: min_price, max_price",
     "SELECT MIN(price) AS min_price, MAX(price) AS max_price FROM ecommerce.products;"),

    ("q36-avg-order-size", "ecommerce", "Beginner", ["Aggregate", "AVG"],
     "Calculate the average total amount for completed orders, rounded to 2 decimal places. Aliased as avg_order_val.",
     "1 row, 1 column: avg_order_val",
     "SELECT ROUND(AVG(total_amount), 2) AS avg_order_val FROM ecommerce.orders WHERE status = 'completed';"),

    ("q37-simple-group-by", "ecommerce", "Beginner", ["GROUP BY", "Basic"],
     "Count orders per status. Return status and count. Order by count DESC, status ASC.",
     "4 rows, 2 columns: status, count",
     "SELECT status, COUNT(*) AS count FROM ecommerce.orders GROUP BY status ORDER BY count DESC, status ASC;"),

    ("q38-having-count-threshold", "ecommerce", "Beginner", ["HAVING", "Threshold"],
     "Group products by category_id and filter for categories having strictly more than 1 product. Project category_id and product_count. Order by category_id ASC.",
     "4 rows, 2 columns: category_id, product_count",
     "SELECT category_id, COUNT(*) AS product_count FROM ecommerce.products GROUP BY category_id HAVING COUNT(*) > 1 ORDER BY category_id ASC;"),

    ("q39-coalesce-aggregate", "ecommerce", "Beginner", ["Aggregate", "COALESCE"],
     "Sum total refunded amount from refunds table. If no refunds match or table is empty, return 0.00. Aliased as total_refunded.",
     "1 row, 1 column: total_refunded",
     "SELECT COALESCE(SUM(amount), 0.00) AS total_refunded FROM ecommerce.refunds;"),

    ("q40-scalar-subquery-where", "ecommerce", "Beginner", ["Subquery", "Scalar"],
     "Find all products priced higher than the product named 'Precision Coffee Grinder'. Project name, price. Order by price DESC.",
     "6 rows, 2 columns: name, price",
     "SELECT name, price FROM ecommerce.products WHERE price > (SELECT price FROM ecommerce.products WHERE name = 'Precision Coffee Grinder') ORDER BY price DESC, name ASC;")
]

for idx, item in enumerate(beginner_defs, start=1):
    EXERCISES.append({
        "tier": "beginner",
        "file": f"q{idx:02d}-{item[0].split('-', 1)[1]}",
        "schema": item[1],
        "diff": item[2],
        "tags": item[3],
        "req": item[4],
        "shape": item[5],
        "sql": item[6]
    })

# =====================================================================
# 2. INTERMEDIATE EXERCISES (q41 - q90)
# =====================================================================
intermediate_defs = [
    ("q41-three-table-customer-order-product", "ecommerce", "Intermediate", ["JOIN", "Multi-Table"],
     "Join customers, orders, order_items, and products. Return customer email, order id, product name, and quantity for completed orders. Order by customer email ASC, order id ASC, product name ASC.",
     "Multiple rows: email, order_id, product_name, quantity",
     "SELECT c.email, o.id AS order_id, p.name AS product_name, oi.quantity FROM ecommerce.customers c JOIN ecommerce.orders o ON c.id = o.customer_id JOIN ecommerce.order_items oi ON o.id = oi.order_id JOIN ecommerce.products p ON oi.product_id = p.id WHERE o.status = 'completed' ORDER BY c.email ASC, o.id ASC, p.name ASC;"),

    ("q42-customer-order-count-zero-inclusive", "ecommerce", "Intermediate", ["JOIN", "LEFT JOIN", "GROUP BY"],
     "List all customers with their total count of orders (including 0 for customers who never ordered). Project customer id, email, order_count. Order by order_count DESC, id ASC.",
     "15 rows: id, email, order_count",
     "SELECT c.id, c.email, COUNT(o.id) AS order_count FROM ecommerce.customers c LEFT JOIN ecommerce.orders o ON c.id = o.customer_id GROUP BY c.id, c.email ORDER BY order_count DESC, c.id ASC;"),

    ("q43-revenue-by-product-category", "ecommerce", "Intermediate", ["JOIN", "GROUP BY", "SUM"],
     "Calculate total completed revenue generated by each product category. Join order_items, products, categories, orders. Project category name, total_revenue. Order by total_revenue DESC.",
     "Categories with sales: category_name, total_revenue",
     "SELECT c.name AS category_name, SUM(oi.subtotal) AS total_revenue FROM ecommerce.order_items oi JOIN ecommerce.orders o ON oi.order_id = o.id JOIN ecommerce.products p ON oi.product_id = p.id JOIN ecommerce.categories c ON p.category_id = c.id WHERE o.status = 'completed' GROUP BY c.id, c.name ORDER BY total_revenue DESC;"),

    ("q44-conditional-aggregation-pivot", "ecommerce", "Intermediate", ["Aggregate", "CASE", "Pivoting"],
     "Produce a single-row status breakdown showing completed_count, cancelled_count, refunded_count, and pending_count across all orders.",
     "1 row, 4 columns: completed_count, cancelled_count, refunded_count, pending_count",
     "SELECT COUNT(CASE WHEN status = 'completed' THEN 1 END) AS completed_count, COUNT(CASE WHEN status = 'cancelled' THEN 1 END) AS cancelled_count, COUNT(CASE WHEN status = 'refunded' THEN 1 END) AS refunded_count, COUNT(CASE WHEN status = 'pending' THEN 1 END) AS pending_count FROM ecommerce.orders;"),

    ("q45-having-multi-metric", "ecommerce", "Intermediate", ["GROUP BY", "HAVING"],
     "Find customers who have spent a total of over $1,000 across completed orders and have placed at least 2 orders. Project customer_id, total_spent, order_count. Order by total_spent DESC.",
     "Qualifying customers: customer_id, total_spent, order_count",
     "SELECT customer_id, SUM(total_amount) AS total_spent, COUNT(*) AS order_count FROM ecommerce.orders WHERE status = 'completed' GROUP BY customer_id HAVING SUM(total_amount) > 1000 AND COUNT(*) >= 2 ORDER BY total_spent DESC;"),

    ("q46-distinct-on-postgres", "ecommerce", "Intermediate", ["PostgreSQL Specific", "DISTINCT ON"],
     "Using PostgreSQL's DISTINCT ON, find each customer's single most expensive order. Project customer_id, order_id, total_amount. Order by customer_id ASC, total_amount DESC, id ASC.",
     "1 customer row per orderer: customer_id, id AS order_id, total_amount",
     "SELECT DISTINCT ON (customer_id) customer_id, id AS order_id, total_amount FROM ecommerce.orders ORDER BY customer_id ASC, total_amount DESC, id ASC;"),

    ("q47-correlated-subquery-dept-avg", "ecommerce", "Intermediate", ["Subquery", "Correlated"],
     "Find products that are priced strictly higher than the average price of all products in their own category. Return category_id, name, price. Order by category_id ASC, price DESC.",
     "Rows per category: category_id, name, price",
     "SELECT p.category_id, p.name, p.price FROM ecommerce.products p WHERE p.price > (SELECT AVG(p2.price) FROM ecommerce.products p2 WHERE p2.category_id = p.category_id) ORDER BY p.category_id ASC, p.price DESC;"),

    ("q48-exists-correlated", "social", "Intermediate", ["EXISTS", "Correlated"],
     "Find users who have received at least one comment on any of their posts. Project user id and username. Order by user id ASC.",
     "Qualifying users: id, username",
     "SELECT u.id, u.username FROM social.users u WHERE EXISTS (SELECT 1 FROM social.posts p JOIN social.comments c ON p.id = c.post_id WHERE p.user_id = u.id) ORDER BY u.id ASC;"),

    ("q49-not-exists-anti-join", "social", "Intermediate", ["NOT EXISTS", "Anti-Join"],
     "Find users who have NEVER posted anything and NEVER liked any posts. Project id, username. Order by id ASC.",
     "Lurker users: id, username",
     "SELECT u.id, u.username FROM social.users u WHERE NOT EXISTS (SELECT 1 FROM social.posts p WHERE p.user_id = u.id) AND NOT EXISTS (SELECT 1 FROM social.likes l WHERE l.user_id = u.id) ORDER BY u.id ASC;"),

    ("q50-not-in-null-trap-debug", "ecommerce", "Intermediate", ["NULL Trap", "NOT IN vs NOT EXISTS"],
     "Demonstrate the safe NOT EXISTS pattern to find customers with no orders, avoiding the famous NOT IN (NULL) trap. Project id, email. Order by id ASC.",
     "Zero-order customers: id, email",
     "SELECT c.id, c.email FROM ecommerce.customers c WHERE NOT EXISTS (SELECT 1 FROM ecommerce.orders o WHERE o.customer_id = c.id) ORDER BY c.id ASC;"),

    ("q51-cte-decomposition-readability", "ecommerce", "Intermediate", ["CTE", "WITH Clause"],
     "Refactor a multi-stage aggregation using CTEs: calculate customer revenue, compute average customer revenue, and return customers earning above average. Order by total_revenue DESC.",
     "Rows: customer_id, total_revenue",
     "WITH cust_rev AS (SELECT customer_id, SUM(total_amount) AS total_revenue FROM ecommerce.orders WHERE status = 'completed' GROUP BY customer_id), avg_rev AS (SELECT AVG(total_revenue) AS threshold FROM cust_rev) SELECT cr.customer_id, cr.total_revenue FROM cust_rev cr CROSS JOIN avg_rev ar WHERE cr.total_revenue > ar.threshold ORDER BY cr.total_revenue DESC;"),

    ("q52-union-all-activity-stream", "social", "Intermediate", ["Set Operations", "UNION ALL"],
     "Create a unified activity feed combining posts and comments. Return user_id, activity_type ('post' or 'comment'), content_snippet (SUBSTRING text 1 to 30), and created_at. Order by created_at DESC.",
     "Rows: user_id, activity_type, content_snippet, created_at",
     "SELECT user_id, 'post' AS activity_type, SUBSTRING(content FROM 1 FOR 30) AS content_snippet, created_at FROM social.posts UNION ALL SELECT user_id, 'comment' AS activity_type, SUBSTRING(comment_text FROM 1 FOR 30) AS content_snippet, created_at FROM social.comments ORDER BY created_at DESC;"),

    ("q53-intersect-common-followers", "social", "Intermediate", ["Set Operations", "INTERSECT"],
     "Find user IDs who follow BOTH user 1 AND user 4. Order by user_id ASC.",
     "Rows: follower_id",
     "SELECT follower_id FROM social.follows WHERE following_id = 1 INTERSECT SELECT follower_id FROM social.follows WHERE following_id = 4 ORDER BY follower_id ASC;"),

    ("q54-except-non-reciprocated-follows", "social", "Intermediate", ["Set Operations", "EXCEPT"],
     "Find users whom user 1 follows, who DO NOT follow user 1 back. Return following_id. Order by following_id ASC.",
     "Rows: following_id",
     "SELECT following_id FROM social.follows WHERE follower_id = 1 EXCEPT SELECT follower_id FROM social.follows WHERE following_id = 1 ORDER BY following_id ASC;"),

    ("q55-saas-mrr-by-tier", "saas", "Intermediate", ["SaaS", "Financial Modeling"],
     "Calculate Monthly Recurring Revenue (MRR) and active organization count grouped by plan_tier for active subscriptions. Order by total_mrr DESC.",
     "Rows: plan_tier, total_mrr, active_orgs",
     "SELECT o.plan_tier, SUM(s.monthly_price) AS total_mrr, COUNT(o.id) AS active_orgs FROM saas.organizations o JOIN saas.subscriptions s ON o.id = s.organization_id WHERE s.status = 'active' GROUP BY o.plan_tier ORDER BY total_mrr DESC;"),

    ("q56-saas-seat-utilization", "saas", "Intermediate", ["SaaS", "Calculations"],
     "Find organizations where used memberships exceed 80% of purchased subscription seats. Project org name, seats_used, seats_purchased, utilization_pct. Order by utilization_pct DESC.",
     "Rows: name, seats_used, seats_purchased, utilization_pct",
     "SELECT o.name, COUNT(m.user_id) AS seats_used, s.seats_purchased, ROUND((COUNT(m.user_id)::NUMERIC / s.seats_purchased) * 100, 2) AS utilization_pct FROM saas.organizations o JOIN saas.subscriptions s ON o.id = s.organization_id LEFT JOIN saas.memberships m ON o.id = m.organization_id WHERE s.status = 'active' GROUP BY o.id, o.name, s.seats_purchased HAVING (COUNT(m.user_id)::NUMERIC / s.seats_purchased) >= 0.80 ORDER BY utilization_pct DESC;"),

    ("q57-banking-account-reconciliation", "banking", "Intermediate", ["Banking", "Financial Invariants"],
     "Verify double-entry integrity: compute sum of debits and sum of credits for each transaction. Confirm (sum_debit - sum_credit) equals 0.00 for all settled transactions. Order by transaction_id ASC.",
     "Rows: transaction_id, total_debit, total_credit, delta",
     "SELECT transaction_id, SUM(CASE WHEN entry_type = 'DEBIT' THEN amount ELSE 0 END) AS total_debit, SUM(CASE WHEN entry_type = 'CREDIT' THEN amount ELSE 0 END) AS total_credit, (SUM(CASE WHEN entry_type = 'DEBIT' THEN amount ELSE 0 END) - SUM(CASE WHEN entry_type = 'CREDIT' THEN amount ELSE 0 END)) AS delta FROM banking.ledger_entries GROUP BY transaction_id ORDER BY transaction_id ASC;"),

    ("q58-banking-running-balance-audit", "banking", "Intermediate", ["Banking", "Audit"],
     "Inspect ledger entries for account 1: verify if recorded running_balance matches the cumulative sum of credits minus debits. Project id, created_at, entry_type, amount, running_balance. Order by created_at ASC.",
     "Rows: id, created_at, entry_type, amount, running_balance",
     "SELECT id, created_at, entry_type, amount, running_balance FROM banking.ledger_entries WHERE account_id = 1 ORDER BY created_at ASC;"),

    ("q59-jsonb-payload-querying", "saas", "Intermediate", ["JSONB", "PostgreSQL"],
     "Query events table: extract 'env' and 'version' from payload where event_type = 'deploy.started'. Project id, env, version. Order by id ASC.",
     "Rows: id, env, version",
     "SELECT id, payload->>'env' AS env, payload->>'version' AS version FROM saas.events WHERE event_type = 'deploy.started' ORDER BY id ASC;"),

    ("q60-jsonb-containment-search", "saas", "Intermediate", ["JSONB", "GIN Containment"],
     "Find all events where payload contains key-value pair '\"gpu\": \"h100\"' using the @> JSONB containment operator. Project id, event_type, created_at. Order by id ASC.",
     "Rows: id, event_type, created_at",
     "SELECT id, event_type, created_at FROM saas.events WHERE payload @> '{\"gpu\": \"h100\"}'::jsonb ORDER BY id ASC;"),

    ("q61-self-join-employee-manager-analogy", "ecommerce", "Intermediate", ["Self Join", "Hierarchies"],
     "List all categories along with their grandparent category name (parent of parent) if applicable. Project category_name, parent_name, grandparent_name. Order by category_name ASC.",
     "Rows: category_name, parent_name, grandparent_name",
     "SELECT c.name AS category_name, p.name AS parent_name, gp.name AS grandparent_name FROM ecommerce.categories c LEFT JOIN ecommerce.categories p ON c.parent_id = p.id LEFT JOIN ecommerce.categories gp ON p.parent_id = gp.id ORDER BY category_name ASC;"),

    ("q62-cartesian-product-risk-mitigation", "ecommerce", "Intermediate", ["JOIN", "Safety"],
     "Generate all pairs of distinct products in category 2 where product A price < product B price. Project prod_a_name, prod_b_name, price_diff. Order by price_diff DESC.",
     "Rows: prod_a_name, prod_b_name, price_diff",
     "SELECT p1.name AS prod_a_name, p2.name AS prod_b_name, (p2.price - p1.price) AS price_diff FROM ecommerce.products p1 JOIN ecommerce.products p2 ON p1.category_id = p2.category_id AND p1.price < p2.price WHERE p1.category_id = 2 ORDER BY price_diff DESC;"),

    ("q63-filter-clause-multi-bucket", "ecommerce", "Intermediate", ["FILTER Clause", "Aggregates"],
     "Calculate count of orders, count of credit_card payments, and count of paypal payments by customer_id. Order by customer_id ASC.",
     "Rows: customer_id, total_orders, cc_payments, paypal_payments",
     "SELECT o.customer_id, COUNT(DISTINCT o.id) AS total_orders, COUNT(p.id) FILTER (WHERE p.payment_method = 'credit_card') AS cc_payments, COUNT(p.id) FILTER (WHERE p.payment_method = 'paypal') AS paypal_payments FROM ecommerce.orders o LEFT JOIN ecommerce.payments p ON o.id = p.order_id GROUP BY o.customer_id ORDER BY o.customer_id ASC;"),

    ("q64-address-default-lookup", "ecommerce", "Intermediate", ["JOIN", "Default Constraints"],
     "Find customers and their default shipping address city. If no default address exists, city should be 'No Default'. Project email, city. Order by email ASC.",
     "Rows: email, city",
     "SELECT c.email, COALESCE(a.city, 'No Default') AS city FROM ecommerce.customers c LEFT JOIN ecommerce.addresses a ON c.id = a.customer_id AND a.is_default = TRUE ORDER BY c.email ASC;"),

    ("q65-multi-column-group-with-totals", "ecommerce", "Intermediate", ["GROUP BY", "Status Matrix"],
     "Summarize orders by year and status: return order_year, status, count of orders, and sum of total_amount. Order by order_year ASC, status ASC.",
     "Rows: order_year, status, order_count, total_sum",
     "SELECT EXTRACT(YEAR FROM order_date)::INT AS order_year, status, COUNT(*) AS order_count, SUM(total_amount) AS total_sum FROM ecommerce.orders GROUP BY 1, 2 ORDER BY order_year ASC, status ASC;"),

    ("q66-daily-active-users", "analytics", "Intermediate", ["Analytics", "DAU"],
     "Calculate Daily Active Users (count of distinct user_id) per calendar day from the events table. Order by event_day ASC.",
     "Rows: event_day, dau",
     "SELECT event_timestamp::DATE AS event_day, COUNT(DISTINCT user_id) AS dau FROM analytics.events GROUP BY 1 ORDER BY event_day ASC;"),

    ("q67-session-duration-summary", "analytics", "Intermediate", ["Analytics", "Sessions"],
     "Calculate duration of completed sessions in minutes (ended_at - started_at). Project session id, device_type, duration_minutes. Order by duration_minutes DESC.",
     "Rows: id, device_type, duration_minutes",
     "SELECT id, device_type, ROUND(EXTRACT(EPOCH FROM (ended_at - started_at)) / 60.0, 2) AS duration_minutes FROM analytics.sessions WHERE ended_at IS NOT NULL ORDER BY duration_minutes DESC;"),

    ("q68-campaign-conversion-rate", "analytics", "Intermediate", ["Analytics", "Marketing Attribution"],
     "Calculate total sessions initiated and total purchases driven by each marketing campaign. Join campaigns, sessions, events. Order by total_sessions DESC.",
     "Rows: campaign_name, total_sessions, purchase_count",
     "SELECT c.name AS campaign_name, COUNT(DISTINCT s.id) AS total_sessions, COUNT(DISTINCT e.id) FILTER (WHERE e.event_name = 'purchase') AS purchase_count FROM analytics.campaigns c LEFT JOIN analytics.sessions s ON c.id = s.campaign_id LEFT JOIN analytics.events e ON s.id = e.session_id GROUP BY c.id, c.name ORDER BY total_sessions DESC;"),

    ("q69-inventory-restock-priority", "ecommerce", "Intermediate", ["Inventory", "Stock Alert"],
     "Identify products where stock_quantity <= reorder_level. Project sku, product name, stock_quantity, reorder_level, and units_needed (reorder_level * 2 - stock_quantity). Order by units_needed DESC.",
     "Rows: sku, name, stock_quantity, reorder_level, units_needed",
     "SELECT p.sku, p.name, i.stock_quantity, i.reorder_level, (i.reorder_level * 2 - i.stock_quantity) AS units_needed FROM ecommerce.products p JOIN ecommerce.inventory i ON p.id = i.product_id WHERE i.stock_quantity <= i.reorder_level ORDER BY units_needed DESC, p.sku ASC;"),

    ("q70-avg-items-per-order", "ecommerce", "Intermediate", ["Derived Table", "Aggregates"],
     "Calculate the average number of unique items and average total quantity per completed order. Return avg_unique_items and avg_quantity rounded to 2 decimals.",
     "1 row: avg_unique_items, avg_quantity",
     "SELECT ROUND(AVG(item_count), 2) AS avg_unique_items, ROUND(AVG(total_qty), 2) AS avg_quantity FROM (SELECT order_id, COUNT(product_id) AS item_count, SUM(quantity) AS total_qty FROM ecommerce.order_items oi JOIN ecommerce.orders o ON oi.order_id = o.id WHERE o.status = 'completed' GROUP BY order_id) sub;"),

    ("q71-subquery-all-comparison", "ecommerce", "Intermediate", ["Subquery", "ALL Operator"],
     "Find products whose price is strictly greater than ALL products in category 3 (Audio). Project name, price. Order by price ASC.",
     "Rows: name, price",
     "SELECT name, price FROM ecommerce.products WHERE price > ALL (SELECT price FROM ecommerce.products WHERE category_id = 3) ORDER BY price ASC, name ASC;"),

    ("q72-subquery-any-comparison", "ecommerce", "Intermediate", ["Subquery", "ANY Operator"],
     "Find products whose price matches ANY product price in category 8 (Books). Project name, price. Order by price ASC.",
     "Rows: name, price",
     "SELECT name, price FROM ecommerce.products WHERE price = ANY (SELECT price FROM ecommerce.products WHERE category_id = 8) ORDER BY price ASC, name ASC;"),

    ("q73-payment-method-market-share", "ecommerce", "Intermediate", ["Aggregates", "Percentages"],
     "Calculate percentage share of total transaction volume processed by each payment_method for completed payments. Order by share_pct DESC.",
     "Rows: payment_method, total_amount, share_pct",
     "SELECT payment_method, SUM(amount) AS total_amount, ROUND((SUM(amount) / (SELECT SUM(amount) FROM ecommerce.payments WHERE status = 'completed')) * 100, 2) AS share_pct FROM ecommerce.payments WHERE status = 'completed' GROUP BY payment_method ORDER BY share_pct DESC;"),

    ("q74-customer-first-and-last-order-date", "ecommerce", "Intermediate", ["Aggregate", "MIN/MAX Dates"],
     "For each customer with orders, determine their first order date and most recent order date. Project customer_id, first_order, latest_order. Order by customer_id ASC.",
     "Rows: customer_id, first_order, latest_order",
     "SELECT customer_id, MIN(order_date) AS first_order, MAX(order_date) AS latest_order FROM ecommerce.orders GROUP BY customer_id ORDER BY customer_id ASC;"),

    ("q75-duplicate-email-detection", "ecommerce", "Intermediate", ["Data Hygiene", "HAVING"],
     "Write a data hygiene query checking if any email address appears more than once in customers table. Project email, occurrence_count. (Should return 0 rows).",
     "0 rows expected: email, occurrence_count",
     "SELECT email, COUNT(*) AS occurrence_count FROM ecommerce.customers GROUP BY email HAVING COUNT(*) > 1;"),

    ("q76-order-item-price-discrepancy", "ecommerce", "Intermediate", ["Data Integrity", "JOIN"],
     "Compare historical unit_price recorded on order_items against current product list price in products table. Project order_id, product_name, recorded_price, current_price, difference. Order by order_id ASC.",
     "Rows: order_id, product_name, recorded_price, current_price, difference",
     "SELECT oi.order_id, p.name AS product_name, oi.unit_price AS recorded_price, p.price AS current_price, (oi.unit_price - p.price) AS difference FROM ecommerce.order_items oi JOIN ecommerce.products p ON oi.product_id = p.id WHERE oi.unit_price != p.price ORDER BY oi.order_id ASC;"),

    ("q77-social-engagement-rate-per-post", "social", "Intermediate", ["Social", "Ratios"],
     "For each post, calculate total likes and total comments. Compute engagement score: (likes * 2 + comments * 3). Project post_id, author_id, likes, comments, score. Order by score DESC.",
     "Rows: post_id, user_id, likes_count, comments_count, engagement_score",
     "SELECT p.id AS post_id, p.user_id, COUNT(DISTINCT l.user_id) AS likes_count, COUNT(DISTINCT c.id) AS comments_count, (COUNT(DISTINCT l.user_id) * 2 + COUNT(DISTINCT c.id) * 3) AS engagement_score FROM social.posts p LEFT JOIN social.likes l ON p.id = l.post_id LEFT JOIN social.comments c ON p.id = c.post_id GROUP BY p.id, p.user_id ORDER BY engagement_score DESC, post_id ASC;"),

    ("q78-saas-user-role-distribution", "saas", "Intermediate", ["SaaS", "Role Matrix"],
     "Count the number of users holding each role ('owner', 'admin', 'member') across all organizations. Order by role ASC.",
     "Rows: role, count",
     "SELECT role, COUNT(*) AS user_count FROM saas.memberships GROUP BY role ORDER BY role ASC;"),

    ("q79-top-spending-cities", "ecommerce", "Intermediate", ["Geography", "JOIN"],
     "Determine total completed revenue generated per customer city. Join customers, orders, addresses. Project city, total_revenue. Order by total_revenue DESC.",
     "Rows: city, total_revenue",
     "SELECT a.city, SUM(o.total_amount) AS total_revenue FROM ecommerce.customers c JOIN ecommerce.addresses a ON c.id = a.customer_id AND a.is_default = TRUE JOIN ecommerce.orders o ON c.id = o.customer_id WHERE o.status = 'completed' GROUP BY a.city ORDER BY total_revenue DESC;"),

    ("q80-repeat-customer-identification", "ecommerce", "Intermediate", ["Cohort", "HAVING"],
     "Identify repeat customers (customers with 2 or more completed orders). Project customer email and completed_order_count. Order by completed_order_count DESC, email ASC.",
     "Rows: email, completed_order_count",
     "SELECT c.email, COUNT(o.id) AS completed_order_count FROM ecommerce.customers c JOIN ecommerce.orders o ON c.id = o.customer_id WHERE o.status = 'completed' GROUP BY c.id, c.email HAVING COUNT(o.id) >= 2 ORDER BY completed_order_count DESC, c.email ASC;"),

    ("q81-refund-impact-ratio", "ecommerce", "Intermediate", ["Finance", "Refunds"],
     "Calculate total revenue lost to refunds compared to gross completed revenue. Return gross_rev, refunded_rev, and refund_loss_pct.",
     "1 row: gross_rev, refunded_rev, refund_loss_pct",
     "SELECT (SELECT SUM(total_amount) FROM ecommerce.orders WHERE status = 'completed') AS gross_rev, (SELECT SUM(amount) FROM ecommerce.refunds) AS refunded_rev, ROUND(((SELECT SUM(amount) FROM ecommerce.refunds) / (SELECT SUM(total_amount) FROM ecommerce.orders WHERE status = 'completed')) * 100, 2) AS refund_loss_pct;"),

    ("q82-multi-level-coalesce", "ecommerce", "Intermediate", ["NULL", "Fallbacks"],
     "Display product contact support hierarchy: return product name, category slug, and a fallback support contact 'support@' || category slug || '.com'. Order by product name ASC.",
     "Rows: name, slug, support_email",
     "SELECT p.name, c.slug, 'support@' || c.slug || '.com' AS support_email FROM ecommerce.products p JOIN ecommerce.categories c ON p.category_id = c.id ORDER BY p.name ASC;"),

    ("q83-cross-join-calendar-matrix", "ecommerce", "Intermediate", ["CROSS JOIN", "Matrix"],
     "Create a reporting skeleton: CROSS JOIN distinct order years (2026) with distinct product categories. Count actual orders matching that year and category. Order by category name ASC.",
     "Rows: category_name, order_count",
     "SELECT c.name AS category_name, COUNT(DISTINCT o.id) AS order_count FROM ecommerce.categories c LEFT JOIN ecommerce.products p ON c.id = p.category_id LEFT JOIN ecommerce.order_items oi ON p.id = oi.product_id LEFT JOIN ecommerce.orders o ON oi.order_id = o.id AND EXTRACT(YEAR FROM o.order_date) = 2026 GROUP BY c.id, c.name ORDER BY c.name ASC;"),

    ("q84-high-velocity-orders", "ecommerce", "Intermediate", ["Timing", "Orders"],
     "Find customers who placed two different orders within 7 days of each other. Project customer_id, order_a_id, order_b_id, days_between. Order by customer_id ASC.",
     "Rows: customer_id, order_a_id, order_b_id, days_between",
     "SELECT o1.customer_id, o1.id AS order_a_id, o2.id AS order_b_id, ROUND(EXTRACT(EPOCH FROM (o2.order_date - o1.order_date)) / 86400.0, 1) AS days_between FROM ecommerce.orders o1 JOIN ecommerce.orders o2 ON o1.customer_id = o2.customer_id AND o1.id < o2.id AND o2.order_date >= o1.order_date AND o2.order_date <= o1.order_date + INTERVAL '7 days' ORDER BY o1.customer_id ASC, order_a_id ASC;"),

    ("q85-banking-high-risk-customers", "banking", "Intermediate", ["Risk Analysis", "WHERE"],
     "Find customers with risk_score >= 70 who hold more than $100 in checking balance. Project customer name, tax_id, risk_score, balance. Order by risk_score DESC.",
     "Rows: full_name, tax_id, risk_score, balance",
     "SELECT c.full_name, c.tax_id, c.risk_score, a.balance FROM banking.customers c JOIN banking.accounts a ON c.id = a.customer_id WHERE c.risk_score >= 70 AND a.account_type = 'checking' AND a.balance > 100 ORDER BY c.risk_score DESC;"),

    ("q86-banking-frozen-account-audit", "banking", "Intermediate", ["Audit", "Status"],
     "List all frozen accounts, their owner's name, and current balance. Order by balance DESC.",
     "Rows: account_number, full_name, balance",
     "SELECT a.account_number, c.full_name, a.balance FROM banking.accounts a JOIN banking.customers c ON a.customer_id = c.id WHERE a.is_frozen = TRUE ORDER BY a.balance DESC;"),

    ("q87-saas-enterprise-feature-usage", "saas", "Intermediate", ["JSONB", "Feature Flag"],
     "Count how many times each feature flag has been enabled in 'settings.updated' events. Inspect payload->'feature_flags'. Return count.",
     "1 row: dark_mode_updates",
     "SELECT COUNT(*) AS dark_mode_updates FROM saas.events WHERE event_type = 'settings.updated' AND (payload->'feature_flags'->>'dark_mode')::BOOLEAN = TRUE;"),

    ("q88-social-lurker-ratio", "social", "Intermediate", ["Social", "Ratios"],
     "Calculate the percentage of total users who have zero posts. Return total_users, lurker_count, lurker_pct.",
     "1 row: total_users, lurker_count, lurker_pct",
     "SELECT COUNT(*) AS total_users, COUNT(CASE WHEN p.id IS NULL THEN 1 END) AS lurker_count, ROUND((COUNT(CASE WHEN p.id IS NULL THEN 1 END)::NUMERIC / COUNT(*)) * 100, 2) AS lurker_pct FROM social.users u LEFT JOIN social.posts p ON u.id = p.user_id;"),

    ("q89-null-safe-equality-is-not-distinct", "ecommerce", "Intermediate", ["Standard SQL", "IS NOT DISTINCT FROM"],
     "Compare two queries: select categories where parent_id = NULL vs parent_id IS NOT DISTINCT FROM NULL. Demonstrate standard SQL NULL-safe equality.",
     "3 rows: id, name, parent_id",
     "SELECT id, name, parent_id FROM ecommerce.categories WHERE parent_id IS NOT DISTINCT FROM NULL ORDER BY id ASC;"),

    ("q90-aggregate-with-string-agg", "ecommerce", "Intermediate", ["PostgreSQL Specific", "STRING_AGG"],
     "For each completed order, aggregate product names into a single comma-separated string aliased as product_list. Order by order_id ASC.",
     "Rows: order_id, product_list",
     "SELECT oi.order_id, STRING_AGG(p.name, ', ' ORDER BY p.name ASC) AS product_list FROM ecommerce.order_items oi JOIN ecommerce.products p ON oi.product_id = p.id JOIN ecommerce.orders o ON oi.order_id = o.id WHERE o.status = 'completed' GROUP BY oi.order_id ORDER BY oi.order_id ASC;")
]

for idx, item in enumerate(intermediate_defs, start=41):
    EXERCISES.append({
        "tier": "intermediate",
        "file": f"q{idx:02d}-{item[0].split('-', 1)[1]}",
        "schema": item[1],
        "diff": item[2],
        "tags": item[3],
        "req": item[4],
        "shape": item[5],
        "sql": item[6]
    })

# =====================================================================
# 3. ADVANCED EXERCISES (q91 - q130)
# =====================================================================
advanced_defs = [
    ("q91-recursive-org-chart", "ecommerce", "Advanced", ["Recursive CTE", "Tree Traversal"],
     "Traverse the category hierarchy recursively to calculate category depth (root = 0, child = 1). Return id, name, depth. Order by depth ASC, id ASC.",
     "Rows: id, name, depth",
     "WITH RECURSIVE cat_hierarchy AS (SELECT id, name, parent_id, 0 AS depth FROM ecommerce.categories WHERE parent_id IS NULL UNION ALL SELECT c.id, c.name, c.parent_id, ch.depth + 1 FROM ecommerce.categories c JOIN cat_hierarchy ch ON c.parent_id = ch.id) SELECT id, name, depth FROM cat_hierarchy ORDER BY depth ASC, id ASC;"),

    ("q92-window-row-number-deduplication", "analytics", "Advanced", ["Window", "ROW_NUMBER", "Deduplication"],
     "In event clickstream, find the FIRST event recorded for each session_id using ROW_NUMBER. Project session_id, event_name, event_timestamp. Order by session_id ASC.",
     "Rows: session_id, event_name, event_timestamp",
     "WITH ranked_events AS (SELECT session_id, event_name, event_timestamp, ROW_NUMBER() OVER (PARTITION BY session_id ORDER BY event_timestamp ASC) AS rn FROM analytics.events) SELECT session_id, event_name, event_timestamp FROM ranked_events WHERE rn = 1 ORDER BY session_id ASC;"),

    ("q93-window-rank-vs-dense-rank-ties", "ecommerce", "Advanced", ["Window", "RANK", "DENSE_RANK"],
     "Demonstrate ties: rank products by price within category 2 using both RANK() and DENSE_RANK(). Project name, price, rnk, dense_rnk. Order by price DESC, name ASC.",
     "Rows: name, price, rnk, dense_rnk",
     "SELECT name, price, RANK() OVER (ORDER BY price DESC) AS rnk, DENSE_RANK() OVER (ORDER BY price DESC) AS dense_rnk FROM ecommerce.products WHERE category_id = 2 ORDER BY price DESC, name ASC;"),

    ("q94-window-partition-by-customer-spending", "ecommerce", "Advanced", ["Window", "PARTITION BY"],
     "For all completed orders, compute total customer spend to date on that order and overall customer average order value side-by-side with order details. Order by customer_id ASC, order_date ASC.",
     "Rows: customer_id, id, order_date, total_amount, running_customer_total, avg_customer_order",
     "SELECT customer_id, id, order_date, total_amount, SUM(total_amount) OVER (PARTITION BY customer_id ORDER BY order_date ASC, id ASC) AS running_customer_total, ROUND(AVG(total_amount) OVER (PARTITION BY customer_id), 2) AS avg_customer_order FROM ecommerce.orders WHERE status = 'completed' ORDER BY customer_id ASC, order_date ASC, id ASC;"),

    ("q95-window-lag-mom-revenue-delta", "ecommerce", "Advanced", ["Window", "LAG", "MoM Growth"],
     "Calculate Month-over-Month revenue change: compute monthly completed revenue, previous month revenue via LAG, and dollar delta. Order by order_month ASC.",
     "Rows: order_month, monthly_rev, prev_month_rev, dollar_delta",
     "WITH monthly AS (SELECT DATE_TRUNC('month', order_date)::DATE AS order_month, SUM(total_amount) AS monthly_rev FROM ecommerce.orders WHERE status = 'completed' GROUP BY 1) SELECT order_month, monthly_rev, LAG(monthly_rev, 1) OVER (ORDER BY order_month ASC) AS prev_month_rev, (monthly_rev - LAG(monthly_rev, 1) OVER (ORDER BY order_month ASC)) AS dollar_delta FROM monthly ORDER BY order_month ASC;"),

    ("q96-window-lead-time-to-next-order", "ecommerce", "Advanced", ["Window", "LEAD", "Repurchase"],
     "For customer 1, calculate days elapsed between current order and the NEXT order using LEAD. Project order_id, order_date, next_order_date, days_to_next. Order by order_date ASC.",
     "Rows: order_id, order_date, next_order_date, days_to_next",
     "SELECT id AS order_id, order_date, LEAD(order_date, 1) OVER (ORDER BY order_date ASC) AS next_order_date, ROUND(EXTRACT(EPOCH FROM (LEAD(order_date, 1) OVER (ORDER BY order_date ASC) - order_date)) / 86400.0, 1) AS days_to_next FROM ecommerce.orders WHERE customer_id = 1 ORDER BY order_date ASC;"),

    ("q97-window-running-total-frames", "ecommerce", "Advanced", ["Window", "ROWS BETWEEN"],
     "Compute cumulative completed revenue using explicit window frame: ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW. Project order_id, order_date, total_amount, cumulative_revenue. Order by order_date ASC.",
     "Rows: order_id, order_date, total_amount, cumulative_revenue",
     "SELECT id AS order_id, order_date, total_amount, SUM(total_amount) OVER (ORDER BY order_date ASC, id ASC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cumulative_revenue FROM ecommerce.orders WHERE status = 'completed' ORDER BY order_date ASC, order_id ASC;"),

    ("q98-window-moving-average-7-day", "ecommerce", "Advanced", ["Window", "Moving Average"],
     "Calculate moving average over last 3 completed orders (current and 2 preceding). Project order_id, total_amount, moving_avg. Order by order_date ASC.",
     "Rows: order_id, total_amount, moving_avg",
     "SELECT id AS order_id, total_amount, ROUND(AVG(total_amount) OVER (ORDER BY order_date ASC, id ASC ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 2) AS moving_avg FROM ecommerce.orders WHERE status = 'completed' ORDER BY order_date ASC, order_id ASC;"),

    ("q99-top-n-per-group-category-products", "ecommerce", "Advanced", ["Window", "Top-N", "DENSE_RANK"],
     "Find top 2 highest revenue products in each category. Join order_items, orders, products. Use DENSE_RANK. Order by category_id ASC, rank ASC, product_name ASC.",
     "Rows: category_id, product_name, product_rev, rank",
     "WITH product_sales AS (SELECT p.category_id, p.name AS product_name, SUM(oi.subtotal) AS product_rev FROM ecommerce.order_items oi JOIN ecommerce.orders o ON oi.order_id = o.id JOIN ecommerce.products p ON oi.product_id = p.id WHERE o.status = 'completed' GROUP BY p.category_id, p.id, p.name), ranked AS (SELECT category_id, product_name, product_rev, DENSE_RANK() OVER (PARTITION BY category_id ORDER BY product_rev DESC) AS rnk FROM product_sales) SELECT category_id, product_name, product_rev, rnk AS rank FROM ranked WHERE rnk <= 2 ORDER BY category_id ASC, rank ASC, product_name ASC;"),

    ("q100-event-deduplication-keep-latest", "analytics", "Advanced", ["Deduplication", "ROW_NUMBER"],
     "Given potential duplicate events per session and event_name, select ONLY the latest occurrence. Project session_id, event_name, event_timestamp. Order by session_id ASC, event_timestamp ASC.",
     "Rows: session_id, event_name, event_timestamp",
     "WITH ranked AS (SELECT session_id, event_name, event_timestamp, ROW_NUMBER() OVER (PARTITION BY session_id, event_name ORDER BY event_timestamp DESC, id DESC) AS rn FROM analytics.events) SELECT session_id, event_name, event_timestamp FROM ranked WHERE rn = 1 ORDER BY session_id ASC, event_timestamp ASC;"),

    ("q101-gaps-and-islands-consecutive-days", "analytics", "Advanced", ["Gaps and Islands", "Date Arithmetic"],
     "Identify consecutive active login days for user 101: group consecutive days into islands by subtracting ROW_NUMBER() days from event date. Project island_start, island_end, streak_length. Order by island_start ASC.",
     "Rows: island_start, island_end, streak_length",
     "WITH user_days AS (SELECT DISTINCT event_timestamp::DATE AS active_date FROM analytics.events WHERE user_id = 101), numbered AS (SELECT active_date, active_date - (ROW_NUMBER() OVER (ORDER BY active_date)) * INTERVAL '1 day' AS grp FROM user_days) SELECT MIN(active_date) AS island_start, MAX(active_date) AS island_end, COUNT(*) AS streak_length FROM numbered GROUP BY grp ORDER BY island_start ASC;"),

    ("q102-conversion-funnel-step-counts", "analytics", "Advanced", ["Funnel", "Conversion"],
     "Compute complete e-commerce conversion funnel counts: step 1 (page_view), step 2 (sign_up), step 3 (view_product), step 4 (add_to_cart), step 5 (purchase). Return unique user count at each stage.",
     "1 row, 5 columns: step1_view, step2_signup, step3_prod, step4_cart, step5_purchase",
     "SELECT COUNT(DISTINCT CASE WHEN event_name = 'page_view' THEN user_id END) AS step1_view, COUNT(DISTINCT CASE WHEN event_name = 'sign_up' THEN user_id END) AS step2_signup, COUNT(DISTINCT CASE WHEN event_name = 'view_product' THEN user_id END) AS step3_prod, COUNT(DISTINCT CASE WHEN event_name = 'add_to_cart' THEN user_id END) AS step4_cart, COUNT(DISTINCT CASE WHEN event_name = 'purchase' THEN user_id END) AS step5_purchase FROM analytics.events;"),

    ("q103-cohort-retention-matrix", "analytics", "Advanced", ["Cohort Analysis", "Retention"],
     "Calculate Month 0 and Month 1 retention counts for user cohorts: count users active in their cohort month vs active 1 month later. Order by cohort_month ASC.",
     "Rows: cohort_month, cohort_size, m1_active, m1_retention_pct",
     "WITH cohort_base AS (SELECT cohort_month, user_id FROM analytics.user_cohorts), m1_activity AS (SELECT DISTINCT uc.cohort_month, e.user_id FROM analytics.user_cohorts uc JOIN analytics.events e ON uc.user_id = e.user_id WHERE DATE_TRUNC('month', e.event_timestamp)::DATE = uc.cohort_month + INTERVAL '1 month') SELECT cb.cohort_month, COUNT(DISTINCT cb.user_id) AS cohort_size, COUNT(DISTINCT m1.user_id) AS m1_active, ROUND((COUNT(DISTINCT m1.user_id)::NUMERIC / NULLIF(COUNT(DISTINCT cb.user_id), 0)) * 100, 2) AS m1_retention_pct FROM cohort_base cb LEFT JOIN m1_activity m1 ON cb.cohort_month = m1.cohort_month AND cb.user_id = m1.user_id GROUP BY cb.cohort_month ORDER BY cb.cohort_month ASC;"),

    ("q104-day-1-7-30-retention-concept", "analytics", "Advanced", ["Retention", "Intervals"],
     "Count users who logged back in exactly within 7 days of their first seen date. Project first_seen_date, total_users, retained_7d. Order by first_seen_date ASC.",
     "Rows: first_seen_date, total_users, retained_7d",
     "SELECT uc.first_seen_at::DATE AS first_seen_date, COUNT(DISTINCT uc.user_id) AS total_users, COUNT(DISTINCT e.user_id) AS retained_7d FROM analytics.user_cohorts uc LEFT JOIN analytics.events e ON uc.user_id = e.user_id AND e.event_timestamp > uc.first_seen_at AND e.event_timestamp <= uc.first_seen_at + INTERVAL '7 days' GROUP BY 1 ORDER BY first_seen_date ASC;"),

    ("q105-pivot-revenue-by-month-category", "ecommerce", "Advanced", ["Pivot", "Conditional Aggregate"],
     "Pivot revenue for 2026: columns for category_name, jan_revenue, feb_revenue, mar_revenue. Order by category_name ASC.",
     "Rows: category_name, jan_revenue, feb_revenue, mar_revenue",
     "SELECT c.name AS category_name, COALESCE(SUM(CASE WHEN EXTRACT(MONTH FROM o.order_date) = 1 THEN oi.subtotal END), 0.00) AS jan_revenue, COALESCE(SUM(CASE WHEN EXTRACT(MONTH FROM o.order_date) = 2 THEN oi.subtotal END), 0.00) AS feb_revenue, COALESCE(SUM(CASE WHEN EXTRACT(MONTH FROM o.order_date) = 3 THEN oi.subtotal END), 0.00) AS mar_revenue FROM ecommerce.categories c LEFT JOIN ecommerce.products p ON c.id = p.category_id LEFT JOIN ecommerce.order_items oi ON p.id = oi.product_id LEFT JOIN ecommerce.orders o ON oi.order_id = o.id AND o.status = 'completed' GROUP BY c.id, c.name ORDER BY category_name ASC;"),

    ("q106-sessionization-30-min-timeout", "analytics", "Advanced", ["Sessionization", "Window LAG"],
     "Reconstruct user browsing sessions: if duration between consecutive events exceeds 30 minutes, flag new session start (is_new_session = 1). Project user_id, event_timestamp, is_new_session. Order by user_id ASC, event_timestamp ASC.",
     "Rows: user_id, event_timestamp, is_new_session",
     "SELECT user_id, event_timestamp, CASE WHEN LAG(event_timestamp) OVER (PARTITION BY user_id ORDER BY event_timestamp ASC) IS NULL OR event_timestamp - LAG(event_timestamp) OVER (PARTITION BY user_id ORDER BY event_timestamp ASC) > INTERVAL '30 minutes' THEN 1 ELSE 0 END AS is_new_session FROM analytics.events WHERE user_id = 101 ORDER BY user_id ASC, event_timestamp ASC;"),

    ("q107-customer-lifetime-value-distribution", "ecommerce", "Advanced", ["LTV", "Percentiles"],
     "Calculate Customer Lifetime Value (LTV) for completed orders, and divide customers into 3 LTV tiers: Top 20% ('VIP'), Middle 50% ('Core'), Bottom 30% ('Standard') using NTILE or PERCENT_RANK. Order by ltv DESC.",
     "Rows: customer_id, ltv, ltv_tier",
     "WITH cust_ltv AS (SELECT customer_id, SUM(total_amount) AS ltv FROM ecommerce.orders WHERE status = 'completed' GROUP BY customer_id), ranked AS (SELECT customer_id, ltv, PERCENT_RANK() OVER (ORDER BY ltv DESC) AS pct_rank FROM cust_ltv) SELECT customer_id, ltv, CASE WHEN pct_rank <= 0.20 THEN 'VIP' WHEN pct_rank <= 0.70 THEN 'Core' ELSE 'Standard' END AS ltv_tier FROM ranked ORDER BY ltv DESC, customer_id ASC;"),

    ("q108-percentile-disc-cont-postgres", "ecommerce", "Advanced", ["PostgreSQL Specific", "PERCENTILE_CONT"],
     "Compute the exact 50th percentile (median) and 90th percentile of completed order amounts using PostgreSQL's WITHIN GROUP clause.",
     "1 row: median_order_val, p90_order_val",
     "SELECT PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY total_amount) AS median_order_val, PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY total_amount) AS p90_order_val FROM ecommerce.orders WHERE status = 'completed';"),

    ("q109-first-value-last-value-frame-trap", "ecommerce", "Advanced", ["Window", "Window Frame Trap"],
     "Demonstrate the default RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW trap with LAST_VALUE, and fix it using explicit UNBOUNDED FOLLOWING. Return order_id, total_amount, highest_order_amount.",
     "Rows: id, total_amount, highest_order_amount",
     "SELECT id, total_amount, LAST_VALUE(total_amount) OVER (ORDER BY total_amount ASC ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS highest_order_amount FROM ecommerce.orders WHERE status = 'completed' ORDER BY id ASC;"),

    ("q110-consecutive-increasing-spending", "ecommerce", "Advanced", ["Window", "Trend Detection"],
     "Identify customers whose order amounts increased across two consecutive completed orders. Use LAG. Project customer_id, order_a_val, order_b_val. Order by customer_id ASC.",
     "Rows: customer_id, prev_amount, curr_amount",
     "WITH order_seq AS (SELECT customer_id, id, total_amount, LAG(total_amount) OVER (PARTITION BY customer_id ORDER BY order_date ASC) AS prev_amount FROM ecommerce.orders WHERE status = 'completed') SELECT customer_id, prev_amount, total_amount AS curr_amount FROM order_seq WHERE prev_amount IS NOT NULL AND total_amount > prev_amount ORDER BY customer_id ASC;"),

    ("q111-recursive-path-accumulation", "ecommerce", "Advanced", ["Recursive CTE", "Breadcrumbs"],
     "Construct full slug paths for all categories (e.g. '/electronics/audio-headphones'). Order by path ASC.",
     "Rows: id, path",
     "WITH RECURSIVE cat_slugs AS (SELECT id, slug, parent_id, ('/' || slug)::TEXT AS path FROM ecommerce.categories WHERE parent_id IS NULL UNION ALL SELECT c.id, c.slug, c.parent_id, (cs.path || '/' || c.slug)::TEXT AS path FROM ecommerce.categories c JOIN cat_slugs cs ON c.parent_id = cs.id) SELECT id, path FROM cat_slugs ORDER BY path ASC;"),

    ("q112-cross-tab-product-affinity", "ecommerce", "Advanced", ["Market Basket", "Self Join"],
     "Market Basket Analysis: find pairs of products frequently bought together in the same order. Project prod_a_id, prod_b_id, co_purchase_count where prod_a_id < prod_b_id. Order by co_purchase_count DESC.",
     "Rows: prod_a_id, prod_b_id, co_purchase_count",
     "SELECT oi1.product_id AS prod_a_id, oi2.product_id AS prod_b_id, COUNT(*) AS co_purchase_count FROM ecommerce.order_items oi1 JOIN ecommerce.order_items oi2 ON oi1.order_id = oi2.order_id AND oi1.product_id < oi2.product_id JOIN ecommerce.orders o ON oi1.order_id = o.id WHERE o.status = 'completed' GROUP BY oi1.product_id, oi2.product_id ORDER BY co_purchase_count DESC, prod_a_id ASC;"),

    ("q113-saas-churn-prediction-candidates", "saas", "Advanced", ["SaaS", "Churn Heuristics"],
     "Flag churn risk organizations: organizations whose subscription is active or past_due, but have generated 0 telemetry events in the last 30 days. Order by id ASC.",
     "Rows: id, name, status",
     "SELECT o.id, o.name, s.status FROM saas.organizations o JOIN saas.subscriptions s ON o.id = s.organization_id WHERE s.status IN ('active', 'past_due') AND NOT EXISTS (SELECT 1 FROM saas.events e WHERE e.organization_id = o.id AND e.created_at >= '2026-02-15 00:00:00+00') ORDER BY o.id ASC;"),

    ("q114-banking-optimistic-locking-verification", "banking", "Advanced", ["Concurrency", "Optimistic Lock"],
     "Simulate optimistic lock verification: write a conditional query checking account balance >= 500 and version = 12 before allowing an update. Project id, balance, version, is_updatable.",
     "Rows: id, balance, version, is_updatable",
     "SELECT id, balance, version, (balance >= 500.00 AND version = 12) AS is_updatable FROM banking.accounts WHERE id = 1;"),

    ("q115-complex-reporting-rolling-revenue", "ecommerce", "Advanced", ["Window", "Rolling 30-Day Window"],
     "For each day with completed orders, calculate daily revenue and rolling 30-day cumulative revenue using window range. Order by order_day ASC.",
     "Rows: order_day, daily_rev, rolling_30d_rev",
     "WITH daily AS (SELECT order_date::DATE AS order_day, SUM(total_amount) AS daily_rev FROM ecommerce.orders WHERE status = 'completed' GROUP BY 1) SELECT order_day, daily_rev, SUM(daily_rev) OVER (ORDER BY order_day ASC ROWS BETWEEN 29 PRECEDING AND CURRENT ROW) AS rolling_30d_rev FROM daily ORDER BY order_day ASC;"),

    ("q116-social-second-degree-friends", "social", "Advanced", ["Social Graph", "Graph Traversal"],
     "Find 'Friends of Friends' (second degree follows) for user 1: people followed by people user 1 follows, who user 1 does not already follow. Project recommended_user_id. Order by recommended_user_id ASC.",
     "Rows: recommended_user_id",
     "SELECT DISTINCT f2.following_id AS recommended_user_id FROM social.follows f1 JOIN social.follows f2 ON f1.following_id = f2.follower_id WHERE f1.follower_id = 1 AND f2.following_id != 1 AND f2.following_id NOT IN (SELECT following_id FROM social.follows WHERE follower_id = 1) ORDER BY recommended_user_id ASC;"),

    ("q117-gap-detection-sequence-numbers", "banking", "Advanced", ["Gaps", "Sequence Integrity"],
     "Detect any missing IDs in a sequence: generate integer sequence from 1 to 10 and identify which IDs do not exist in accounts table. Return missing_id. Order by missing_id ASC.",
     "Rows: missing_id",
     "SELECT s.id AS missing_id FROM generate_series(1, 10) AS s(id) LEFT JOIN banking.accounts a ON s.id = a.id WHERE a.id IS NULL ORDER BY missing_id ASC;"),

    ("q118-window-cume-dist-percentiles", "ecommerce", "Advanced", ["Window", "CUME_DIST"],
     "Calculate cumulative distribution CUME_DIST() of order totals. Project id, total_amount, cume_dist_val. Order by total_amount ASC.",
     "Rows: id, total_amount, cume_dist_val",
     "SELECT id, total_amount, ROUND(CUME_DIST() OVER (ORDER BY total_amount ASC)::NUMERIC, 4) AS cume_dist_val FROM ecommerce.orders WHERE status = 'completed' ORDER BY total_amount ASC, id ASC;"),

    ("q119-multi-tenant-data-isolation-check", "saas", "Advanced", ["Multi-Tenancy", "Security"],
     "Write a multi-tenant query ensuring user 1 (Acme Corp) only accesses projects belonging to organization 1. Return project_id, project_name. Order by id ASC.",
     "Rows: id, name",
     "SELECT p.id, p.name FROM saas.projects p JOIN saas.memberships m ON p.organization_id = m.organization_id WHERE m.user_id = 1 AND p.organization_id = 1 ORDER BY p.id ASC;"),

    ("q120-hierarchical-tree-cycle-prevention", "ecommerce", "Advanced", ["Recursive CTE", "Cycle Prevention"],
     "Write a recursive query with cycle detection tracking array of visited IDs to prevent infinite loops in bad graph data. Project id, name, cycle_detected.",
     "Rows: id, name, cycle_detected",
     "WITH RECURSIVE safe_tree AS (SELECT id, name, parent_id, ARRAY[id] AS visited, FALSE AS cycle_detected FROM ecommerce.categories WHERE parent_id IS NULL UNION ALL SELECT c.id, c.name, c.parent_id, st.visited || c.id, c.id = ANY(st.visited) FROM ecommerce.categories c JOIN safe_tree st ON c.parent_id = st.id WHERE NOT st.cycle_detected) SELECT id, name, cycle_detected FROM safe_tree ORDER BY id ASC;"),

    ("q121-running-inventory-depletion", "ecommerce", "Advanced", ["Inventory", "Window Simulation"],
     "Simulate inventory depletion: for product 1, show orders requesting it in order_date order, quantity requested, and remaining simulated stock starting from 45. Order by order_date ASC.",
     "Rows: order_id, order_date, quantity, remaining_stock",
     "SELECT oi.order_id, o.order_date, oi.quantity, (45 - SUM(oi.quantity) OVER (ORDER BY o.order_date ASC, oi.order_id ASC)) AS remaining_stock FROM ecommerce.order_items oi JOIN ecommerce.orders o ON oi.order_id = o.id WHERE oi.product_id = 1 AND o.status = 'completed' ORDER BY o.order_date ASC;"),

    ("q122-window-range-vs-rows-difference", "ecommerce", "Advanced", ["Window", "RANGE vs ROWS"],
     "Demonstrate the critical difference between RANGE and ROWS frames when duplicate timestamps or values exist. Project order_id, total_amount, rows_sum, range_sum. Order by total_amount ASC.",
     "Rows: id, total_amount, rows_sum, range_sum",
     "SELECT id, total_amount, SUM(total_amount) OVER (ORDER BY total_amount ASC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS rows_sum, SUM(total_amount) OVER (ORDER BY total_amount ASC RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS range_sum FROM ecommerce.orders WHERE status = 'completed' ORDER BY total_amount ASC, id ASC;"),

    ("q123-funnel-drop-off-percentage", "analytics", "Advanced", ["Funnel", "Drop-Off"],
     "Calculate the conversion percentage from page_view to purchase per acquisition campaign. Join campaigns, sessions, events. Order by conversion_rate DESC.",
     "Rows: campaign_name, views, purchases, conversion_rate",
     "SELECT c.name AS campaign_name, COUNT(DISTINCT CASE WHEN e.event_name = 'page_view' THEN s.user_id END) AS views, COUNT(DISTINCT CASE WHEN e.event_name = 'purchase' THEN s.user_id END) AS purchases, ROUND((COUNT(DISTINCT CASE WHEN e.event_name = 'purchase' THEN s.user_id END)::NUMERIC / NULLIF(COUNT(DISTINCT CASE WHEN e.event_name = 'page_view' THEN s.user_id END), 0)) * 100, 2) AS conversion_rate FROM analytics.campaigns c JOIN analytics.sessions s ON c.id = s.campaign_id JOIN analytics.events e ON s.id = e.session_id GROUP BY c.id, c.name ORDER BY conversion_rate DESC NULLS LAST;"),

    ("q124-social-network-influence-score", "social", "Advanced", ["Graph", "Influence"],
     "Calculate PageRank-style simplified influence score: user's follower count + total likes received across all authored posts. Project user_id, username, score. Order by score DESC.",
     "Rows: user_id, username, influence_score",
     "SELECT u.id AS user_id, u.username, (COALESCE(fc.follower_count, 0) + COALESCE(lc.likes_count, 0)) AS influence_score FROM social.users u LEFT JOIN (SELECT following_id, COUNT(*) AS follower_count FROM social.follows GROUP BY following_id) fc ON u.id = fc.following_id LEFT JOIN (SELECT p.user_id, COUNT(l.user_id) AS likes_count FROM social.posts p JOIN social.likes l ON p.id = l.post_id GROUP BY p.user_id) lc ON u.id = lc.user_id ORDER BY influence_score DESC, user_id ASC;"),

    ("q125-banking-audit-trail-reconstruction", "banking", "Advanced", ["Audit", "JSONB Diff"],
     "Reconstruct entity history from audit_log: for account table changes, extract old balance and new balance from JSONB states. Project record_id, action, timestamp. Order by timestamp ASC.",
     "Rows: record_id, action, timestamp",
     "SELECT record_id, action, timestamp FROM banking.audit_log WHERE table_name = 'accounts' ORDER BY timestamp ASC;"),

    ("q126-cohort-size-normalization", "analytics", "Advanced", ["Cohorts", "Normalization"],
     "Compute signup cohort sizes for each month and return normalized user counts. Order by cohort_month ASC.",
     "Rows: cohort_month, total_users",
     "SELECT cohort_month, COUNT(*) AS total_users FROM analytics.user_cohorts GROUP BY cohort_month ORDER BY cohort_month ASC;"),

    ("q127-median-spending-by-city", "ecommerce", "Advanced", ["Window", "Median"],
     "Calculate median order total per shipping city. Join orders, addresses. Project city, median_spent. Order by median_spent DESC.",
     "Rows: city, median_spent",
     "SELECT a.city, PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY o.total_amount) AS median_spent FROM ecommerce.orders o JOIN ecommerce.addresses a ON o.shipping_address_id = a.id WHERE o.status = 'completed' GROUP BY a.city ORDER BY median_spent DESC;"),

    ("q128-jsonb-array-elements-expansion", "saas", "Advanced", ["JSONB", "jsonb_array_elements"],
     "Demonstrate JSONB array unnesting: if payload has tags array, expand with jsonb_array_elements_text. Return payload.",
     "Rows: id, payload",
     "SELECT id, payload FROM saas.events WHERE payload ? 'version' ORDER BY id ASC;"),

    ("q129-running-count-active-subscriptions", "saas", "Advanced", ["SaaS", "Active Subscriptions"],
     "Count currently active subscriptions vs trialing and past due subscriptions. Project status, sub_count, total_mrr. Order by status ASC.",
     "Rows: status, sub_count, total_mrr",
     "SELECT status, COUNT(*) AS sub_count, SUM(monthly_price) AS total_mrr FROM saas.subscriptions GROUP BY status ORDER BY status ASC;"),

    ("q130-anti-join-zero-purchase-sessions", "analytics", "Advanced", ["Anti-Join", "Sessions"],
     "Find sessions that viewed products but never reached checkout. Project session id and user_id. Order by session id ASC.",
     "Rows: session_id, user_id",
     "SELECT DISTINCT s.id AS session_id, s.user_id FROM analytics.sessions s JOIN analytics.events e ON s.id = e.session_id WHERE e.event_name = 'view_product' AND NOT EXISTS (SELECT 1 FROM analytics.events e2 WHERE e2.session_id = s.id AND e2.event_name IN ('begin_checkout', 'purchase')) ORDER BY session_id ASC;")
]

for idx, item in enumerate(advanced_defs, start=91):
    EXERCISES.append({
        "tier": "advanced",
        "file": f"q{idx:02d}-{item[0].split('-', 1)[1]}",
        "schema": item[1],
        "diff": item[2],
        "tags": item[3],
        "req": item[4],
        "shape": item[5],
        "sql": item[6]
    })

# =====================================================================
# 4. CHALLENGE EXERCISES (q131 - q160)
# =====================================================================
challenge_defs = [
    ("q131-top-three-products-by-category-revenue", "ecommerce", "Challenge", ["Window", "Top-N", "Business Core"],
     "Find the top 3 products by revenue for each category over completed orders, excluding refunds. Project category_name, product_name, revenue, rank. Order by category_name ASC, rank ASC, revenue DESC.",
     "Rows: category_name, product_name, revenue, rank",
     "WITH product_revenue AS (SELECT c.name AS category_name, p.name AS product_name, SUM(oi.subtotal) AS revenue FROM ecommerce.order_items oi JOIN ecommerce.orders o ON oi.order_id = o.id JOIN ecommerce.products p ON oi.product_id = p.id JOIN ecommerce.categories c ON p.category_id = c.id WHERE o.status = 'completed' AND NOT EXISTS (SELECT 1 FROM ecommerce.refunds r WHERE r.order_id = o.id) GROUP BY c.name, p.name), ranked AS (SELECT category_name, product_name, revenue, DENSE_RANK() OVER (PARTITION BY category_name ORDER BY revenue DESC) AS rnk FROM product_revenue) SELECT category_name, product_name, revenue, rnk AS rank FROM ranked WHERE rnk <= 3 ORDER BY category_name ASC, rank ASC, revenue DESC;"),

    ("q132-customer-second-purchase-within-30-days", "ecommerce", "Challenge", ["Window", "Repurchase Lag"],
     "Find customers whose second order occurred within 30 days of their first order. Project customer_id, first_order_date, second_order_date, days_between. Order by customer_id ASC.",
     "Rows: customer_id, first_order_date, second_order_date, days_between",
     "WITH ordered_purchases AS (SELECT customer_id, order_date, ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date ASC) AS purchase_num FROM ecommerce.orders WHERE status = 'completed'), paired AS (SELECT p1.customer_id, p1.order_date AS first_order_date, p2.order_date AS second_order_date, ROUND(EXTRACT(EPOCH FROM (p2.order_date - p1.order_date)) / 86400.0, 1) AS days_between FROM ordered_purchases p1 JOIN ordered_purchases p2 ON p1.customer_id = p2.customer_id AND p1.purchase_num = 1 AND p2.purchase_num = 2) SELECT customer_id, first_order_date, second_order_date, days_between FROM paired WHERE days_between <= 30.0 ORDER BY customer_id ASC;"),

    ("q133-rolling-seven-day-revenue", "ecommerce", "Challenge", ["Window", "Rolling Scaffolding"],
     "Calculate rolling 7-day revenue for every calendar day in January 2026. Use generate_series to guarantee no missing dates. Order by calendar_day ASC.",
     "Rows: calendar_day, daily_revenue, rolling_7d_revenue",
     "WITH calendar AS (SELECT d::DATE AS calendar_day FROM generate_series('2026-01-01'::DATE, '2026-01-31'::DATE, '1 day'::INTERVAL) d), daily_sales AS (SELECT order_date::DATE AS order_day, SUM(total_amount) AS revenue FROM ecommerce.orders WHERE status = 'completed' GROUP BY 1) SELECT c.calendar_day, COALESCE(ds.revenue, 0.00) AS daily_revenue, SUM(COALESCE(ds.revenue, 0.00)) OVER (ORDER BY c.calendar_day ASC ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS rolling_7d_revenue FROM calendar c LEFT JOIN daily_sales ds ON c.calendar_day = ds.order_day ORDER BY c.calendar_day ASC;"),

    ("q134-consecutive-active-days-islands", "analytics", "Challenge", ["Gaps and Islands", "Mastery"],
     "Find all users who were active for at least 3 consecutive days in January 2026. Project user_id, streak_start, streak_end, streak_days. Order by user_id ASC, streak_start ASC.",
     "Rows: user_id, streak_start, streak_end, streak_days",
     "WITH user_dates AS (SELECT DISTINCT user_id, event_timestamp::DATE AS active_day FROM analytics.events WHERE event_timestamp >= '2026-01-01' AND event_timestamp < '2026-02-01'), grouped_islands AS (SELECT user_id, active_day, active_day - (ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY active_day ASC)) * INTERVAL '1 day' AS island_id FROM user_dates) SELECT user_id, MIN(active_day) AS streak_start, MAX(active_day) AS streak_end, COUNT(*) AS streak_days FROM grouped_islands GROUP BY user_id, island_id HAVING COUNT(*) >= 3 ORDER BY user_id ASC, streak_start ASC;"),

    ("q135-monthly-retention-cohort-analysis", "analytics", "Challenge", ["Cohorts", "Retention Table"],
     "Generate a cohort retention report: for each signup cohort month, display cohort size, count active in Month 0, count active in Month 1, and retention percentage. Order by cohort_month ASC.",
     "Rows: cohort_month, cohort_size, m0_users, m1_users, m1_retention_rate",
     "WITH cohorts AS (SELECT user_id, cohort_month FROM analytics.user_cohorts), activity AS (SELECT DISTINCT uc.user_id, uc.cohort_month, EXTRACT(MONTH FROM AGE(DATE_TRUNC('month', e.event_timestamp), uc.cohort_month))::INT AS month_offset FROM analytics.user_cohorts uc JOIN analytics.events e ON uc.user_id = e.user_id) SELECT c.cohort_month, COUNT(DISTINCT c.user_id) AS cohort_size, COUNT(DISTINCT CASE WHEN a.month_offset = 0 THEN a.user_id END) AS m0_users, COUNT(DISTINCT CASE WHEN a.month_offset = 1 THEN a.user_id END) AS m1_users, ROUND((COUNT(DISTINCT CASE WHEN a.month_offset = 1 THEN a.user_id END)::NUMERIC / NULLIF(COUNT(DISTINCT c.user_id), 0)) * 100, 2) AS m1_retention_rate FROM cohorts c LEFT JOIN activity a ON c.user_id = a.user_id GROUP BY c.cohort_month ORDER BY c.cohort_month ASC;"),

    ("q136-deduplicate-payments-keep-latest-valid", "ecommerce", "Challenge", ["Data Hygiene", "Window ROW_NUMBER"],
     "Identify duplicate completed payments for the same order_id: keep the newest record (by created_at, id) and list all duplicate records that should be purged. Project id, order_id, created_at. Order by order_id ASC, id ASC.",
     "Rows: id, order_id, created_at",
     "WITH ranked_payments AS (SELECT id, order_id, created_at, ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY created_at DESC, id DESC) AS rn FROM ecommerce.payments WHERE status = 'completed') SELECT id, order_id, created_at FROM ranked_payments WHERE rn > 1 ORDER BY order_id ASC, id ASC;"),

    ("q137-conversion-funnel-step-rates", "analytics", "Challenge", ["Funnel", "Step-to-Step"],
     "Calculate step-to-step drop-off for conversion: Step 1 (page_view), Step 2 (sign_up), Step 3 (purchase). Calculate step1_count, step2_count, step3_count, step1_to_2_pct, step2_to_3_pct.",
     "1 row: step1_count, step2_count, step3_count, step1_to_2_pct, step2_to_3_pct",
     "WITH steps AS (SELECT COUNT(DISTINCT CASE WHEN event_name = 'page_view' THEN user_id END) AS s1, COUNT(DISTINCT CASE WHEN event_name = 'sign_up' THEN user_id END) AS s2, COUNT(DISTINCT CASE WHEN event_name = 'purchase' THEN user_id END) AS s3 FROM analytics.events) SELECT s1 AS step1_count, s2 AS step2_count, s3 AS step3_count, ROUND((s2::NUMERIC / NULLIF(s1, 0)) * 100, 2) AS step1_to_2_pct, ROUND((s3::NUMERIC / NULLIF(s2, 0)) * 100, 2) AS step2_to_3_pct FROM steps;"),

    ("q138-double-entry-trial-balance-audit", "banking", "Challenge", ["Banking", "Accounting"],
     "Generate a complete General Ledger Trial Balance: for every account, calculate net balance from ledger entries (Credits - Debits or Debits - Credits per account type) and verify that overall debits equal overall credits across the entire institution.",
     "1 row: total_system_debits, total_system_credits, system_balance_delta",
     "SELECT SUM(CASE WHEN entry_type = 'DEBIT' THEN amount ELSE 0 END) AS total_system_debits, SUM(CASE WHEN entry_type = 'CREDIT' THEN amount ELSE 0 END) AS total_system_credits, (SUM(CASE WHEN entry_type = 'DEBIT' THEN amount ELSE 0 END) - SUM(CASE WHEN entry_type = 'CREDIT' THEN amount ELSE 0 END)) AS system_balance_delta FROM banking.ledger_entries;"),

    ("q139-saas-mrr-cohort-waterfall", "saas", "Challenge", ["SaaS", "Financial Modeling"],
     "Construct an MRR report showing total active subscriptions, total MRR, average revenue per organization (ARPO), and enterprise tier share percentage. Order by total_mrr DESC.",
     "1 row: active_subs, total_mrr, arpo, enterprise_share_pct",
     "SELECT COUNT(*) AS active_subs, SUM(monthly_price) AS total_mrr, ROUND(AVG(monthly_price), 2) AS arpo, ROUND((SUM(CASE WHEN o.plan_tier = 'enterprise' THEN s.monthly_price ELSE 0 END) / SUM(monthly_price)) * 100, 2) AS enterprise_share_pct FROM saas.subscriptions s JOIN saas.organizations o ON s.organization_id = o.id WHERE s.status = 'active';"),

    ("q140-social-graph-triangle-detection", "social", "Challenge", ["Graph", "Triangles"],
     "Detect social triangles (triads of mutual followers): user A follows B, B follows C, C follows A where user A < B < C. Return user_a, user_b, user_c. Order by user_a, user_b, user_c.",
     "Rows: user_a, user_b, user_c",
     "SELECT f1.follower_id AS user_a, f2.follower_id AS user_b, f3.follower_id AS user_c FROM social.follows f1 JOIN social.follows f2 ON f1.following_id = f2.follower_id JOIN social.follows f3 ON f2.following_id = f3.follower_id AND f3.following_id = f1.follower_id WHERE f1.follower_id < f2.follower_id AND f2.follower_id < f3.follower_id ORDER BY user_a ASC, user_b ASC, user_c ASC;"),

    ("q141-inventory-stockout-projection", "ecommerce", "Challenge", ["Inventory", "Demand Forecasting"],
     "Forecast stockout risk: calculate average daily units sold over the last 60 days, and divide current stock_quantity by daily run rate to estimate days_until_stockout. Project sku, stock_quantity, days_until_stockout. Order by days_until_stockout ASC.",
     "Rows: sku, stock_quantity, days_until_stockout",
     "WITH daily_velocity AS (SELECT oi.product_id, SUM(oi.quantity) / 60.0 AS daily_units_sold FROM ecommerce.order_items oi JOIN ecommerce.orders o ON oi.order_id = o.id WHERE o.status = 'completed' AND o.order_date >= '2026-01-01' GROUP BY oi.product_id) SELECT p.sku, i.stock_quantity, ROUND(i.stock_quantity / NULLIF(dv.daily_units_sold, 0), 1) AS days_until_stockout FROM ecommerce.products p JOIN ecommerce.inventory i ON p.id = i.product_id LEFT JOIN daily_velocity dv ON p.id = dv.product_id ORDER BY days_until_stockout ASC NULLS LAST, p.sku ASC;"),

    ("q142-customer-order-frequency-intervals", "ecommerce", "Challenge", ["Window", "Intervals"],
     "For customers with at least 3 orders, calculate the average interval in days between their successive orders. Project customer_id, order_count, avg_days_between_orders. Order by avg_days_between_orders ASC.",
     "Rows: customer_id, order_count, avg_days_between_orders",
     "WITH order_intervals AS (SELECT customer_id, order_date, EXTRACT(EPOCH FROM (order_date - LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date ASC))) / 86400.0 AS days_gap FROM ecommerce.orders WHERE status = 'completed') SELECT customer_id, COUNT(*) AS order_count, ROUND(AVG(days_gap)::NUMERIC, 1) AS avg_days_between_orders FROM order_intervals GROUP BY customer_id HAVING COUNT(*) >= 3 ORDER BY avg_days_between_orders ASC;"),

    ("q143-session-referrer-attribution", "analytics", "Challenge", ["Marketing", "Attribution"],
     "Multi-touch attribution: identify the first marketing campaign that touched each customer prior to their first purchase. Return user_id, acquisition_campaign. Order by user_id ASC.",
     "Rows: user_id, acquisition_campaign",
     "WITH first_sessions AS (SELECT s.user_id, c.name AS acquisition_campaign, ROW_NUMBER() OVER (PARTITION BY s.user_id ORDER BY s.started_at ASC) AS rn FROM analytics.sessions s JOIN analytics.campaigns c ON s.campaign_id = c.id) SELECT user_id, acquisition_campaign FROM first_sessions WHERE rn = 1 ORDER BY user_id ASC;"),

    ("q144-banking-fraud-velocity-alert", "banking", "Challenge", ["Fraud Detection", "Velocity"],
     "Detect potential financial fraud: accounts with 2 or more debit transactions occurring within 60 minutes of each other. Project account_id, txn1_id, txn2_id, minutes_delta. Order by account_id ASC.",
     "Rows: account_id, txn1_id, txn2_id, minutes_delta",
     "SELECT le1.account_id, le1.transaction_id AS txn1_id, le2.transaction_id AS txn2_id, ROUND(EXTRACT(EPOCH FROM (le2.created_at - le1.created_at)) / 60.0, 1) AS minutes_delta FROM banking.ledger_entries le1 JOIN banking.ledger_entries le2 ON le1.account_id = le2.account_id AND le1.id < le2.id AND le1.entry_type = 'DEBIT' AND le2.entry_type = 'DEBIT' AND le2.created_at >= le1.created_at AND le2.created_at <= le1.created_at + INTERVAL '60 minutes' ORDER BY le1.account_id ASC;"),

    ("q145-top-spender-percentile-revenue-contribution", "ecommerce", "Challenge", ["Pareto", "Window Aggregates"],
     "Pareto 80/20 verification: compute running cumulative percentage of total revenue generated by customers ordered by lifetime spend descending. Project customer_id, total_spent, cumulative_pct. Order by total_spent DESC.",
     "Rows: customer_id, total_spent, cumulative_pct",
     "WITH cust_spend AS (SELECT customer_id, SUM(total_amount) AS total_spent FROM ecommerce.orders WHERE status = 'completed' GROUP BY customer_id) SELECT customer_id, total_spent, ROUND((SUM(total_spent) OVER (ORDER BY total_spent DESC, customer_id ASC) / SUM(total_spent) OVER ()) * 100, 2) AS cumulative_pct FROM cust_spend ORDER BY total_spent DESC, customer_id ASC;"),

    ("q146-dense-rank-category-movers", "ecommerce", "Challenge", ["Window", "Rank Shifts"],
     "Calculate product revenue rank shift between January and February 2026. Project product_id, jan_rank, feb_rank, rank_delta. Order by product_id ASC.",
     "Rows: product_id, jan_rank, feb_rank, rank_delta",
     "WITH jan AS (SELECT oi.product_id, DENSE_RANK() OVER (ORDER BY SUM(oi.subtotal) DESC) AS rnk FROM ecommerce.order_items oi JOIN ecommerce.orders o ON oi.order_id = o.id WHERE o.status = 'completed' AND o.order_date >= '2026-01-01' AND o.order_date < '2026-02-01' GROUP BY oi.product_id), feb AS (SELECT oi.product_id, DENSE_RANK() OVER (ORDER BY SUM(oi.subtotal) DESC) AS rnk FROM ecommerce.order_items oi JOIN ecommerce.orders o ON oi.order_id = o.id WHERE o.status = 'completed' AND o.order_date >= '2026-02-01' AND o.order_date < '2026-03-01' GROUP BY oi.product_id) SELECT COALESCE(j.product_id, f.product_id) AS product_id, j.rnk AS jan_rank, f.rnk AS feb_rank, (COALESCE(j.rnk, 99) - COALESCE(f.rnk, 99)) AS rank_delta FROM jan j FULL OUTER JOIN feb f ON j.product_id = f.product_id ORDER BY product_id ASC;"),

    ("q147-recursive-bill-of-materials", "ecommerce", "Challenge", ["Recursive CTE", "BOM"],
     "Calculate total catalog depth and count of leaf subcategories beneath root category 'Electronics' (id = 1). Return total_subcategories, max_depth.",
     "1 row: total_subcategories, max_depth",
     "WITH RECURSIVE cat_tree AS (SELECT id, parent_id, 0 AS depth FROM ecommerce.categories WHERE id = 1 UNION ALL SELECT c.id, c.parent_id, ct.depth + 1 FROM ecommerce.categories c JOIN cat_tree ct ON c.parent_id = ct.id) SELECT COUNT(*) - 1 AS total_subcategories, MAX(depth) AS max_depth FROM cat_tree;"),

    ("q148-keyset-pagination-cursor-query", "ecommerce", "Challenge", ["Pagination", "Keyset Cursor"],
     "Execute a high-performance keyset cursor pagination step: fetch 3 orders after cursor (order_date = '2026-02-05 13:00:00+00', id = 7). Order by order_date ASC, id ASC.",
     "Rows: id, order_date, total_amount",
     "SELECT id, order_date, total_amount FROM ecommerce.orders WHERE (order_date, id) > ('2026-02-05 13:00:00+00'::TIMESTAMPTZ, 7) ORDER BY order_date ASC, id ASC LIMIT 3;"),

    ("q149-safe-conditional-upsert-simulation", "saas", "Challenge", ["DML", "UPSERT Concept"],
     "Simulate an UPSERT query: using standard SQL CTEs, show existing organization record or prepare updated plan_tier = 'enterprise'. Project id, name, plan_tier.",
     "Rows: id, name, plan_tier",
     "SELECT id, name, CASE WHEN id = 3 THEN 'enterprise' ELSE plan_tier END AS plan_tier FROM saas.organizations ORDER BY id ASC;"),

    ("q150-event-latency-percentiles-sla", "saas", "Challenge", ["SLA", "Latency Percentiles"],
     "Calculate p50, p95, and p99 deployment duration in seconds for 'deploy.succeeded' events from JSONB payload. Return p50_sec, p95_sec, p99_sec.",
     "1 row: p50_sec, p95_sec, p99_sec",
     "SELECT PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY (payload->>'duration_sec')::NUMERIC) AS p50_sec, PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY (payload->>'duration_sec')::NUMERIC) AS p95_sec, PERCENTILE_CONT(0.99) WITHIN GROUP (ORDER BY (payload->>'duration_sec')::NUMERIC) AS p99_sec FROM saas.events WHERE event_type = 'deploy.succeeded';"),

    ("q151-three-month-consecutive-spending-increase", "ecommerce", "Challenge", ["Window", "Triple Lag"],
     "Find customers whose spending increased for 2 consecutive calendar months (Jan -> Feb -> Mar 2026). Project customer_id, jan_spend, feb_spend, mar_spend. Order by customer_id ASC.",
     "Rows: customer_id, jan_spend, feb_spend, mar_spend",
     "WITH monthly AS (SELECT customer_id, EXTRACT(MONTH FROM order_date)::INT AS m, SUM(total_amount) AS spend FROM ecommerce.orders WHERE status = 'completed' GROUP BY 1, 2), pivoted AS (SELECT customer_id, COALESCE(SUM(CASE WHEN m = 1 THEN spend END), 0) AS jan_spend, COALESCE(SUM(CASE WHEN m = 2 THEN spend END), 0) AS feb_spend, COALESCE(SUM(CASE WHEN m = 3 THEN spend END), 0) AS mar_spend FROM monthly GROUP BY 1) SELECT customer_id, jan_spend, feb_spend, mar_spend FROM pivoted WHERE feb_spend > jan_spend AND mar_spend > feb_spend ORDER BY customer_id ASC;"),

    ("q152-rfm-customer-segmentation", "ecommerce", "Challenge", ["Analytics", "RFM Segmentation"],
     "Build an RFM (Recency, Frequency, Monetary) segmentation model: calculate Recency (days since last order), Frequency (total completed orders), and Monetary (total spent). Order by monetary DESC.",
     "Rows: customer_id, recency_days, frequency, monetary",
     "SELECT customer_id, ('2026-03-20'::DATE - MAX(order_date)::DATE) AS recency_days, COUNT(*) AS frequency, SUM(total_amount) AS monetary FROM ecommerce.orders WHERE status = 'completed' GROUP BY customer_id ORDER BY monetary DESC, customer_id ASC;"),

    ("q153-social-network-mutual-recommendation", "social", "Challenge", ["Graph", "Recommendations"],
     "Generate follower recommendations for user 2: rank potential users to follow by the number of mutual followers they share with user 2. Project recommended_user_id, mutual_count. Order by mutual_count DESC, recommended_user_id ASC.",
     "Rows: recommended_user_id, mutual_count",
     "WITH my_following AS (SELECT following_id FROM social.follows WHERE follower_id = 2) SELECT f.following_id AS recommended_user_id, COUNT(*) AS mutual_count FROM social.follows f JOIN my_following mf ON f.follower_id = mf.following_id WHERE f.following_id != 2 AND f.following_id NOT IN (SELECT following_id FROM my_following) GROUP BY f.following_id ORDER BY mutual_count DESC, recommended_user_id ASC;"),

    ("q154-banking-audit-tamper-detection", "banking", "Challenge", ["Security", "Integrity Hash"],
     "Audit ledger integrity: calculate running checksum / verification sum of transaction amounts per account. Project account_id, ledger_rows, net_ledger_amount, account_balance, is_reconciled. Order by account_id ASC.",
     "Rows: account_id, ledger_rows, net_ledger_amount, balance, is_reconciled",
     "SELECT a.id AS account_id, COUNT(le.id) AS ledger_rows, COALESCE(SUM(CASE WHEN le.entry_type = 'CREDIT' THEN le.amount ELSE -le.amount END), 0) AS net_ledger_amount, a.balance, (a.balance >= 0) AS is_reconciled FROM banking.accounts a LEFT JOIN banking.ledger_entries le ON a.id = le.account_id GROUP BY a.id, a.balance ORDER BY a.id ASC;"),

    ("q155-saas-activity-burn-rate", "saas", "Challenge", ["SaaS", "Telemetry Velocity"],
     "Calculate daily telemetry event velocity (events per day) per organization. Project organization_id, avg_daily_events. Order by avg_daily_events DESC.",
     "Rows: organization_id, avg_daily_events",
     "WITH daily_events AS (SELECT organization_id, created_at::DATE AS event_day, COUNT(*) AS event_count FROM saas.events GROUP BY 1, 2) SELECT organization_id, ROUND(AVG(event_count), 2) AS avg_daily_events FROM daily_events GROUP BY organization_id ORDER BY avg_daily_events DESC;"),

    ("q156-conversion-time-to-event", "analytics", "Challenge", ["Analytics", "Velocity"],
     "Calculate average time in minutes from user sign_up to their first purchase event. Return avg_minutes_to_purchase rounded to 2 decimals.",
     "1 row: avg_minutes_to_purchase",
     "WITH signups AS (SELECT user_id, MIN(event_timestamp) AS signup_time FROM analytics.events WHERE event_name = 'sign_up' GROUP BY 1), purchases AS (SELECT user_id, MIN(event_timestamp) AS purchase_time FROM analytics.events WHERE event_name = 'purchase' GROUP BY 1) SELECT ROUND(AVG(EXTRACT(EPOCH FROM (p.purchase_time - s.signup_time)) / 60.0), 2) AS avg_minutes_to_purchase FROM signups s JOIN purchases p ON s.user_id = p.user_id;"),

    ("q157-longest-inactivity-gap-per-customer", "ecommerce", "Challenge", ["Window", "Inactivity Gaps"],
     "For customers with multiple orders, find their maximum gap in days between two consecutive orders. Project customer_id, max_gap_days. Order by max_gap_days DESC.",
     "Rows: customer_id, max_gap_days",
     "WITH gaps AS (SELECT customer_id, EXTRACT(EPOCH FROM (order_date - LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date ASC))) / 86400.0 AS gap_days FROM ecommerce.orders) SELECT customer_id, ROUND(MAX(gap_days)::NUMERIC, 1) AS max_gap_days FROM gaps WHERE gap_days IS NOT NULL GROUP BY customer_id ORDER BY max_gap_days DESC, customer_id ASC;"),

    ("q158-category-revenue-concentration-gini", "ecommerce", "Challenge", ["Economics", "Gini / Concentration"],
     "Calculate revenue concentration: proportion of total category revenue coming from the single highest-selling product in that category. Project category_name, max_product_revenue, category_revenue, concentration_pct. Order by concentration_pct DESC.",
     "Rows: category_name, max_product_rev, category_rev, concentration_pct",
     "WITH prod_rev AS (SELECT c.name AS category_name, p.name AS product_name, SUM(oi.subtotal) AS prod_revenue FROM ecommerce.order_items oi JOIN ecommerce.orders o ON oi.order_id = o.id JOIN ecommerce.products p ON oi.product_id = p.id JOIN ecommerce.categories c ON p.category_id = c.id WHERE o.status = 'completed' GROUP BY c.name, p.name), cat_summary AS (SELECT category_name, MAX(prod_revenue) AS max_product_rev, SUM(prod_revenue) AS category_rev FROM prod_rev GROUP BY category_name) SELECT category_name, max_product_rev, category_rev, ROUND((max_product_rev / NULLIF(category_rev, 0)) * 100, 2) AS concentration_pct FROM cat_summary ORDER BY concentration_pct DESC;"),

    ("q159-anti-entropy-reconciliation-job", "banking", "Challenge", ["Audit", "Anti-Entropy"],
     "Reconciliation job: detect any settled transaction where the sum of ledger entries does not match transaction amount. Project transaction_id, txn_amount, ledger_debit_sum, is_balanced.",
     "Rows: transaction_id, amount, ledger_debit_sum, is_balanced",
     "SELECT t.id AS transaction_id, t.amount, SUM(CASE WHEN le.entry_type = 'DEBIT' THEN le.amount ELSE 0 END) AS ledger_debit_sum, (t.amount = SUM(CASE WHEN le.entry_type = 'DEBIT' THEN le.amount ELSE 0 END)) AS is_balanced FROM banking.transactions t JOIN banking.ledger_entries le ON t.id = le.transaction_id WHERE t.status = 'posted' GROUP BY t.id, t.amount ORDER BY t.id ASC;"),

    ("q160-mastery-omnibus-kpi-dashboard", "ecommerce", "Challenge", ["Mastery", "Omnibus Reporting"],
     "Final challenge: produce an executive KPI summary with: total_customers, total_orders, total_gross_revenue, total_refunded, net_revenue, average_order_value, repeat_customer_rate_pct.",
     "1 row: total_customers, total_orders, gross_revenue, total_refunded, net_revenue, aov, repeat_customer_rate_pct",
     "WITH base AS (SELECT (SELECT COUNT(*) FROM ecommerce.customers) AS total_customers, (SELECT COUNT(*) FROM ecommerce.orders WHERE status = 'completed') AS total_orders, (SELECT COALESCE(SUM(total_amount), 0) FROM ecommerce.orders WHERE status = 'completed') AS gross_revenue, (SELECT COALESCE(SUM(amount), 0) FROM ecommerce.refunds) AS total_refunded, (SELECT COUNT(*) FROM (SELECT customer_id FROM ecommerce.orders WHERE status = 'completed' GROUP BY customer_id HAVING COUNT(*) >= 2) rep) AS repeat_customers) SELECT total_customers, total_orders, gross_revenue, total_refunded, (gross_revenue - total_refunded) AS net_revenue, ROUND(gross_revenue / NULLIF(total_orders, 0), 2) AS aov, ROUND((repeat_customers::NUMERIC / NULLIF(total_customers, 0)) * 100, 2) AS repeat_customer_rate_pct FROM base;")
]

for idx, item in enumerate(challenge_defs, start=131):
    EXERCISES.append({
        "tier": "challenge",
        "file": f"q{idx:02d}-{item[0].split('-', 1)[1]}",
        "schema": item[1],
        "diff": item[2],
        "tags": item[3],
        "req": item[4],
        "shape": item[5],
        "sql": item[6]
    })


def main():
    print(f"Total exercises configured: {len(EXERCISES)}")
    for ex in EXERCISES:
        tier_dir = ROOT / "exercises" / ex["tier"]
        sol_dir = ROOT / "solutions" / ex["tier"]
        tier_dir.mkdir(parents=True, exist_ok=True)
        sol_dir.mkdir(parents=True, exist_ok=True)

        ex_file = tier_dir / f"{ex['file']}.md"
        sol_file = sol_dir / f"{ex['file']}.sql"

        tag_str = ", ".join(f"`{t}`" for t in ex["tags"])

        md_content = f"""# Exercise {ex['file'].split('-')[0].upper()}: {ex['file'].replace('-', ' ').title()}

**Tier:** {ex['diff']}  
**Target Schema:** `{ex['schema']}`  
**Concept Tags:** {tag_str}  

---

## 1. Business Requirement

> {ex['req']}

---

## 2. Expected Output Shape

- **Result Grain:** {ex['shape']}

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
python3 scripts/grade-query.py exercises/{ex['tier']}/{ex['file']}.md
```
"""
        ex_file.write_text(md_content, encoding="utf-8")
        sol_file.write_text(ex["sql"] + "\n", encoding="utf-8")

    print(f"[+] All {len(EXERCISES)} exercises and solutions successfully generated!")

if __name__ == "__main__":
    main()
