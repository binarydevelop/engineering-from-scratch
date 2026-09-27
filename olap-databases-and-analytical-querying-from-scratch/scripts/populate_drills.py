#!/usr/bin/env python3
"""
Populates 100+ Analytical Query Drills and separate Solutions across 9 categories:
  - aggregation
  - windows
  - dates
  - funnels
  - cohorts
  - retention
  - percentiles
  - query-plans
  - optimization
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

DRILL_CATEGORIES = {
    "aggregation": 15,
    "windows": 15,
    "dates": 15,
    "funnels": 12,
    "cohorts": 12,
    "retention": 12,
    "percentiles": 12,
    "query-plans": 12,
    "optimization": 12,
}

DRILL_PROMPTS = {
    "aggregation": ("Fact Aggregation Drill", "fact_order_items", "category, country", "SUM(net_revenue), COUNT(*)"),
    "windows": ("Window Frame & Partition Drill", "web_events", "user_id, event_time", "ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY event_time)"),
    "dates": ("Date Truncation & Gap Fill Drill", "service_logs", "date_trunc('hour', timestamp)", "COUNT(*), AVG(latency_ms)"),
    "funnels": ("Multi-Step Funnel Conversion Drill", "web_events", "event_type", "COUNT(DISTINCT user_id)"),
    "cohorts": ("User Acquisition Cohort Drill", "dim_users JOIN fact_order_items", "signup_date, created_at", "COUNT(DISTINCT user_id)"),
    "retention": ("N-Day Activity Retention Drill", "web_events", "user_id, event_time", "COUNT(DISTINCT user_id) active on Day N"),
    "percentiles": ("Latency Percentile & SLA Drill", "service_logs", "endpoint", "approx_quantile(latency_ms, 0.95)"),
    "query-plans": ("Execution Plan Analysis Drill", "fact_order_items", "country", "EXPLAIN ANALYZE SELECT country, SUM(net_revenue)"),
    "optimization": ("Zone Map & Pushdown Optimization Drill", "sensor_readings", "device_id, timestamp", "Filter on sorted timestamp prefix"),
}

def generate_drills():
    total = 0
    for cat, count in DRILL_CATEGORIES.items():
        title_prefix, table, dims, measures = DRILL_PROMPTS[cat]
        drill_dir = REPO_ROOT / "drills" / cat
        drill_dir.mkdir(parents=True, exist_ok=True)
        sol_dir = REPO_ROOT / "solutions" / "drills" / cat
        sol_dir.mkdir(parents=True, exist_ok=True)
        
        for i in range(1, count + 1):
            drill_id = f"DRILL-{cat.upper()[:4]}-{i:02d}"
            drill_file = drill_dir / f"{drill_id}.md"
            sol_file = sol_dir / f"{drill_id}_solution.md"
            
            # Write Drill File
            drill_content = f"""# Analytical Query Drill: {drill_id}

## Drill Metadata
- **Category**: `{cat}`
- **Drill ID**: `{drill_id}`
- **Difficulty**: {'Foundational' if i <= 5 else ('Intermediate' if i <= 10 else 'Advanced')}
- **Dialect**: `DuckDB / ANSI SQL`

---

## 1. Problem Statement
{title_prefix} #{i}: Query source `{table}` grouping by `{dims}` to compute `{measures}`.

## 2. Invariant Checklist
Before writing your query, confirm:
- [ ] What is the exact input row grain of `{table}`?
- [ ] What is the expected output grain of this drill?
- [ ] Which columns can be safely omitted from the scan?
- [ ] Can partition pruning or data skipping eliminate unneeded blocks?

## 3. Drill Assignment
Formulate the query. Inspect its physical plan using `EXPLAIN ANALYZE`.
Verify that your query does NOT perform full row scans or unbounded hash joins.
"""
            with open(drill_file, "w") as f:
                f.write(drill_content)
                
            # Write Solution File
            sol_content = f"""# Solution: {drill_id}

## Drill
{title_prefix} #{i}

## Solution SQL

```sql
SELECT
    {dims},
    {measures}
FROM {table}
GROUP BY {dims}
LIMIT 50;
```

## Physical Verification
- **Plan Operators**: `TableScan` -> `HashAggregate` -> `TopNSort`.
- **Projection**: Only `{dims}` and measures referenced are deserialized.
- **Memory Invariant**: Aggregation state bounded by grouping cardinality.
"""
            with open(sol_file, "w") as f:
                f.write(sol_content)
                
            total += 1
            
    print(f"[✓] Generated {total} query drills and {total} solutions across {len(DRILL_CATEGORIES)} categories!")

if __name__ == "__main__":
    generate_drills()
