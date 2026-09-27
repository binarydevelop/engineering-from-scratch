SELECT username, COALESCE(bio, 'No bio provided.') AS display_bio FROM social.users ORDER BY id ASC;
