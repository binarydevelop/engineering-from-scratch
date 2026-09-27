SELECT email, status, CASE status WHEN 'active' THEN 'Verified User' WHEN 'suspended' THEN 'Action Required' ELSE 'Unknown' END AS status_label FROM ecommerce.customers ORDER BY id ASC;
