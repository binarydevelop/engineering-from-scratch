-- transformations/marts/mart_customer_lifetime_value.sql
-- Grain: One row per customer. Aggregates historical spend, frequency, and recency.

WITH users AS (
    SELECT user_id, email, full_name, customer_tier
    FROM (
        SELECT user_id, email, full_name, UPPER(tier) AS customer_tier
        FROM read_csv_auto('datasets/raw/users.csv')
    )
),
completed_orders AS (
    SELECT
        user_id,
        CAST(total_amount AS NUMERIC(10,2)) AS amount,
        CAST(created_at AS TIMESTAMP) AS ordered_at
    FROM read_csv_auto('datasets/raw/orders.csv')
    WHERE order_status = 'COMPLETED'
),
customer_aggregates AS (
    SELECT
        user_id,
        COUNT(*) AS total_completed_orders,
        SUM(amount) AS lifetime_revenue,
        AVG(amount) AS average_order_value,
        MIN(ordered_at) AS first_order_timestamp,
        MAX(ordered_at) AS last_order_timestamp
    FROM completed_orders
    GROUP BY user_id
)
SELECT
    u.user_id,
    u.full_name,
    u.email,
    u.customer_tier,
    COALESCE(ca.total_completed_orders, 0) AS total_orders,
    COALESCE(ca.lifetime_revenue, 0.0) AS lifetime_value,
    COALESCE(ca.average_order_value, 0.0) AS avg_order_value,
    ca.first_order_timestamp,
    ca.last_order_timestamp
FROM users u
LEFT JOIN customer_aggregates ca ON u.user_id = ca.user_id
ORDER BY lifetime_value DESC;
