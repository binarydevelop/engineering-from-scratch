SELECT id, parent_id, name FROM ecommerce.categories WHERE parent_id IS NOT NULL ORDER BY parent_id ASC, id ASC;
