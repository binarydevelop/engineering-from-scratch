SELECT
    name,
    price,
    NTILE(4) OVER (ORDER BY price ASC) AS quartile
FROM ecommerce.products
ORDER BY price ASC, name ASC;
