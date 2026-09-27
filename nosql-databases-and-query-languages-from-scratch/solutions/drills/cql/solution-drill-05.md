# Reference Solution for Drill 05: Cassandra CQL Partition & Clustering Queries

## Query Statement
```text
-- Target Language: CQL
-- Evaluated against seed dataset
SELECT * FROM cql 
WHERE partition_key = 'CQL_ID_0005' 
  AND metric >= 50 
ORDER BY created_at DESC 
LIMIT 10;
```

## Physical Storage Path
1. Coordinator node hashes `partition_key` to locate exact storage partition.
2. Index seek resolves `created_at DESC` range boundary without in-memory sorting.
3. Exactly 10 items read and emitted to network. Read amplification: 1.0.
