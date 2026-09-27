SELECT
    c.name AS subcategory_name,
    p.name AS parent_category_name
FROM ecommerce.categories c
JOIN ecommerce.categories p ON c.parent_id = p.id
ORDER BY c.name ASC;
