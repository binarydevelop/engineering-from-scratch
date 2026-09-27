SELECT
    customer_id,
    COUNT(*) AS total_orders,
    COUNT(*) FILTER (WHERE status = 'completed') AS completed_orders,
    COUNT(*) FILTER (WHERE status = 'refunded') AS refunded_orders
FROM ecommerce.orders
GROUP BY customer_id
ORDER BY customer_id ASC;
