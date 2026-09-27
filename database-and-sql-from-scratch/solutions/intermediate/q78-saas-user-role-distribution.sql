SELECT role, COUNT(*) AS user_count FROM saas.memberships GROUP BY role ORDER BY role ASC;
