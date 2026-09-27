# Relational Database Mental Models

> **Repository Motto:** Understand it. Model it. Query it. Inspect it. Measure it. Break it. Fix it. Optimize it. Ship it.

To become a master of relational databases and SQL, you must develop five mechanical mental models:

```text
1. Relational Algebra (The Mathematical Foundation)
2. Physical Page Storage (How Bytes Sit on NVMe/Disk)
3. The B-Tree Index (How Lookups Avoid Full Scans)
4. Multi-Version Concurrency Control / MVCC (How Readers Don't Block Writers)
5. The Query Optimizer / Planner (How Declarative SQL Becomes an Imperative Plan Tree)
```

---

## 1. Relational Algebra

Invented by Edgar F. Codd in 1970, relational algebra treats data as mathematical relations (tables) containing sets of tuples (rows). Every operation takes one or more relations as input and produces a new relation as output (**Relational Closure**).

```text
┌─────────────────────────┬──────────────────────┬───────────────────────────────┐
│ Relational Operation    │ SQL Equivalent       │ Mathematical Meaning          │
├─────────────────────────┼──────────────────────┼───────────────────────────────┤
│ Selection (σ)           │ WHERE                │ Filters tuples by predicate   │
│ Projection (π)          │ SELECT columns       │ Extracts specific attributes  │
│ Cartesian Product (×)   │ CROSS JOIN           │ Every tuple paired with every │
│ Natural / Theta Join (⋈)│ INNER JOIN ON ...    │ Pairs matching predicates     │
│ Union (∪)               │ UNION                │ Set combination (deduplicated)│
│ Difference (−)          │ EXCEPT               │ Tuples in R but not in S      │
│ Intersection (∩)        │ INTERSECT            │ Tuples common to both R and S │
│ Extended Aggregate (γ)  │ GROUP BY + Aggregate │ Partitions & collapses tuples │
└─────────────────────────┴──────────────────────┴───────────────────────────────┘
```

**Key Insight:** Because relational operations are closed, you can compose, nest, and reorder them. The SQL Query Optimizer leverages this property to rewrite your query into an equivalent algebraic expression with lower computational cost.

---

## 2. Physical Page Storage (PostgreSQL Heap Pages)

Databases do not read individual rows from disk. They read and write fixed-size blocks called **Pages** (in PostgreSQL, 8192 bytes = 8KB).

```text
 0                                                          8192 bytes
┌─────────────────┬──────────┬───────────┬──────────────┬──────────────┐
│  PageHeaderData │ ItemIdData [1..N]    │ (Free Space) │ HeapTuples   │
│  (24 bytes)     │ (Pointers to tuples) │              │ (Stored rows)│
└─────────────────┴──────────┴───────────┴──────────────┴──────────────┘
  ▲                 ▲                                    ▲
  │                 │                                    │
  Page LSN & flags  Offset & length to tuple in page     Data payload
```

- **ctid (Item Pointer):** Every tuple is identified by a physical address `(page_number, item_offset)`, e.g., `(42, 3)` means page 42, item pointer 3.
- **Sequential Scan:** The engine reads page 0, page 1, page 2... into the buffer cache in memory, inspecting every tuple.
- **Tuple Overhead:** Each PostgreSQL tuple has a 23-byte header containing transaction metadata (`xmin`, `xmax`, `t_ctid`, `infomasks`).

---

## 3. The B-Tree Index

When a table has 10,000,000 rows across 500,000 pages, a sequential scan requires reading 4GB of data. A B-Tree (specifically a balanced $B^+$-Tree) allows finding any row in 3 to 4 page reads:

```text
                  ┌──────────────┐
                  │  Root Page   │
                  │ [100 | 500]  │
                  └──────┬───────┘
            ┌────────────┼────────────┐
            ▼                         ▼
     ┌──────────────┐          ┌──────────────┐
     │ Internal Page│          │ Internal Page│
     │  [25 | 75]   │          │ [650 | 850]  │
     └──────┬───────┘          └──────┬───────┘
       ┌────┴────┐               ┌────┴────┐
       ▼         ▼               ▼         ▼
  ┌─────────┐ ┌─────────┐   ┌─────────┐ ┌─────────┐
  │ Leaf P1 │─│ Leaf P2 │───│ Leaf P3 │─│ Leaf P4 │ (Doubly linked leaf chain)
  │ k:1->ctid│ │k:50->ctid│  │k:600->..│ │k:900->..│
  └─────────┘ └─────────┘   └─────────┘ └─────────┘
```

- **Equality Lookup ($O(\log N)$):** Traverse root -> internal -> leaf -> fetch heap page by `ctid`.
- **Range Scan:** Traverse to the starting leaf node, then walk the sibling pointers (`Leaf P1 -> Leaf P2`) sequentially.
- **Index-Only Scan:** If the index contains all required columns and the visibility map indicates the page has no unvacuumed dead tuples, the engine never touches the heap table!

---

## 4. Multi-Version Concurrency Control (MVCC)

Traditional databases locked entire tables or rows during updates, causing readers to block writers and writers to block readers. PostgreSQL uses MVCC:

```text
Transaction 101: INSERT row -> Heap tuple created with xmin=101, xmax=0
Transaction 102: UPDATE row -> Old tuple marked xmax=102
                               New tuple created with xmin=102, xmax=0
```

- **xmin:** The transaction ID that inserted this tuple version.
- **xmax:** The transaction ID that updated or deleted this tuple version (or 0 if still alive).
- **Snapshot Isolation:** When a query begins, it takes a snapshot of active transactions. It only sees tuples where `xmin` committed before the snapshot began and `xmax` has not committed.
- **Result:** Readers never block writers, and writers never block readers!
- **Consequence:** Updates do not overwrite in place; they create new versions. The `VACUUM` process is responsible for reclaiming space occupied by dead tuples.

---

## 5. The Query Planner & Optimizer

Declarative SQL specifies *what* you want. The Query Planner determines *how* to execute it:

```text
                     Raw SQL Text
                          │
                          ▼
                      [ Parser ] ──► Abstract Syntax Tree (AST)
                          │
                          ▼
                      [ Analyzer / Rewriter ] ──► Query Tree (resolves views/rules)
                          │
                          ▼
                      [ Planner / Optimizer ]
                          ├── Estimate Selectivity & Cardinality (pg_statistic)
                          ├── Generate Execution Paths (SeqScan, IndexScan, HashJoin)
                          └── Calculate Cost ($Cost = Pages \times 1.0 + Tuples \times 0.01$)
                          │
                          ▼
                      [ Chosen Plan Tree ]
                          │
                          ▼
                      [ Executor ] ──► Result Tuples
```
