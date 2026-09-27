-- transformations/marts/mart_daily_revenue.sql
-- Grain: One row per day. Aggregates financial performance, total orders, completed vs cancelled.

WITH orders AS (
    SELECT
        CAST(created_at AS DATE) AS order_date,
        order_status,
        CAST(total_amount AS NUMERIC(10,2)) AS total_amount
    FROM read_csv_auto('datasets/raw/orders.csv')
)
SELECT
    order_date,
    COUNT(*) AS total_orders_placed,
    COUNT(CASE WHEN order_status = 'COMPLETED' THEN 1 END) AS completed_orders,
    COUNT(CASE WHEN order_status = 'CANCELLED' THEN 1 END) AS cancelled_orders,
    SUM(CASE WHEN order_status = 'COMPLETED' THEN total_amount ELSE 0 END) AS net_revenue,
    AVG(CASE WHEN order_status = 'COMPLETED' THEN total_amount END) AS average_order_value
FROM orders
GROUP BY order_date
ORDER BY order_date ASC;
