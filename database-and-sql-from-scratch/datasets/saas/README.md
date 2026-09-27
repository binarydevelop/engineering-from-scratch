# SaaS Multi-Tenant Dataset

A B2B multi-tenant schema modeling enterprise accounts, user role memberships, subscriptions, and high-frequency JSONB telemetry events.

## Entity-Relationship Diagram

```text
  [organizations] 1 ──── 1 [subscriptions]
         │
         ├── 1 ── N [memberships] N ── 1 [users]
         │
         ├── 1 ── N [projects]
         │
         └── 1 ── N [events] (JSONB payload, GIN indexed)
```

## Key Query Capabilities
- MRR (Monthly Recurring Revenue) aggregation across active subscription tiers.
- Seat utilization ratios: `COUNT(memberships) / subscriptions.seats_purchased`.
- JSONB telemetry querying: Extract nested keys (`payload->'env'`), filter with containment (`payload @> '{"format": "csv"}'`).
- Multi-tenant role authorization verification.
