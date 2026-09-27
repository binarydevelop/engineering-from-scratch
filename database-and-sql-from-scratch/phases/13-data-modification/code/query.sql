INSERT INTO ecommerce.customers (email, first_name, last_name) VALUES ('new@ex.com', 'New', 'User') RETURNING id, created_at;
