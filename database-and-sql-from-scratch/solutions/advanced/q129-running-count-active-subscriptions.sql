SELECT status, COUNT(*) AS sub_count, SUM(monthly_price) AS total_mrr FROM saas.subscriptions GROUP BY status ORDER BY status ASC;
