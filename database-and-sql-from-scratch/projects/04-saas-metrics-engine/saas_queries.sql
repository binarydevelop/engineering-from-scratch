-- SaaS Multi-Tenant Analytics Queries
SET search_path TO saas, public;

-- 1. Total MRR and Active Subscription Counts
SELECT 
    COUNT(*) AS total_active_subscriptions,
    SUM(monthly_price) AS total_mrr,
    ROUND(AVG(monthly_price), 2) AS arpo,
    SUM(seats_purchased) AS total_licensed_seats
FROM subscriptions
WHERE status = 'active';

-- 2. MRR Breakdown by Subscription Plan Tier
SELECT 
    o.plan_tier,
    COUNT(s.id) AS active_subscriptions,
    SUM(s.monthly_price) AS tier_mrr,
    ROUND((SUM(s.monthly_price) / (SELECT SUM(monthly_price) FROM subscriptions WHERE status = 'active')) * 100, 2) AS mrr_pct
FROM organizations o
JOIN subscriptions s ON o.id = s.organization_id
WHERE s.status = 'active'
GROUP BY o.plan_tier
ORDER BY tier_mrr DESC;

-- 3. Seat Utilization per Organization
SELECT 
    o.name AS org_name,
    o.plan_tier,
    s.seats_purchased,
    COUNT(m.user_id) AS seats_occupied,
    ROUND((COUNT(m.user_id)::NUMERIC / NULLIF(s.seats_purchased, 0)) * 100, 2) AS seat_utilization_pct
FROM organizations o
JOIN subscriptions s ON o.id = s.organization_id
LEFT JOIN memberships m ON o.id = m.organization_id
GROUP BY o.id, o.name, o.plan_tier, s.seats_purchased
ORDER BY seat_utilization_pct DESC;

-- 4. Churn Risk: Active Subscriptions with Zero Events in Last 30 Days
SELECT 
    o.id AS org_id,
    o.name AS org_name,
    s.monthly_price AS at_risk_mrr,
    s.status AS subscription_status
FROM organizations o
JOIN subscriptions s ON o.id = s.organization_id
WHERE s.status IN ('active', 'past_due')
  AND NOT EXISTS (
      SELECT 1 
      FROM events e 
      WHERE e.organization_id = o.id 
        AND e.created_at >= NOW() - INTERVAL '30 days'
  )
ORDER BY at_risk_mrr DESC;

-- 5. JSONB Feature Adoption: Deployment Success Rate
SELECT 
    COUNT(*) FILTER (WHERE event_type = 'deploy.succeeded') AS successful_deploys,
    COUNT(*) FILTER (WHERE event_type = 'deploy.started') AS started_deploys,
    ROUND(AVG((payload->>'duration_sec')::NUMERIC) FILTER (WHERE event_type = 'deploy.succeeded'), 2) AS avg_deploy_duration_sec
FROM events
WHERE event_type LIKE 'deploy.%';
