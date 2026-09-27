SELECT
    name,
    price
FROM ecommerce.products
WHERE price > (SELECT AVG(price) FROM ecommerce.products)
ORDER BY price DESC;
