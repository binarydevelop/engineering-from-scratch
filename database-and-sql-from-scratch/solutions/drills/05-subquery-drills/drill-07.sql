WITH RECURSIVE cat_tree AS (
    SELECT
        id,
        name,
        parent_id,
        name::TEXT AS path
    FROM ecommerce.categories
    WHERE parent_id IS NULL
    UNION ALL
    SELECT
        c.id,
        c.name,
        c.parent_id,
        (ct.path || ' > ' || c.name)::TEXT AS path
    FROM ecommerce.categories c
    JOIN cat_tree ct ON c.parent_id = ct.id
)
SELECT
    id,
    path
FROM cat_tree
ORDER BY id ASC;
