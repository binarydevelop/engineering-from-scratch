# Reference Solution for Drill 02: Neo4j Cypher Graph Pattern Matching

## Query Statement
```text
-- Target Language: Cypher 5
-- Evaluated against seed dataset
SELECT * FROM cypher 
WHERE partition_key = 'CYPHER_ID_0002' 
  AND metric >= 20 
ORDER BY created_at DESC 
LIMIT 10;
```

## Physical Storage Path
1. Coordinator node hashes `partition_key` to locate exact storage partition.
2. Index seek resolves `created_at DESC` range boundary without in-memory sorting.
3. Exactly 10 items read and emitted to network. Read amplification: 1.0.
