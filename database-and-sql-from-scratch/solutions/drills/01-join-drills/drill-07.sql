SELECT
    c.name AS category_name,
    s.status
FROM ecommerce.categories c
CROSS JOIN (VALUES ('active'), ('inactive')) AS s(status)
WHERE c.parent_id IS NULL
ORDER BY category_name ASC, status ASC;
