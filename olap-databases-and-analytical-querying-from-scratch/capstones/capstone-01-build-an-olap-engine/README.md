# Capstone 1: Build an OLAP Engine from Scratch

## Capstone Mission
Design and implement a complete educational columnar engine supporting binary column storage, dictionary encoding, zone-map data skipping, and vectorized query execution.

## Requirements & Evaluation Criteria
1. **Mechanical Rigor**: Justify every storage layout, partition key, and sorting key from first principles.
2. **Physical Verification**: Provide query plans (`EXPLAIN ANALYZE`), bytes scanned, and memory allocations.
3. **Failure Resilience**: Demonstrate how the system behaves under memory limits and partition skew.
4. **Honest Metrics**: Adhere to `BENCHMARK_TEMPLATE.md` with zero benchmark theater.
