# Capstone 6: OLAP Production Chaos & Failure Day

## Capstone Mission
Diagnose and recover 10 injected production failures: ClickHouse merge backlog, partition explosion, hash join OOM, and unpruned partition scans.

## Requirements & Evaluation Criteria
1. **Mechanical Rigor**: Justify every storage layout, partition key, and sorting key from first principles.
2. **Physical Verification**: Provide query plans (`EXPLAIN ANALYZE`), bytes scanned, and memory allocations.
3. **Failure Resilience**: Demonstrate how the system behaves under memory limits and partition skew.
4. **Honest Metrics**: Adhere to `BENCHMARK_TEMPLATE.md` with zero benchmark theater.
