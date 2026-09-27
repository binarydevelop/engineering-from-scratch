SELECT
    c.id,
    c.first_name,
    c.last_name,
    c.email
FROM ecommerce.customers c
WHERE NOT EXISTS (
    SELECT 1
    FROM ecommerce.orders o
    WHERE o.customer_id = c.id
)
ORDER BY c.id ASC;
