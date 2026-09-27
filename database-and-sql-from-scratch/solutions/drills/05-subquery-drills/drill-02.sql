SELECT
    p1.category_id,
    p1.name,
    p1.price
FROM ecommerce.products p1
WHERE p1.price > (
    SELECT AVG(p2.price)
    FROM ecommerce.products p2
    WHERE p2.category_id = p1.category_id
)
ORDER BY p1.category_id ASC, p1.price DESC;
