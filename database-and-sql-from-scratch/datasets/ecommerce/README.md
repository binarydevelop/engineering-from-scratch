# E-Commerce Dataset

A transactional retail database modeling an online technology, kitchen, and media store.

## Entity-Relationship Diagram

```text
  [customers] 1 ──── N [addresses]
       │
       │ 1
       │
       ▼ N
    [orders] 1 ─────── N [order_items] N ────── 1 [products] 1 ── 1 [inventory]
       │                                              │
       ├── 1 ── N [payments]                          ▼ N
       │               │ 1                     [categories] (hierarchical)
       │               │
       └── 1 ── N [refunds] ◄─────────────────────────┘
```

## Key Grain & Cardinality Facts
- `customers`: 1 row = 1 registered account.
- `orders`: 1 row = 1 order transaction.
- `order_items`: 1 row = 1 specific product inside an order.
- `categories`: Self-referencing tree via `parent_id` (used for Recursive CTE drills).
- Customer #14 and #15 have **zero orders** (essential for `LEFT JOIN` and `NOT EXISTS` drills).
- Order #9 is **refunded** (essential for business queries excluding refunds).
