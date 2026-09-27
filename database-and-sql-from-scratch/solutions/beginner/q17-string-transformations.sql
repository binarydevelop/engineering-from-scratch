SELECT id, UPPER(full_name) AS upper_name, LOWER(username) AS lower_username, COALESCE(LENGTH(bio), 0) AS bio_len FROM social.users ORDER BY id ASC;
