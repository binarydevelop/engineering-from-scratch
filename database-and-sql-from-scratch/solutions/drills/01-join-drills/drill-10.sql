SELECT
    c.id AS customer_id,
    c.email,
    a.id AS address_id
FROM (SELECT * FROM ecommerce.customers WHERE id IN (14, 15)) c
FULL OUTER JOIN ecommerce.addresses a ON c.id = a.customer_id
ORDER BY customer_id ASC NULLS LAST, address_id ASC NULLS LAST;
