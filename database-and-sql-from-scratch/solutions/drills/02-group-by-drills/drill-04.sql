SELECT
    customer_id,
    COUNT(CASE WHEN status = 'completed' THEN 1 END) AS completed_orders,
    COUNT(CASE WHEN status IN ('cancelled', 'refunded') THEN 1 END) AS bad_orders
FROM ecommerce.orders
GROUP BY customer_id
ORDER BY customer_id ASC;
