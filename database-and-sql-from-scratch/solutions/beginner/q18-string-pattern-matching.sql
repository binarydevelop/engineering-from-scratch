SELECT id, first_name, email FROM ecommerce.customers WHERE email LIKE '%@example.com' AND (first_name LIKE 'A%' OR first_name LIKE 'B%') ORDER BY id ASC;
