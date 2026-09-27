SELECT
    c.id AS customer_id,
    c.email,
    o.id AS order_id
FROM ecommerce.customers c
LEFT JOIN ecommerce.orders o ON c.id = o.customer_id
ORDER BY c.id ASC, o.id ASC NULLS LAST;
