SELECT name, price FROM ecommerce.products WHERE price = ANY (SELECT price FROM ecommerce.products WHERE category_id = 8) ORDER BY price ASC, name ASC;
