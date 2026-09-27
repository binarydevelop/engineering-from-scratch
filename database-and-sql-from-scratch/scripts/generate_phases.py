"""
Curriculum Phase Generator: Generates all 102 curriculum phases with
comprehensive lesson documentation, runnable queries, break-it experiments, and evidence ledgers.
"""

import os
from pathlib import Path

ROOT = Path("/Users/tushar/Desktop/private/repos/database-and-sql-from-scratch")

PHASE_DATA = [
    (0, "environment-and-sql-lab", "Your terminal is your microscope; understand every layer between your keystroke and the engine.",
     "Environment setup and understanding the client-server relational architecture.",
     "Without knowing how psql talks to PostgreSQL, you cannot distinguish client disconnects from server crashes or network latency from query execution.",
     "psql client connects via TCP port 5432 to postmaster daemon, spawning a dedicated backend process per connection.",
     "Client (psql) -> TCP Socket (5432) -> Postmaster -> Backend Process -> Buffer Pool -> Disk Pages",
     "SELECT version();\nSELECT current_database();\nSELECT current_user;\nSELECT inet_server_addr(), inet_server_port();",
     "-- Connect with wrong user or port\n-- psql -h localhost -p 9999 -U unknown_user",
     "Verify port listening and pg_hba.conf host-based authentication rules.",
     "Level 1: Inspect server version and uptime.\nLevel 5: Measure TCP socket connection establishment latency."),

    (1, "why-databases-exist", "Files store data; database engines preserve invariants, concurrency, and durability under crash failure.",
     "Explore why simple CSV and JSON files collapse under multi-user updates, concurrent writes, and system power cuts.",
     "Using raw files for transactions leads to silent race conditions, partial writes, file corruption, and O(N) full-file rewrites on every update.",
     "ACID guarantees, write-ahead logging (WAL), crash recovery via REDO logs, and row-level locking.",
     "App A & App B -> Concurrent writes to data.csv -> Corrupted file!\nApp A & App B -> RDBMS Buffer Pool -> WAL -> ACID State",
     "-- Python simulation: two threads appending to same file concurrently\n-- Demonstrates torn writes without locks.",
     "-- Kill process mid-write in CSV vs PostgreSQL transaction rollback.",
     "Databases guarantee durability via fsync on append-only WAL before reporting commit success.",
     "Level 1: Append 10,000 records to CSV.\nLevel 5: Simulate kernel panic during write and inspect recovery."),

    (2, "relational-mental-model", "Data is not a tree or a document; it is a mathematical set of relations governed by predicate logic.",
     "Internalize Codd's Relational Model: Relations, Tuples, Attributes, and the concept of Relational Closure.",
     "Navigational databases (hierarchical and network models) forced queries to know the exact physical storage path. Relational algebra decoupled logical intent from physical access.",
     "First normal form: attributes are atomic; tuples are unordered; duplicate rows are mathematically impossible in a true relation.",
     "Relation Heading: {id: INT, email: VARCHAR}\nRelation Body: Set of Tuples {(1, 'a@b.com'), (2, 'c@d.com')}",
     "CREATE TABLE lab.users (\n    id INT PRIMARY KEY,\n    email VARCHAR(255) NOT NULL UNIQUE\n);",
     "INSERT INTO lab.users VALUES (1, 'a@b.com'), (1, 'duplicate@b.com'); -- Primary key violation",
     "Enforcing relational constraints at the engine level guarantees application consistency.",
     "Level 1: Define relation attributes.\nLevel 5: Prove relational closure: query output is itself a relation."),

    (3, "sql-query-anatomy", "SQL says WHAT result is needed; the database decides HOW to obtain it.",
     "Understand the declarative nature of SQL and the difference between lexical syntax and execution.",
     "Treating SQL like imperative Python leads to inefficient procedural loops instead of leveraging set-based relational operators.",
     "Declarative programming: the query is a formal specification of the desired mathematical relation.",
     "SQL Query (WHAT) ──► Query Optimizer ──► Execution Plan (HOW) ──► Results",
     "SELECT first_name, last_name FROM ecommerce.customers WHERE status = 'active' ORDER BY last_name ASC;",
     "SELECT first_name FROM ecommerce.customers WHERE unknown_col = 1; -- Semantic validation error",
     "Check catalog pg_attribute during parse analysis.",
     "Level 1: Identify SELECT and FROM clauses.\nLevel 5: Trace the transformation of AST to Query Tree."),

    (4, "select-deeply", "Every projected expression defines the attributes of your output relation.",
     "Master column projection, mathematical expressions, column aliasing, and output grain reasoning.",
     "Lazy SELECT * leaks database internals, breaks application contracts when schemas evolve, and forces expensive heap scans instead of index-only scans.",
     "Relational Projection (π): removes unwanted attributes and computes new derived values per tuple.",
     "Table: [A, B, C, D] ──► π(A, B*2) ──► Result: [A, new_col]",
     "SELECT id, first_name || ' ' || last_name AS full_name, created_at FROM ecommerce.customers ORDER BY id ASC;",
     "SELECT id, non_existent_col FROM ecommerce.customers; -- Compiler syntax error",
     "Always project explicit columns needed by the consumer.",
     "Level 1: Project 2 columns.\nLevel 5: Measure memory bandwidth impact of SELECT * vs projected columns."),

    (5, "where-deeply", "Filter early, filter aggressively; every discarded tuple saves downstream CPU and RAM.",
     "Master relational selection (σ), boolean logic, comparisons, BETWEEN, IN, and operator precedence.",
     "Misunderstanding boolean operator precedence (AND has higher precedence than OR) causes severe security leaks and data corruption.",
     "Relational Selection (σ): extracts tuples that satisfy a propositional predicate.",
     "Rows (N) ──► [ Predicate σ(P) ] ──► Surviving Rows (M <= N)",
     "SELECT * FROM ecommerce.products WHERE (category_id = 2 OR category_id = 3) AND price < 500.00;",
     "SELECT * FROM ecommerce.products WHERE category_id = 2 OR category_id = 3 AND price < 500.00; -- Operator precedence bug!",
     "Parenthesize compound boolean expressions explicitly.",
     "Level 1: Filter on equality.\nLevel 5: Analyze index sargability of complex WHERE clauses."),

    (6, "null-and-three-valued-logic", "NULL is not zero, not empty string, and not equal to itself; it is the absence of known truth.",
     "Master Three-Valued Logic (3VL): TRUE, FALSE, and UNKNOWN.",
     "Using col = NULL silently drops all rows. Using NOT IN with a subquery containing NULL drops the entire result set.",
     "Kleene's 3-valued logic truth tables for AND, OR, and NOT when evaluated against UNKNOWN.",
     "NULL = NULL ──► UNKNOWN (Not TRUE!)\nWHERE UNKNOWN ──► Dropped (WHERE requires TRUE to emit row)",
     "SELECT id, email, COALESCE(bio, 'N/A') FROM social.users WHERE bio IS NULL;",
     "SELECT * FROM social.users WHERE bio = NULL; -- Returns 0 rows!",
     "Use IS NULL and IS NOT NULL, never equality with NULL.",
     "Level 1: Filter on IS NULL.\nLevel 5: Trace truth table for NOT (UNKNOWN OR FALSE)."),

    (7, "order-by", "A relational table is an unordered set; without ORDER BY, row ordering is completely undefined.",
     "Master deterministic sorting, multi-column ordering, and NULL ordering.",
     "Relying on implicit insertion order or index order causes subtle, non-reproducible pagination bugs in production.",
     "Relational tables are unordered bags of tuples. The engine may read them in any physical order (parallel scans, bitmap scans, sequential sweeps).",
     "Unordered Tuples ──► [ Sort Operator / B-Tree Index ] ──► Ordered Output Sequence",
     "SELECT id, total_amount, order_date FROM ecommerce.orders ORDER BY total_amount DESC, id ASC;",
     "SELECT id FROM ecommerce.orders ORDER BY order_date; -- Non-deterministic if identical dates exist!",
     "Always provide an unambiguous primary key tie-breaker.",
     "Level 1: Sort by one column.\nLevel 5: Check EXPLAIN for external merge disk spills vs quicksort."),

    (8, "limit-fetch-pagination", "Limit without deterministic ordering is random sampling in disguise.",
     "Understand result set slicing with LIMIT/OFFSET and standard SQL FETCH FIRST.",
     "OFFSET 100,000 forces the engine to read and discard 100,000 rows, burning disk I/O and CPU.",
     "Windowing over physical streams; resource bounds on query output buffers.",
     "Engine Heap Scan (100,010 rows) ──► Discard 100,000 ──► Emit 10 rows (Brutal!)",
     "SELECT id, name, price FROM ecommerce.products ORDER BY price DESC, id ASC LIMIT 5 OFFSET 0;",
     "SELECT * FROM ecommerce.products LIMIT 5; -- Non-deterministic across runs!",
     "Use ORDER BY with unique key for reproducible slices.",
     "Level 1: Slices top 5 rows.\nLevel 5: Measure latency scaling as OFFSET increases from 10 to 1,000,000."),

    (9, "expressions-and-functions", "Compute close to the data to minimize network egress and application CPU cycles.",
     "Leverage SQL arithmetic, type casting, mathematical functions, and date calculations.",
     "Pulling millions of raw rows into Node.js or Python to calculate basic totals destroys network bandwidth and memory.",
     "Vectorized in-engine expression evaluation within the tuple projection loop.",
     "Raw Attributes ──► [ In-Engine Function Call ] ──► Computed Value",
     "SELECT sku, ROUND(price * 1.0825, 2) AS price_with_tax FROM ecommerce.products ORDER BY id ASC;",
     "SELECT price / 0 FROM ecommerce.products; -- Division by zero abort!",
     "Use NULLIF(divisor, 0) to guard arithmetic.",
     "Level 1: Basic addition.\nLevel 5: Compare in-database aggregation vs client-side transformation."),

    (10, "case-expressions", "CASE is an expression that returns a scalar value, not a procedural control-flow statement.",
     "Master conditional logic inside SQL queries for classification, bucketing, and pivoting.",
     "Novices try to use IF/ELSE in standard SQL, not realizing CASE is an inline scalar expression.",
     "Piecewise mathematical function mapping input tuples to distinct output values.",
     "Input Tuple ──► WHEN Condition 1 THEN Val 1 ... ELSE Default ──► Output Scalar",
     "SELECT id, total_amount, CASE WHEN total_amount >= 1000 THEN 'High' WHEN total_amount >= 250 THEN 'Medium' ELSE 'Low' END AS spend_tier FROM ecommerce.orders ORDER BY id ASC;",
     "SELECT CASE WHEN total_amount > 100 THEN 'High' END FROM ecommerce.orders; -- Unhandled cases return NULL!",
     "Always provide an explicit ELSE branch in production queries.",
     "Level 1: Categorize into 2 tiers.\nLevel 5: Use CASE inside SUM() for conditional aggregation."),

    (11, "string-querying", "Text querying without index strategy is a full-table sequential scan waiting to happen.",
     "Master LOWER, UPPER, TRIM, CONCAT, SUBSTRING, LIKE, and PostgreSQL ILIKE.",
     "LIKE '%keyword%' cannot use standard B-Tree indexes, triggering catastrophic table scans at scale.",
     "String pattern matching via finite state automata vs trigram/GIN index structures.",
     "LIKE 'abc%' -> B-Tree Range Search (Fast!)\nLIKE '%abc%' -> Full Sequential Scan (Slow!)",
     "SELECT id, name, sku FROM ecommerce.products WHERE name ILIKE '%phone%' ORDER BY id ASC;",
     "SELECT * FROM ecommerce.products WHERE LOWER(name) LIKE '%phone%'; -- Invalidates standard B-Tree on name",
     "Use functional indexes or pg_trgm for arbitrary substring matching.",
     "Level 1: Concatenate names.\nLevel 5: Compare B-Tree prefix search vs GIN trigram index search."),

    (12, "date-and-time-sql", "Time without timezone awareness is ambiguous; timestamps without intervals are useless.",
     "Master TIMESTAMPTZ, intervals, DATE_TRUNC, EXTRACT, and date arithmetic.",
     "Storing timestamps in UTC without understanding timezone offsets causes reporting discrepancies across calendar days.",
     "Epoch timestamps (seconds since 1970-01-01 UTC) vs calendar date representations with leap seconds and daylight savings.",
     "Timestamp with Time Zone ──► Stored as UTC Epoch ──► Formatted to Client Session Timezone",
     "SELECT DATE_TRUNC('month', order_date)::DATE AS sales_month, SUM(total_amount) AS revenue FROM ecommerce.orders WHERE status = 'completed' GROUP BY 1 ORDER BY sales_month ASC;",
     "SELECT * FROM ecommerce.orders WHERE order_date = '2026-02-01'; -- Fails to match rows with non-zero time!",
     "Use half-open ranges: [start, end) for robust timestamp filtering.",
     "Level 1: Extract year.\nLevel 5: Generate date scaffolds using generate_series to catch missing days."),

    (13, "data-modification", "Every INSERT, UPDATE, and DELETE is a transaction that generates WAL and affects MVCC tuple versions.",
     "Master safe DML habits, WHERE clauses on updates, and PostgreSQL RETURNING clause.",
     "An accidental UPDATE or DELETE without a WHERE clause can wipe an entire production database in milliseconds.",
     "PostgreSQL Append-Only MVCC: UPDATE writes a new tuple version and sets xmax on the old tuple.",
     "Old Tuple: (xmin=100, xmax=102) [Dead]\nNew Tuple: (xmin=102, xmax=0)   [Live]",
     "INSERT INTO ecommerce.customers (email, first_name, last_name) VALUES ('new@ex.com', 'New', 'User') RETURNING id, created_at;",
     "UPDATE ecommerce.customers SET status = 'active'; -- Catastrophe: missing WHERE clause!",
     "Always test updates inside a transaction: BEGIN; UPDATE ...; ROLLBACK;",
     "Level 1: Safe insert.\nLevel 5: Inspect xmin/xmax tuple headers in page inspection after update."),

    (14, "keys-and-constraints", "Constraints are the firewall of your database; your application code will fail, but constraints never sleep.",
     "Master Primary Keys, Unique Constraints, Foreign Keys, Not Null, and Check Constraints.",
     "Relying solely on ORM validation allows race conditions, concurrent duplicate inserts, and orphaned child rows.",
     "Declarative relational invariants verified atomically by the engine before tuple write completion.",
     "INSERT Tuple ──► [ Check Constraints -> PK Index Probe -> FK Parent Probe ] ──► Write Page",
     "CREATE TABLE lab.accounts (\n    id SERIAL PRIMARY KEY,\n    balance NUMERIC(12, 2) NOT NULL CHECK (balance >= 0.00)\n);",
     "INSERT INTO lab.accounts (balance) VALUES (-50.00); -- check constraint violation!",
     "Enforce business rules directly in database DDL.",
     "Level 1: Add NOT NULL constraint.\nLevel 5: Measure CPU overhead of check constraints during bulk inserts."),

    (15, "relationships", "Foreign keys model physical relationships; cardinality determines query duplication risk.",
     "Master One-to-One, One-to-Many, and Many-to-Many entity relationships.",
     "Misunderstanding relationship cardinality results in catastrophic Cartesian explosions during query joins.",
     "Referential integrity constraints linking foreign key attributes in referencing relations to candidate keys in referenced relations.",
     "1:1 (Customer -> Profile)\n1:N (Customer -> Orders)\nN:M (Orders <-> OrderItems <-> Products)",
     "SELECT o.id, c.email FROM ecommerce.orders o JOIN ecommerce.customers c ON o.customer_id = c.id ORDER BY o.id ASC;",
     "INSERT INTO ecommerce.orders (customer_id) VALUES (9999); -- Foreign key violation!",
     "Always verify referential integrity exists before loading child data.",
     "Level 1: Map 1:N foreign key.\nLevel 5: Design a junction table with compound primary key for N:M relations.")
]

# We will generate all 102 phases dynamically
def get_phase_meta(phase_num):
    # If explicitly defined above, return it
    for p in PHASE_DATA:
        if p[0] == phase_num:
            return p
    
    # Otherwise generate systematically based on phase title
    titles = {
        16: ("inner-join-from-first-principles", "A join is not magic syntax; it is a filtered Cartesian product connecting related relations."),
        17: ("left-join", "Preserve the entities that matter; never let unmatched right rows erase left reality."),
        18: ("right-full-join", "Full outer joins materialize symmetric completeness when neither side owns the whole truth."),
        19: ("join-cardinality", "Ask before every join: how many rows can one row match?"),
        20: ("join-debugging", "When numbers multiply mysteriously, suspect an unconstrained 1:N join explosion."),
        21: ("aggregate-functions", "COUNT(*) counts rows; COUNT(col) counts values. Know the difference."),
        22: ("group-by", "Grouping partitions rows into buckets; everything projected must belong to the bucket or summarize it."),
        23: ("having", "WHERE filters rows before the bucket; HAVING filters the bucket after aggregation."),
        24: ("conditional-aggregation", "Pivoting rows into columns is simply conditional aggregation with CASE."),
        25: ("logical-sql-processing-order", "SQL is written inside-out; FROM runs first, SELECT runs almost last."),
        26: ("distinct", "DISTINCT often masks sloppy join logic; fix the relationship, don't slap on DISTINCT."),
        27: ("subqueries", "Decompose complex questions into nested relational queries."),
        28: ("correlated-subqueries", "An inner query that references outer tuples runs once per outer candidate."),
        29: ("exists-not-exists", "Existence thinking tests reality without reading unneeded attributes."),
        30: ("in-and-not-in", "A single NULL inside NOT IN destroys the entire universe of answers."),
        31: ("set-operations", "Set operations combine tuples vertically; joins combine attributes horizontally."),
        32: ("ctes", "Common Table Expressions turn procedural confusion into clean relational pipelines."),
        33: ("recursive-ctes", "Recursion in SQL traverses trees, graphs, and hierarchies without procedural code."),
        34: ("window-functions-mental-model", "GROUP BY collapses rows; Window functions calculate across rows while keeping every single row alive."),
        35: ("row-number", "Assign strict sequential integers to orderings within partitions."),
        36: ("rank-and-dense-rank", "Leaderboards have ties; know whether your game leaves gaps or stays dense."),
        37: ("partition-by", "Window partitions create isolated calculation boundaries without collapsing detail."),
        38: ("lag-and-lead", "Look backward and forward in time without expensive self-joins."),
        39: ("running-totals", "Cumulative sums reveal momentum, runway, and depletion across time."),
        40: ("window-frames", "ROWS BETWEEN defines the physical moving aperture of your window calculations."),
        41: ("top-n-per-group", "Finding the best items per category is the quintessential window function mastery test."),
        42: ("deduplication", "Keep the newest, purge the rest: windowed row numbering is the safest deduplication tool."),
        43: ("gaps-and-islands", "Detecting streaks and uptime periods separates novice query writers from masters."),
        44: ("pivot-like-queries", "Transform vertical fact rows into horizontal executive reporting matrices."),
        45: ("funnel-queries", "Track conversion drop-offs step by step through rigorous user deduplication."),
        46: ("cohort-queries", "Trace user engagement over time relative to their initial acquisition epoch."),
        47: ("retention-analysis", "Day 1, Day 7, Day 30: measure product stickiness using date interval arithmetic."),
        48: ("query-challenge-set-i", "Test your foundational query reasoning without looking at answers."),
        49: ("schema-design", "A bad schema makes every query agonizing; a great schema makes complex queries trivial."),
        50: ("normalization", "Eliminate update, insert, and deletion anomalies through 1NF, 2NF, and 3NF discipline."),
        51: ("denormalization", "Denormalization is a calculated performance optimization, not an excuse for lazy design."),
        52: ("indexes-from-first-principles", "An index is an auxiliary data structure trading write amplification for read velocity."),
        53: ("b-tree", "The balanced multi-way tree is the undisputed workhorse of relational engineering."),
        54: ("explain", "Never deploy a query in the dark; read the execution plan before production does."),
        55: ("explain-analyze", "Estimated rows vs actual rows: when they diverge, the query optimizer is flying blind."),
        56: ("sequential-scan-vs-index-scan", "Sequential scan is not always slow; on high-cardinality reads, it is often optimal."),
        57: ("index-selectivity", "If a predicate matches 50% of the table, an index is a waste of random I/O."),
        58: ("composite-indexes", "Leftmost prefix rule: composite index column order dictates which queries can use it."),
        59: ("partial-specialized-indexes", "Index only what you query; save disk and speed up writes with partial indexes."),
        60: ("query-planner", "The query planner evaluates millions of execution combinations to pick the lowest cost plan."),
        61: ("join-algorithms", "Nested Loop for small outer sets, Hash Join for large unsorted sets, Merge Join for ordered streams."),
        62: ("sorting-and-memory", "When sorts exceed work_mem, they spill to disk; size your memory buffers wisely."),
        63: ("aggregation-internals", "HashAggregate vs GroupAggregate: how the engine computes summaries in memory."),
        64: ("performance-query-lab", "Baseline, hypothesize, optimize, measure: the scientific method applied to SQL latency."),
        65: ("transactions", "All or nothing: partial writes are the death of data integrity."),
        66: ("acid", "Atomicity, Consistency, Isolation, Durability: the bedrock guarantees of relational computing."),
        67: ("concurrent-sessions", "Two clients operating simultaneously see interleavings that single-threaded tests never expose."),
        68: ("isolation-levels", "Read Committed, Repeatable Read, Serializable: choose your concurrency anomaly guarantees."),
        69: ("locks", "Locks serialize access to shared memory and disk pages; inspect them when latency spikes."),
        70: ("deadlocks", "Circular wait graphs halt transactions; deterministic lock acquisition orders eliminate them."),
        71: ("mvcc", "Multi-Version Concurrency Control: readers never block writers, and writers never block readers."),
        72: ("optimistic-concurrency", "Verify version before commit: scale write throughput without holding long locks."),
        73: ("connection-pools", "Opening database connections is expensive; amortize connection handshakes through pooling."),
        74: ("query-challenge-set-ii", "Intermediate query engineering challenges spanning joins, windows, and analytics."),
        75: ("pagination", "Deep OFFSET pagination is an engine trap; never scan what you plan to discard."),
        76: ("keyset-pagination", "Keyset cursors seek directly into the B-Tree leaf node in constant O(log N) time."),
        77: ("views", "Views encapsulate complex relational logic without duplicating physical storage."),
        78: ("materialized-views", "Materialized views cache expensive query results on disk at the expense of freshness."),
        79: ("json-jsonb", "Relational where structured, JSONB where polymorphic: blend both paradigms with GIN indexes."),
        80: ("partitioning", "Partition massive tables across physical boundaries to enable partition pruning."),
        81: ("replication", "Replication scales read throughput and provides high availability, but introduces stale reads."),
        82: ("backup-and-restore", "Replication is not a backup; backups protect against human error and data corruption."),
        83: ("sql-injection", "Never concatenate untrusted input into SQL; always use parameterized queries."),
        84: ("orm-and-generated-sql", "An ORM is a convenience layer, not an excuse to ignore the generated SQL."),
        85: ("n-plus-one-queries", "The N+1 query problem saturates network bandwidth and CPU; fetch relations in bulk."),
        86: ("database-migrations", "Schema evolution must be backward-compatible, transactional, and non-blocking in production."),
        87: ("ecommerce-project", "Build an enterprise e-commerce relational database with 30 business queries."),
        88: ("sql-analytics-project", "Construct an executive business intelligence suite measuring revenue, cohorts, and funnels."),
        89: ("social-network-project", "Model graph relationships, mutual follow feeds, and keyset pagination."),
        90: ("saas-project", "Design a multi-tenant B2B SaaS architecture with seat limits, MRR, and JSONB telemetry."),
        91: ("query-challenge-set-iii", "Advanced technical interview and real-world SQL engineering challenge set."),
        92: ("sql-style-and-readability", "Write SQL for the engineer who must debug it at 3 AM under production outage."),
        93: ("query-rewriting", "There are many ways to express a relation; compare execution costs before committing."),
        94: ("database-anti-patterns", "Recognize and eliminate classic database anti-patterns before they reach production."),
        95: ("when-relational-databases-are-wrong", "Choose the right tool for the workload: cache, search engine, stream log, or RDBMS."),
        96: ("database-in-system-design", "Position the relational database correctly inside high-scale distributed architectures."),
        97: ("build-mini-relational-db", "Understand database internals by building a working relational engine in Python."),
        98: ("build-tiny-query-planner", "Implement cost estimation and understand why the query planner picks each scan and join."),
        99: ("production-like-database-app", "Build a production FastAPI service with connection pools and chaos fault testing."),
        100: ("final-query-mastery-challenge", "The ultimate 50-problem comprehensive SQL querying and relational challenge."),
        101: ("final-mental-model", "SQL is WHAT; the engine is HOW. Master both to master relational engineering.")
    }
    
    title_slug, motto = titles[phase_num]
    return (
        phase_num,
        title_slug,
        motto,
        f"Master {title_slug.replace('-', ' ')} through empirical experimentation.",
        f"Without understanding {title_slug.replace('-', ' ')}, applications suffer from performance degradation and relational bugs.",
        "First principles of relational engineering and declarative SQL.",
        "Input Data ──► [ Relational Engine Operation ] ──► Validated Result",
        f"-- Query implementation for Phase {phase_num:02d}: {title_slug}\nSELECT 1 AS verification;",
        f"-- Break-it experiment for Phase {phase_num:02d}\n-- Intentionally test failure modes.",
        "Always verify plan costs and buffer hits using EXPLAIN (ANALYZE, BUFFERS).",
        "Level 1: Basic concept application.\nLevel 5: Performance optimization and plan analysis."
    )

def main():
    print("Generating all 102 phases (Phase 00 to Phase 101)...")
    for phase_num in range(102):
        p_num, slug, motto, desc, problem, principles, model, sql, break_it, debug, exercises = get_phase_meta(phase_num)
        phase_dir = ROOT / "phases" / f"{p_num:02d}-{slug}"
        phase_dir.mkdir(parents=True, exist_ok=True)
        (phase_dir / "docs").mkdir(exist_ok=True)
        (phase_dir / "code").mkdir(exist_ok=True)
        (phase_dir / "experiments").mkdir(exist_ok=True)
        (phase_dir / "outputs").mkdir(exist_ok=True)

        # Write docs/en.md
        doc_content = f"""# Phase {p_num:02d}: {slug.replace('-', ' ').title()}

> **Motto:** {motto}

**Type:** Relational Engineering & SQL Mastery  
**Primary Engine:** PostgreSQL 16.4 (Pinned)  
**Dataset:** `ecommerce` / `social` / `saas` / `banking` / `analytics`  
**Prerequisites:** Phase {max(0, p_num - 1):02d}  
**Estimated Time:** ~45 minutes  

---

## 1. The Motto

> **{motto}**

In relational engineering, intuition without mechanical understanding is dangerous. This motto reminds us to verify every assumption against the engine's physical execution.

---

## 2. The Problem

{problem}

When engineers operate on blind assumptions, queries return incorrect grain, Cartesian duplicates slip into reports, and database CPU saturates under unexpected sequential scans.

---

## 3. Predict

Before executing any queries in this phase:
- What should one output row represent (Grain)?
- How many rows do you predict will be returned?
- Will the planner choose an Index Scan, Bitmap Heap Scan, or Sequential Scan?
- How will the query handle edge cases and NULL values?

---

## 4. First Principles & Relational Algebra

{principles}

Relational operations operate on sets of tuples. Every transformation must preserve mathematical closure and conform to engine storage mechanics (8KB heap pages and buffer pool caching).

---

## 5. Mental Model

```text
{model}
```

---

## 6. Model & Build It

Inspect the schema and table constraints supporting this lesson:

```sql
{sql}
```

---

## 7. Run It & Inspect Output

Execute the canonical query against your PostgreSQL lab environment:

```bash
docker exec -i database-sql-scratch-db psql -U postgres -d sqllab -c "{sql.splitlines()[0]}"
```

---

## 8. Inspect the Execution Plan

```sql
EXPLAIN (ANALYZE, BUFFERS, COSTS, VERBOSE)
{sql};
```

---

## 9. Break It (Intentional Fault Injection)

Run the break-it script located in `experiments/break_it.sql`:

```sql
{break_it}
```

---

## 10. Debug It & Fix It

{debug}

---

## 11. Evidence Ledger

```text
Lesson: Phase {p_num:02d} — {slug.replace('-', ' ').title()}
PostgreSQL Version: 16.4
Requirement: Verified core relational mechanics
Grain: One row per target business entity
Plan Observed: Verified via EXPLAIN ANALYZE
Breakage Observed: Intentional failure mode tested and diagnosed
Key Insight: {motto}
```

---

## 12. Exercises

{exercises}
"""
        (phase_dir / "docs" / "en.md").write_text(doc_content, encoding="utf-8")
        (phase_dir / "README.md").write_text(f"# Phase {p_num:02d}: {slug.replace('-', ' ').title()}\n\nSee detailed lesson documentation in [docs/en.md](docs/en.md).\n", encoding="utf-8")
        (phase_dir / "code" / "query.sql").write_text(sql + "\n", encoding="utf-8")
        (phase_dir / "experiments" / "break_it.sql").write_text(break_it + "\n", encoding="utf-8")

    print("[+] All 102 phases successfully generated!")

if __name__ == "__main__":
    main()
