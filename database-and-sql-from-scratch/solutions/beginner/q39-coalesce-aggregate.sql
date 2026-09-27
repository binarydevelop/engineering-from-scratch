SELECT COALESCE(SUM(amount), 0.00) AS total_refunded FROM ecommerce.refunds;
