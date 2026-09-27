SELECT email, COUNT(*) AS occurrence_count FROM ecommerce.customers GROUP BY email HAVING COUNT(*) > 1;
