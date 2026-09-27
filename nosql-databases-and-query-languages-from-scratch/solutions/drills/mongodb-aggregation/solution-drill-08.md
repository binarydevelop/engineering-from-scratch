# Reference Solution for Drill 08: MongoDB Aggregation Pipeline Stages

## Query Statement
```text
-- Target Language: MQL Aggregation
-- Evaluated against seed dataset
SELECT * FROM mongodb_aggregation 
WHERE partition_key = 'MONGODB-AGGREGATION_ID_0008' 
  AND metric >= 80 
ORDER BY created_at DESC 
LIMIT 10;
```

## Physical Storage Path
1. Coordinator node hashes `partition_key` to locate exact storage partition.
2. Index seek resolves `created_at DESC` range boundary without in-memory sorting.
3. Exactly 10 items read and emitted to network. Read amplification: 1.0.
