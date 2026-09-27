# Columnar Storage Internals: Mechanical Principles

This document provides a deep physical explanation of how columnar storage works at the byte and disk block levels.

---

## 1. Physical Layout Comparison: Row Store vs Column Store

Consider a table with 4 columns and 4 rows:

```text
Table Schema:
  id: INT (4 bytes)
  country: CHAR(2) (2 bytes)
  user_id: BIGINT (8 bytes)
  revenue: DOUBLE (8 bytes)
Total row size = 22 bytes.
```

### Row-Oriented Layout (Heap Pages):
Values are written row-by-row consecutively:
```text
[id_1, country_1, user_1, rev_1] [id_2, country_2, user_2, rev_2] [id_3, country_3, user_3, rev_3] [id_4, country_4, user_4, rev_4]
```
If a query asks: `SELECT SUM(revenue) FROM orders;`:
- The storage engine MUST read through `id`, `country`, and `user_id` to reach each `revenue` value.
- To read 100M rows, the engine scans $100\text{M} \times 22 \text{ bytes} \approx 2.2 \text{ GB}$ of data, even though `revenue` only accounts for $0.8 \text{ GB}$.

### Column-Oriented Layout (Columnar Partitions):
Each column is stored in a separate contiguous array on disk:
```text
File id.bin:      [id_1, id_2, id_3, id_4]
File country.bin: [country_1, country_2, country_3, country_4]
File user_id.bin: [user_1, user_2, user_3, user_4]
File revenue.bin: [rev_1, rev_2, rev_3, rev_4]
```
When running `SELECT SUM(revenue) FROM orders;`:
- The engine opens **only** `revenue.bin`.
- Files `id.bin`, `country.bin`, and `user_id.bin` are **never touched**.
- Total I/O drops immediately by 63.6% before compression is even applied!

---

## 2. Why Column Stores Compress 5× to 20× Better

In a row store, adjacent bytes have completely different types and distributions (an integer ID followed by a country string followed by a timestamp). The entropy is high, making general-purpose compression (like Gzip) slow and inefficient.

In a column store, adjacent values come from the **exact same domain**:
1. **Low Information Entropy**: A `country` column in a table of 10M rows contains only 200 distinct string values.
2. **Predictable Sequences**: A `timestamp` column sorted chronologically consists of monotonically increasing numbers.
3. **Repeated Numbers**: A `status` column has only 4 distinct values (`pending`, `paid`, `shipped`, `cancelled`).

### Specialized Column Encodings:

#### A. Dictionary Encoding
Replaces distinct variable-length strings with compact integer IDs.
```text
Raw:        ["US", "DE", "US", "US", "DE", "IN"]
Dictionary: {0: "US", 1: "DE", 2: "IN"}
Encoded:    [0, 1, 0, 0, 1, 2]  (Stored as 8-bit integers)
```
Scan operations can evaluate predicates directly on dictionary IDs (`id == 0`) without decoding strings.

#### B. Run-Length Encoding (RLE)
Collapses repeated sequences of identical values into `(value, count)` pairs:
```text
Raw:     [US, US, US, US, US, DE, DE, DE]
Encoded: [(US, 5), (DE, 3)]
```
Reduces millions of sorted rows down to a few kilobytes.

#### C. Delta Encoding + Bit Packing
Stores the differences between successive numbers:
```text
Raw Timestamps: [1700000000, 1700000002, 1700000005, 1700000007]
Delta:          [1700000000, +2, +3, +2]
```
The delta values ($+2, +3$) fit into 2 bits rather than 64 bits. Bit packing packs four 2-bit numbers into a single 8-bit byte.

---

## 3. Anatomy of a Parquet File

Apache Parquet is the industry-standard open columnar file format for analytical systems:

```text
┌────────────────────────────────────────────────────────┐
│ File Header: Magic Number "PAR1"                       │
├────────────────────────────────────────────────────────┤
│ ROW GROUP 1 (e.g. 500,000 rows)                        │
│ ┌────────────────────────────────────────────────────┐ │
│ │ Column Chunk 1 (user_id): Pages, Min/Max Stats     │ │
│ ├────────────────────────────────────────────────────┤ │
│ │ Column Chunk 2 (country): Dictionary, Data Pages   │ │
│ ├────────────────────────────────────────────────────┤ │
│ │ Column Chunk 3 (revenue): Compressed Data Pages    │ │
│ └────────────────────────────────────────────────────┘ │
├────────────────────────────────────────────────────────┤
│ ROW GROUP 2 (e.g. 500,000 rows)                        │
│ ...                                                    │
├────────────────────────────────────────────────────────┤
│ FILE METADATA FOOTER                                   │
│ - Schema Definition                                    │
│ - Row Group Offsets & Row Counts                       │
│ - Column Chunk Metadata (Min/Max values, Null counts)  │
│ - Size of Footer (4 bytes)                             │
│ - File Trailer: Magic Number "PAR1"                    │
└────────────────────────────────────────────────────────┘
```

### Why Reading the Footer First Matters:
When DuckDB or ClickHouse reads a Parquet file:
1. It reads the last few kilobytes of the file to inspect the **Footer**.
2. It examines the min/max statistics for every Row Group.
3. If the query is `WHERE country = 'JP'`, and Row Group 1 has `min = 'AU'` and `max = 'DE'`, Row Group 1 is **skipped completely**.

---

## 4. Anatomy of a ClickHouse MergeTree Part

ClickHouse stores table data in immutable filesystem directories called **parts**:

```text
/var/lib/clickhouse/data/olaplab/fact_order_items/202601_1_1_0/
├── checksums.txt            # Integrity verification
├── columns.txt              # Column names and types
├── count.txt                # Number of rows in part
├── default_compression_codec.txt
├── primary.cidx             # Sparse primary index in RAM
├── country.bin              # Compressed columnar data
├── country.mrk2             # Marks linking index marks to .bin offsets
├── revenue.bin              # Compressed columnar data
└── revenue.mrk2             # Marks linking index marks to .bin offsets
```

### The Role of Marks (`.mrk2`):
- ClickHouse does not index every row. It indexes every **granule** (default 8,192 rows).
- The `primary.cidx` contains the primary key value at the beginning of each granule.
- The `.mrk2` file tells the query engine the exact byte offset inside `revenue.bin` where granule #42 starts.
- This allows ClickHouse to seek directly to the relevant compressed block in `revenue.bin` without reading unreferenced granules.
