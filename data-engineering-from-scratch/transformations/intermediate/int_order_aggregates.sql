-- transformations/intermediate/int_order_aggregates.sql
-- Joins staging orders with staging line items to aggregate metrics per order

WITH orders AS (
    SELECT * FROM read_csv_auto('datasets/raw/orders.csv')
),
items AS (
    SELECT * FROM read_csv_auto('datasets/raw/order_items.csv')
),
item_rollups AS (
    SELECT
        order_id,
        COUNT(item_id) AS total_items_count,
        SUM(quantity) AS total_units_sold,
        SUM(line_total) AS items_gross_value
    FROM items
    GROUP BY order_id
)
SELECT
    o.order_id,
    o.user_id,
    o.order_status,
    CAST(o.total_amount AS NUMERIC(10,2)) AS total_amount,
    COALESCE(r.total_items_count, 0) AS total_items_count,
    COALESCE(r.total_units_sold, 0) AS total_units_sold,
    COALESCE(r.items_gross_value, 0.0) AS items_gross_value,
    CAST(o.created_at AS TIMESTAMP) AS created_at
FROM orders o
LEFT JOIN item_rollups r ON o.order_id = r.order_id;
