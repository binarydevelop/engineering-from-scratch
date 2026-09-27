# Final OLAP Architecture Challenge: 5 TB/Day Global SaaS

## Capstone Mission
Reason through and architect the complete end-to-end analytical platform for a global multi-tenant SaaS producing 5 TB of raw events daily.

## Requirements & Evaluation Criteria
1. **Mechanical Rigor**: Justify every storage layout, partition key, and sorting key from first principles.
2. **Physical Verification**: Provide query plans (`EXPLAIN ANALYZE`), bytes scanned, and memory allocations.
3. **Failure Resilience**: Demonstrate how the system behaves under memory limits and partition skew.
4. **Honest Metrics**: Adhere to `BENCHMARK_TEMPLATE.md` with zero benchmark theater.
