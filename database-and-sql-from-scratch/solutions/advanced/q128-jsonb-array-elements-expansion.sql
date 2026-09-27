SELECT id, payload FROM saas.events WHERE payload ? 'version' ORDER BY id ASC;
