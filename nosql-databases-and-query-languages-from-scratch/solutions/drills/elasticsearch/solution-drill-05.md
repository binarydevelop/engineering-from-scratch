# Reference Solution for Drill 05: Elasticsearch JSON Query DSL & Aggregations

## Query Statement
```text
-- Target Language: Query DSL
-- Evaluated against seed dataset
SELECT * FROM elasticsearch 
WHERE partition_key = 'ELASTICSEARCH_ID_0005' 
  AND metric >= 50 
ORDER BY created_at DESC 
LIMIT 10;
```

## Physical Storage Path
1. Coordinator node hashes `partition_key` to locate exact storage partition.
2. Index seek resolves `created_at DESC` range boundary without in-memory sorting.
3. Exactly 10 items read and emitted to network. Read amplification: 1.0.
