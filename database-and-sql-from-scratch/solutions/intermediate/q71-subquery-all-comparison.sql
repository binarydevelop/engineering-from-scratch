SELECT name, price FROM ecommerce.products WHERE price > ALL (SELECT price FROM ecommerce.products WHERE category_id = 3) ORDER BY price ASC, name ASC;
