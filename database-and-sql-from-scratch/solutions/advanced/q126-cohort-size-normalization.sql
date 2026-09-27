SELECT cohort_month, COUNT(*) AS total_users FROM analytics.user_cohorts GROUP BY cohort_month ORDER BY cohort_month ASC;
