SELECT
    o.id,
    o.name
FROM saas.organizations o
WHERE NOT EXISTS (
    SELECT 1
    FROM saas.events e
    WHERE e.organization_id = o.id
      AND e.created_at >= '2026-03-01 00:00:00+00'
      AND e.created_at < '2026-04-01 00:00:00+00'
)
ORDER BY o.id ASC;
