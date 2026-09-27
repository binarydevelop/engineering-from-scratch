SELECT id, category_id, name FROM ecommerce.products WHERE category_id NOT IN (2, 3) ORDER BY id ASC;
