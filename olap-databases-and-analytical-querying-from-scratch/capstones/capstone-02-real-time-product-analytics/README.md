# Capstone 2: Real-Time Product Analytics Platform

## Capstone Mission
Architect a streaming ingestion pipeline processing clickstream events with sub-second query latency for conversion funnels and retention analysis.

## Requirements & Evaluation Criteria
1. **Mechanical Rigor**: Justify every storage layout, partition key, and sorting key from first principles.
2. **Physical Verification**: Provide query plans (`EXPLAIN ANALYZE`), bytes scanned, and memory allocations.
3. **Failure Resilience**: Demonstrate how the system behaves under memory limits and partition skew.
4. **Honest Metrics**: Adhere to `BENCHMARK_TEMPLATE.md` with zero benchmark theater.
