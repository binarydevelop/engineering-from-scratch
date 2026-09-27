# Reference Solution for Drill 12: DynamoDB PartiQL SQL-Compatible Queries

## Query Statement
```text
-- Target Language: PartiQL
-- Evaluated against seed dataset
SELECT * FROM partiql 
WHERE partition_key = 'PARTIQL_ID_0012' 
  AND metric >= 120 
ORDER BY created_at DESC 
LIMIT 10;
```

## Physical Storage Path
1. Coordinator node hashes `partition_key` to locate exact storage partition.
2. Index seek resolves `created_at DESC` range boundary without in-memory sorting.
3. Exactly 10 items read and emitted to network. Read amplification: 1.0.
