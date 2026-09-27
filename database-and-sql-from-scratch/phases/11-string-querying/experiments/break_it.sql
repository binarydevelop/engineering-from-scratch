SELECT * FROM ecommerce.products WHERE LOWER(name) LIKE '%phone%'; -- Invalidates standard B-Tree on name
