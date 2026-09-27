SELECT
    o.name AS org_name,
    COUNT(m.user_id) AS used_seats,
    s.seats_purchased
FROM saas.organizations o
JOIN saas.subscriptions s ON o.id = s.organization_id
LEFT JOIN saas.memberships m ON o.id = m.organization_id
GROUP BY o.id, o.name, s.seats_purchased
ORDER BY org_name ASC;
