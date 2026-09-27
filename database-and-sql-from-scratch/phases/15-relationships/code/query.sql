SELECT o.id, c.email FROM ecommerce.orders o JOIN ecommerce.customers c ON o.customer_id = c.id ORDER BY o.id ASC;
