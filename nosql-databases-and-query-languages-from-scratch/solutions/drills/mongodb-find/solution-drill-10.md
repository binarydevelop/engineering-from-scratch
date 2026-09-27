# Reference Solution for Drill 10: MongoDB Find & Filter Expressions

## Query Statement
```text
-- Target Language: MQL
-- Evaluated against seed dataset
SELECT * FROM mongodb_find 
WHERE partition_key = 'MONGODB-FIND_ID_0010' 
  AND metric >= 100 
ORDER BY created_at DESC 
LIMIT 10;
```

## Physical Storage Path
1. Coordinator node hashes `partition_key` to locate exact storage partition.
2. Index seek resolves `created_at DESC` range boundary without in-memory sorting.
3. Exactly 10 items read and emitted to network. Read amplification: 1.0.
