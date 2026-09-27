SELECT id, name, parent_id FROM ecommerce.categories WHERE parent_id IS NOT DISTINCT FROM NULL ORDER BY id ASC;
