SELECT c.id, c.email, COUNT(o.id) AS order_count FROM ecommerce.customers c LEFT JOIN ecommerce.orders o ON c.id = o.customer_id GROUP BY c.id, c.email ORDER BY order_count DESC, c.id ASC;
