# Database & SQL Engineering Glossary

> **Repository Motto:** Understand it. Model it. Query it. Inspect it. Measure it. Break it. Fix it. Optimize it. Ship it.

| Term | What People Say (Misconception) | What It Actually Means (Relational Engineering Reality) |
| :--- | :--- | :--- |
| **Relation** | "A table." | A mathematical set of unordered tuples conforming to a fixed heading of typed attributes with no duplicate rows. |
| **Tuple** | "A row in Excel." | An unordered set of attribute-value pairs within a relation, mathematically identified by its candidate keys. |
| **Grain** | "The size of the table." | The atomic real-world business entity represented by exactly one row in a dataset or result set. |
| **Primary Key** | "An auto-incrementing ID column." | A chosen minimal candidate key that enforces both `UNIQUE` and `NOT NULL` constraints, providing permanent entity identity. |
| **Foreign Key** | "A link between two tables." | A referential integrity constraint ensuring that values in referencing columns exist in referenced candidate key columns. |
| **NULL** | "Zero, blank, or empty string." | A marker denoting absent, inapplicable, or unknown information, evaluated using Three-Valued Logic (`UNKNOWN`). |
| **WHERE** | "Filters the output." | A predicate filter applied during relation scanning *before* any grouping or aggregation occurs. |
| **HAVING** | "A WHERE clause for numbers." | A predicate filter applied *after* grouping to eliminate aggregated buckets. |
| **B-Tree** | "A binary search tree." | A balanced, multi-way search tree with high branching factor (fanout ~100-300), storing ordered keys in 8KB disk blocks with doubly linked leaf chains. |
| **Sequential Scan** | "A slow query." | The physical access method of reading every page of a table in order. It is optimal when scanning high percentages of a table or small relations. |
| **Index Scan** | "The fastest query possible." | Traversing an index B-tree to locate tuple item pointers (`ctid`), then fetching the corresponding heap pages. Can cause random I/O if unclustered. |
| **Index Only Scan** | "An index scan." | Retrieving all requested query columns directly from the index leaf pages without fetching heap pages, verified via the visibility map. |
| **Card. Estimation** | "The number of rows returned." | The query optimizer's statistical forecast of row counts at each plan node, calculated from histogram buckets in `pg_statistic`. |
| **MVCC** | "A row-level locking system." | Multi-Version Concurrency Control: An engine design where updates create new tuple versions (`xmin`/`xmax`), allowing readers and writers to operate concurrently without blocking. |
| **ACID** | "A guarantee that data is safe." | Four strict guarantees: Atomicity (all-or-nothing), Consistency (constraint preservation), Isolation (concurrency boundaries), Durability (persisted to WAL). |
| **Deadlock** | "A slow database lock." | A circular dependency graph between two or more transactions waiting for locks held by each other, resolved only when the engine aborts one session. |
| **Buffer Pool** | "RAM used by PostgreSQL." | An in-memory cache of fixed 8KB shared disk pages managed by a clock-sweep eviction algorithm. |
| **WAL** | "A transaction backup." | Write-Ahead Logging: An append-only binary log where changes must be flushed to non-volatile disk *before* heap pages are modified in memory, ensuring durability. |
