SELECT p.id, p.name FROM saas.projects p JOIN saas.memberships m ON p.organization_id = m.organization_id WHERE m.user_id = 1 AND p.organization_id = 1 ORDER BY p.id ASC;
