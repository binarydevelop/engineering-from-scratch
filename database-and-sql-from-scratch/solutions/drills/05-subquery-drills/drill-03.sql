SELECT
    c.id,
    c.email
FROM ecommerce.customers c
WHERE EXISTS (
    SELECT 1
    FROM ecommerce.orders o
    WHERE o.customer_id = c.id
      AND o.status = 'completed'
)
ORDER BY c.id ASC;
