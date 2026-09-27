SELECT p.name, c.slug, 'support@' || c.slug || '.com' AS support_email FROM ecommerce.products p JOIN ecommerce.categories c ON p.category_id = c.id ORDER BY p.name ASC;
