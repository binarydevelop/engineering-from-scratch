SELECT c.id, c.email FROM ecommerce.customers c LEFT JOIN ecommerce.orders o ON c.id = o.customer_id WHERE o.id IS NULL ORDER BY c.id ASC;
