SELECT
    c.email,
    COUNT(o.id) AS completed_order_count
FROM ecommerce.customers c
LEFT JOIN ecommerce.orders o
    ON c.id = o.customer_id
    AND o.status = 'completed'
GROUP BY c.id, c.email
ORDER BY completed_order_count DESC, c.email ASC;
