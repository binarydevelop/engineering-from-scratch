SELECT id, email, COALESCE(bio, 'N/A') FROM social.users WHERE bio IS NULL;
