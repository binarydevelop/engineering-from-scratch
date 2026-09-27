SELECT id, name, CASE WHEN id = 3 THEN 'enterprise' ELSE plan_tier END AS plan_tier FROM saas.organizations ORDER BY id ASC;
