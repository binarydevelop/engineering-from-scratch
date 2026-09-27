# Clickstream & Event Analytics Dataset

Event-driven analytics telemetry modeling marketing acquisition campaigns, visitor sessions, conversion funnel progressions, and monthly cohort retention.

## Entity-Relationship Diagram

```text
  [campaigns] 1 ──── N [sessions] 1 ──── N [events]
                           │
       [user_cohorts] ◄────┘ (user_id linkage)
```

## Key Query Capabilities
- **Conversion Funnels:** Tracking step conversion drop-off percentages from `page_view` -> `sign_up` -> `view_product` -> `add_to_cart` -> `begin_checkout` -> `purchase`.
- **Cohort Retention:** Monthly matrix tracing user activity in Month 0 vs Month 1.
- **Gaps & Islands:** Identifying streaks of consecutive active days per user (e.g. user 101 active Jan 10-14 = 5 consecutive days).
- **Session Duration:** Computing time spent per session and average events per session.
