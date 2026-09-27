-- SQL Analytics Platform: Core BI & Executive Metrics
SET search_path TO ecommerce, analytics, public;

-- 1. Daily Revenue Breakdown (Jan - Mar 2026)
SELECT 
    order_date::DATE AS sales_date,
    COUNT(id) AS orders_count,
    SUM(total_amount) AS daily_revenue,
    ROUND(AVG(total_amount), 2) AS daily_aov
FROM ecommerce.orders
WHERE status = 'completed'
GROUP BY 1
ORDER BY sales_date ASC;

-- 2. Monthly Revenue Run & Active Customer Count
SELECT 
    DATE_TRUNC('month', order_date)::DATE AS sales_month,
    COUNT(DISTINCT customer_id) AS active_customers,
    COUNT(id) AS total_orders,
    SUM(total_amount) AS monthly_revenue
FROM ecommerce.orders
WHERE status = 'completed'
GROUP BY 1
ORDER BY sales_month ASC;

-- 3. Average Order Value (AOV) by Month
SELECT 
    DATE_TRUNC('month', order_date)::DATE AS month,
    ROUND(SUM(total_amount) / COUNT(id), 2) AS monthly_aov
FROM ecommerce.orders
WHERE status = 'completed'
GROUP BY 1
ORDER BY month ASC;

-- 4. Top Products by Total Revenue and Unit Volume
SELECT 
    p.id,
    p.name,
    p.sku,
    SUM(oi.quantity) AS total_units_sold,
    SUM(oi.subtotal) AS gross_revenue
FROM ecommerce.order_items oi
JOIN ecommerce.orders o ON oi.order_id = o.id
JOIN ecommerce.products p ON oi.product_id = p.id
WHERE o.status = 'completed'
GROUP BY p.id, p.name, p.sku
ORDER BY gross_revenue DESC;

-- 5. Top Categories by Completed Revenue
SELECT 
    c.id AS category_id,
    c.name AS category_name,
    SUM(oi.subtotal) AS category_revenue,
    ROUND((SUM(oi.subtotal) / (SELECT SUM(total_amount) FROM ecommerce.orders WHERE status = 'completed')) * 100, 2) AS revenue_share_pct
FROM ecommerce.order_items oi
JOIN ecommerce.orders o ON oi.order_id = o.id
JOIN ecommerce.products p ON oi.product_id = p.id
JOIN ecommerce.categories c ON p.category_id = c.id
WHERE o.status = 'completed'
GROUP BY c.id, c.name
ORDER BY category_revenue DESC;

-- 6. Repeat Customer Identification and Metrics
WITH customer_orders AS (
    SELECT customer_id, COUNT(*) AS order_count, SUM(total_amount) AS total_spend
    FROM ecommerce.orders
    WHERE status = 'completed'
    GROUP BY customer_id
)
SELECT 
    customer_id,
    order_count,
    total_spend,
    CASE WHEN order_count > 1 THEN 'Repeat Buyer' ELSE 'One-Time Buyer' END AS buyer_type
FROM customer_orders
ORDER BY order_count DESC, total_spend DESC;

-- 7. Customer Lifetime Revenue (LTV) Distribution
SELECT 
    c.id AS customer_id,
    c.email,
    COALESCE(SUM(o.total_amount), 0.00) AS lifetime_value,
    DENSE_RANK() OVER (ORDER BY COALESCE(SUM(o.total_amount), 0.00) DESC) AS ltv_rank
FROM ecommerce.customers c
LEFT JOIN ecommerce.orders o ON c.id = o.customer_id AND o.status = 'completed'
GROUP BY c.id, c.email
ORDER BY lifetime_value DESC;

-- 8. Conversion Funnel (Page View -> Sign Up -> View Product -> Add to Cart -> Purchase)
SELECT 
    COUNT(DISTINCT CASE WHEN event_name = 'page_view' THEN user_id END) AS step_1_page_view,
    COUNT(DISTINCT CASE WHEN event_name = 'sign_up' THEN user_id END) AS step_2_sign_up,
    COUNT(DISTINCT CASE WHEN event_name = 'view_product' THEN user_id END) AS step_3_view_product,
    COUNT(DISTINCT CASE WHEN event_name = 'add_to_cart' THEN user_id END) AS step_4_add_to_cart,
    COUNT(DISTINCT CASE WHEN event_name = 'purchase' THEN user_id END) AS step_5_purchase
FROM analytics.events;

-- 9. Monthly Cohort Retention Matrix
WITH user_activity AS (
    SELECT DISTINCT 
        uc.user_id,
        uc.cohort_month,
        DATE_TRUNC('month', e.event_timestamp)::DATE AS activity_month
    FROM analytics.user_cohorts uc
    JOIN analytics.events e ON uc.user_id = e.user_id
)
SELECT 
    uc.cohort_month,
    COUNT(DISTINCT uc.user_id) AS cohort_size,
    COUNT(DISTINCT CASE WHEN ua.activity_month = uc.cohort_month THEN ua.user_id END) AS month_0_active,
    COUNT(DISTINCT CASE WHEN ua.activity_month = uc.cohort_month + INTERVAL '1 month' THEN ua.user_id END) AS month_1_active
FROM analytics.user_cohorts uc
LEFT JOIN user_activity ua ON uc.user_id = ua.user_id AND uc.cohort_month = ua.cohort_month
GROUP BY uc.cohort_month
ORDER BY uc.cohort_month ASC;

-- 10. Rolling 7-Day Revenue
WITH daily AS (
    SELECT order_date::DATE AS day, SUM(total_amount) AS revenue
    FROM ecommerce.orders
    WHERE status = 'completed'
    GROUP BY 1
)
SELECT 
    day,
    revenue AS daily_rev,
    ROUND(SUM(revenue) OVER (ORDER BY day ASC ROWS BETWEEN 6 PRECEDING AND CURRENT ROW), 2) AS rolling_7d_revenue
FROM daily
ORDER BY day ASC;

-- 11. Month-over-Month (MoM) Growth Percentage
WITH monthly AS (
    SELECT 
        DATE_TRUNC('month', order_date)::DATE AS sales_month,
        SUM(total_amount) AS revenue
    FROM ecommerce.orders
    WHERE status = 'completed'
    GROUP BY 1
)
SELECT 
    sales_month,
    revenue,
    LAG(revenue) OVER (ORDER BY sales_month ASC) AS prev_month_revenue,
    ROUND(((revenue - LAG(revenue) OVER (ORDER BY sales_month ASC)) / 
           NULLIF(LAG(revenue) OVER (ORDER BY sales_month ASC), 0)) * 100, 2) AS mom_growth_pct
FROM monthly
ORDER BY sales_month ASC;
