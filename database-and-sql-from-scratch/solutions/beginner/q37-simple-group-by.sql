SELECT status, COUNT(*) AS count FROM ecommerce.orders GROUP BY status ORDER BY count DESC, status ASC;
