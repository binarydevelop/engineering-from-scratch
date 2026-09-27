SELECT p.id, p.name AS product_name, c.name AS category_name, p.price FROM ecommerce.products p JOIN ecommerce.categories c ON p.category_id = c.id ORDER BY p.id ASC;
