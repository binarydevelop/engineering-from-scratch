SELECT
    o.id AS order_id,
    c.email,
    o.total_amount
FROM ecommerce.orders o
JOIN ecommerce.customers c ON o.customer_id = c.id
WHERE o.status = 'completed'
ORDER BY o.id ASC;
