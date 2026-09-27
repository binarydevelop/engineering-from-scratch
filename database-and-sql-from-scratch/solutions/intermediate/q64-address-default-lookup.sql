SELECT c.email, COALESCE(a.city, 'No Default') AS city FROM ecommerce.customers c LEFT JOIN ecommerce.addresses a ON c.id = a.customer_id AND a.is_default = TRUE ORDER BY c.email ASC;
