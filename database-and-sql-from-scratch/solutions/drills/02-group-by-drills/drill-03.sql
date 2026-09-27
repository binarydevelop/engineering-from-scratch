SELECT
    customer_id,
    COUNT(*) AS order_count
FROM ecommerce.orders
WHERE status = 'completed'
GROUP BY customer_id
HAVING COUNT(*) >= 2
ORDER BY order_count DESC, customer_id ASC;
