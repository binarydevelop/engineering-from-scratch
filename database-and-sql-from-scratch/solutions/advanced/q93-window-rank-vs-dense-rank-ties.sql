SELECT name, price, RANK() OVER (ORDER BY price DESC) AS rnk, DENSE_RANK() OVER (ORDER BY price DESC) AS dense_rnk FROM ecommerce.products WHERE category_id = 2 ORDER BY price DESC, name ASC;
