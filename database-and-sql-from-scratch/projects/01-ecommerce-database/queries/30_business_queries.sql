-- 30 Production Business Queries for E-Commerce Platform
SET search_path TO ecommerce, public;

-- 1. All active products with category name and stock
SELECT p.id, p.name, c.name AS category_name, p.price, i.stock_quantity
FROM products p
JOIN categories c ON p.category_id = c.id
JOIN inventory i ON p.id = i.product_id
WHERE p.is_active = TRUE
ORDER BY p.id ASC;

-- 2. Low-stock alert: products at or below reorder level
SELECT p.sku, p.name, i.stock_quantity, i.reorder_level
FROM products p
JOIN inventory i ON p.id = i.product_id
WHERE i.stock_quantity <= i.reorder_level
ORDER BY i.stock_quantity ASC;

-- 3. Total gross revenue from completed orders
SELECT SUM(total_amount) AS total_gross_revenue
FROM orders
WHERE status = 'completed';

-- 4. Net revenue (gross completed revenue minus total refunded amount)
SELECT 
    (SELECT COALESCE(SUM(total_amount), 0) FROM orders WHERE status = 'completed') -
    (SELECT COALESCE(SUM(amount), 0) FROM refunds) AS net_revenue;

-- 5. Average Order Value (AOV)
SELECT ROUND(AVG(total_amount), 2) AS average_order_value
FROM orders
WHERE status = 'completed';

-- 6. Top 5 highest spending customers
SELECT c.id, c.email, c.first_name, c.last_name, SUM(o.total_amount) AS lifetime_spend
FROM customers c
JOIN orders o ON c.id = o.customer_id
WHERE o.status = 'completed'
GROUP BY c.id, c.email, c.first_name, c.last_name
ORDER BY lifetime_spend DESC
LIMIT 5;

-- 7. Customers who have never placed an order (Lurkers)
SELECT c.id, c.email, c.created_at
FROM customers c
WHERE NOT EXISTS (
    SELECT 1 FROM orders o WHERE o.customer_id = c.id
)
ORDER BY c.id ASC;

-- 8. Monthly completed sales trend
SELECT 
    DATE_TRUNC('month', order_date)::DATE AS sales_month,
    COUNT(*) AS total_orders,
    SUM(total_amount) AS revenue
FROM orders
WHERE status = 'completed'
GROUP BY 1
ORDER BY sales_month ASC;

-- 9. Revenue by top-level product category
SELECT 
    COALESCE(parent.name, child.name) AS main_category,
    SUM(oi.subtotal) AS category_revenue
FROM order_items oi
JOIN orders o ON oi.order_id = o.id
JOIN products p ON oi.product_id = p.id
JOIN categories child ON p.category_id = child.id
LEFT JOIN categories parent ON child.parent_id = parent.id
WHERE o.status = 'completed'
GROUP BY 1
ORDER BY category_revenue DESC;

-- 10. Most frequently purchased products by quantity sold
SELECT p.id, p.name, p.sku, SUM(oi.quantity) AS total_units_sold
FROM order_items oi
JOIN orders o ON oi.order_id = o.id
JOIN products p ON oi.product_id = p.id
WHERE o.status = 'completed'
GROUP BY p.id, p.name, p.sku
ORDER BY total_units_sold DESC;

-- 11. Products that have never been ordered
SELECT p.id, p.sku, p.name, p.price
FROM products p
WHERE NOT EXISTS (
    SELECT 1 FROM order_items oi WHERE oi.product_id = p.id
)
ORDER BY p.id ASC;

-- 12. Payment method breakdown by volume and value
SELECT 
    payment_method,
    COUNT(*) AS transaction_count,
    SUM(amount) AS total_processed,
    ROUND(AVG(amount), 2) AS avg_transaction_size
FROM payments
WHERE status = 'completed'
GROUP BY payment_method
ORDER BY total_processed DESC;

-- 13. Refund rate percentage
SELECT 
    ROUND((COUNT(DISTINCT r.order_id)::NUMERIC / NULLIF(COUNT(DISTINCT o.id), 0)) * 100, 2) AS refund_order_rate_pct
FROM orders o
LEFT JOIN refunds r ON o.id = r.order_id
WHERE o.status IN ('completed', 'refunded');

-- 14. Top 3 products by revenue within each category (Window Function)
WITH ranked AS (
    SELECT 
        c.name AS category_name,
        p.name AS product_name,
        SUM(oi.subtotal) AS product_revenue,
        DENSE_RANK() OVER (PARTITION BY c.id ORDER BY SUM(oi.subtotal) DESC) AS rnk
    FROM order_items oi
    JOIN orders o ON oi.order_id = o.id
    JOIN products p ON oi.product_id = p.id
    JOIN categories c ON p.category_id = c.id
    WHERE o.status = 'completed'
    GROUP BY c.id, c.name, p.id, p.name
)
SELECT category_name, product_name, product_revenue, rnk AS rank
FROM ranked
WHERE rnk <= 3
ORDER BY category_name ASC, rank ASC;

-- 15. Repeat purchase rate (customers with >= 2 orders / total customers)
WITH customer_order_counts AS (
    SELECT customer_id, COUNT(*) AS orders_placed
    FROM orders
    WHERE status = 'completed'
    GROUP BY customer_id
)
SELECT 
    COUNT(*) FILTER (WHERE orders_placed >= 2) AS repeat_buyers,
    COUNT(*) AS total_buyers,
    ROUND((COUNT(*) FILTER (WHERE orders_placed >= 2)::NUMERIC / NULLIF(COUNT(*), 0)) * 100, 2) AS repeat_buyer_pct
FROM customer_order_counts;

-- 16. Running cumulative revenue across orders
SELECT 
    id AS order_id,
    order_date,
    total_amount,
    SUM(total_amount) OVER (ORDER BY order_date ASC, id ASC) AS cumulative_revenue
FROM orders
WHERE status = 'completed'
ORDER BY order_date ASC;

-- 17. Month-over-Month revenue growth percentage
WITH monthly_rev AS (
    SELECT 
        DATE_TRUNC('month', order_date)::DATE AS sales_month,
        SUM(total_amount) AS revenue
    FROM orders
    WHERE status = 'completed'
    GROUP BY 1
)
SELECT 
    sales_month,
    revenue,
    LAG(revenue) OVER (ORDER BY sales_month ASC) AS previous_month_revenue,
    ROUND(((revenue - LAG(revenue) OVER (ORDER BY sales_month ASC)) / NULLIF(LAG(revenue) OVER (ORDER BY sales_month ASC), 0)) * 100, 2) AS mom_growth_pct
FROM monthly_rev
ORDER BY sales_month ASC;

-- 18. Customer geographic distribution by shipping state
SELECT 
    a.state,
    COUNT(DISTINCT c.id) AS customer_count,
    COUNT(o.id) AS total_orders,
    SUM(o.total_amount) AS state_revenue
FROM customers c
JOIN addresses a ON c.id = a.customer_id AND a.is_default = TRUE
LEFT JOIN orders o ON c.id = o.customer_id AND o.status = 'completed'
GROUP BY a.state
ORDER BY state_revenue DESC NULLS LAST;

-- 19. Average number of items per order
SELECT 
    ROUND(AVG(item_count), 2) AS avg_distinct_items_per_order,
    ROUND(AVG(total_units), 2) AS avg_units_per_order
FROM (
    SELECT order_id, COUNT(product_id) AS item_count, SUM(quantity) AS total_units
    FROM order_items
    GROUP BY order_id
) s;

-- 20. Orders with discount or price discrepancies
SELECT oi.order_id, oi.product_id, p.price AS catalog_price, oi.unit_price AS actual_paid_price
FROM order_items oi
JOIN products p ON oi.product_id = p.id
WHERE oi.unit_price != p.price;

-- 21. Customers with suspended accounts holding completed orders
SELECT c.id, c.email, c.status, COUNT(o.id) AS completed_orders
FROM customers c
JOIN orders o ON c.id = o.customer_id
WHERE c.status = 'suspended' AND o.status = 'completed'
GROUP BY c.id, c.email, c.status;

-- 22. Category hierarchy breadcrumb paths (Recursive CTE)
WITH RECURSIVE category_paths AS (
    SELECT id, name, parent_id, name::TEXT AS breadcrumb
    FROM categories
    WHERE parent_id IS NULL
    UNION ALL
    SELECT c.id, c.name, c.parent_id, (cp.breadcrumb || ' -> ' || c.name)::TEXT
    FROM categories c
    JOIN category_paths cp ON c.parent_id = cp.id
)
SELECT id, breadcrumb
FROM category_paths
ORDER BY breadcrumb ASC;

-- 23. Largest single orders by monetary value
SELECT o.id, c.email, o.total_amount, o.order_date
FROM orders o
JOIN customers c ON o.customer_id = c.id
WHERE o.status = 'completed'
ORDER BY o.total_amount DESC
LIMIT 3;

-- 24. Average fulfillment delay (order date to payment settled)
SELECT 
    ROUND(AVG(EXTRACT(EPOCH FROM (p.created_at - o.order_date)) / 60.0), 2) AS avg_payment_delay_minutes
FROM orders o
JOIN payments p ON o.id = p.order_id
WHERE p.status = 'completed';

-- 25. Products with highest profit margins (markup percentage)
SELECT sku, name, price, cost, (price - cost) AS unit_margin, ROUND(((price - cost) / cost) * 100, 2) AS margin_pct
FROM products
WHERE is_active = TRUE
ORDER BY margin_pct DESC
LIMIT 5;

-- 26. Daily order count and revenue for February 2026
SELECT 
    order_date::DATE AS day,
    COUNT(*) AS order_count,
    SUM(total_amount) AS daily_revenue
FROM orders
WHERE status = 'completed'
  AND order_date >= '2026-02-01' AND order_date < '2026-03-01'
GROUP BY 1
ORDER BY day ASC;

-- 27. Cross-sold products (frequently bought together with Product 1)
SELECT oi2.product_id, p.name AS cross_sold_product, COUNT(*) AS times_bought_together
FROM order_items oi1
JOIN order_items oi2 ON oi1.order_id = oi2.order_id AND oi1.product_id != oi2.product_id
JOIN products p ON oi2.product_id = p.id
WHERE oi1.product_id = 1
GROUP BY oi2.product_id, p.name
ORDER BY times_bought_together DESC;

-- 28. Status breakdown counts as columns (Pivot)
SELECT 
    COUNT(*) FILTER (WHERE status = 'completed') AS completed,
    COUNT(*) FILTER (WHERE status = 'refunded') AS refunded,
    COUNT(*) FILTER (WHERE status = 'cancelled') AS cancelled,
    COUNT(*) FILTER (WHERE status = 'pending') AS pending
FROM orders;

-- 29. Customers whose total lifetime spend exceeds the 90th percentile
WITH customer_spending AS (
    SELECT customer_id, SUM(total_amount) AS lifetime_spend
    FROM orders
    WHERE status = 'completed'
    GROUP BY customer_id
),
threshold AS (
    SELECT PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY lifetime_spend) AS p90_cutoff
    FROM customer_spending
)
SELECT cs.customer_id, cs.lifetime_spend, t.p90_cutoff
FROM customer_spending cs
CROSS JOIN threshold t
WHERE cs.lifetime_spend >= t.p90_cutoff
ORDER BY cs.lifetime_spend DESC;

-- 30. Executive e-commerce KPI summary card
SELECT 
    (SELECT COUNT(*) FROM customers WHERE status = 'active') AS active_customers,
    (SELECT COUNT(*) FROM products WHERE is_active = TRUE) AS active_skus,
    (SELECT COUNT(*) FROM orders WHERE status = 'completed') AS total_completed_orders,
    (SELECT COALESCE(SUM(total_amount), 0) FROM orders WHERE status = 'completed') AS gross_merchandise_value,
    (SELECT COALESCE(SUM(amount), 0) FROM refunds) AS refunded_value,
    ROUND((SELECT COALESCE(SUM(total_amount), 0) FROM orders WHERE status = 'completed') / 
          NULLIF((SELECT COUNT(*) FROM orders WHERE status = 'completed'), 0), 2) AS average_order_value;
