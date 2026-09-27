SELECT
    customer_id,
    MAX(order_date)::DATE AS latest_order_date,
    ('2026-03-20'::DATE - MAX(order_date)::DATE) AS days_since_last_order
FROM ecommerce.orders
GROUP BY customer_id
ORDER BY days_since_last_order ASC, customer_id ASC;
