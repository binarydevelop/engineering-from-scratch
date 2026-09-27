SELECT name, price FROM ecommerce.products WHERE price > (SELECT price FROM ecommerce.products WHERE name = 'Precision Coffee Grinder') ORDER BY price DESC, name ASC;
