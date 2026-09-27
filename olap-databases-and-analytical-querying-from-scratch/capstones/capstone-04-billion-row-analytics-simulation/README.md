# Capstone 4: Scalable Analytical Stress Simulation

## Capstone Mission
Generate scaled datasets (1M, 10M, 100M rows) to measure how compression ratios, memory usage, and scan bandwidth scale under increasing load.

## Requirements & Evaluation Criteria
1. **Mechanical Rigor**: Justify every storage layout, partition key, and sorting key from first principles.
2. **Physical Verification**: Provide query plans (`EXPLAIN ANALYZE`), bytes scanned, and memory allocations.
3. **Failure Resilience**: Demonstrate how the system behaves under memory limits and partition skew.
4. **Honest Metrics**: Adhere to `BENCHMARK_TEMPLATE.md` with zero benchmark theater.
