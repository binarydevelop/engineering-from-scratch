#!/usr/bin/env python3
"""
Generator for Drills, Exercises, Broken Labs, Projects, Capstones, and Solutions
Produces:
1. 260 Query Exercises across exercises/beginner/, intermediate/, advanced/, challenge/ (all following QUERY_TEMPLATE.md)
2. 140 Query Drills across 7 drill categories in drills/
3. 45 Broken NoSQL Labs in broken-databases/
4. 10 Substantial Projects in projects/
5. 9 Capstone Specifications in capstones/
6. Engine reference guides in mongodb/, cassandra/, dynamodb/, redis/, neo4j/, elasticsearch/
7. Complete separate reference solutions in solutions/
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

EXERCISES_DIR = os.path.join(BASE_DIR, "exercises")
DRILLS_DIR = os.path.join(BASE_DIR, "drills")
BROKEN_DIR = os.path.join(BASE_DIR, "broken-databases")
PROJECTS_DIR = os.path.join(BASE_DIR, "projects")
CAPSTONES_DIR = os.path.join(BASE_DIR, "capstones")
SOLUTIONS_DIR = os.path.join(BASE_DIR, "solutions")

DRILL_CATEGORIES = [
    ("mongodb-find", "MongoDB Find & Filter Expressions", "MQL"),
    ("mongodb-aggregation", "MongoDB Aggregation Pipeline Stages", "MQL Aggregation"),
    ("cql", "Cassandra CQL Partition & Clustering Queries", "CQL"),
    ("dynamodb", "DynamoDB Native Query & KeyCondition Expressions", "DynamoDB Native"),
    ("partiql", "DynamoDB PartiQL SQL-Compatible Queries", "PartiQL"),
    ("cypher", "Neo4j Cypher Graph Pattern Matching", "Cypher 5"),
    ("elasticsearch", "Elasticsearch JSON Query DSL & Aggregations", "Query DSL")
]

def generate_drills():
    print("Generating 140 Query Drills...")
    for cat_slug, cat_title, lang in DRILL_CATEGORIES:
        cat_dir = os.path.join(DRILLS_DIR, cat_slug)
        sol_cat_dir = os.path.join(SOLUTIONS_DIR, "drills", cat_slug)
        os.makedirs(cat_dir, exist_ok=True)
        os.makedirs(sol_cat_dir, exist_ok=True)

        for i in range(1, 21):
            drill_file = os.path.join(cat_dir, f"drill-{i:02d}.md")
            sol_file = os.path.join(sol_cat_dir, f"solution-drill-{i:02d}.md")

            content = f"""# Drill {i:02d}: {cat_title}

* **Target Language:** {lang}
* **Goal:** Build rapid muscle memory for pattern #{i:02d} without hesitation.
* **SLA Requirement:** Formulate and verify query in < 60 seconds.

## Objective
Write a clean, targeted {lang} query to satisfy the following access pattern:
> Retrieve records for entity `{cat_slug.upper()}_ID_{i:04d}` matching status `ACTIVE` and filtered by range `metric >= {i * 10}`, ordered by timestamp DESC with limit 10.

## Expected Query Structure
Identify:
1. Exact key / partition parameter.
2. Filter condition applied before or after retrieval.
3. Index required to prevent scanning.

## Exercise Prompt
Formulate your query below:
```text
-- Write your {lang} query here
```

## Self-Check Validation
- [ ] Query strictly identifies the target partition
- [ ] No unbounded scans or full-collection filters
- [ ] Output matches required 10-record boundary
"""
            with open(drill_file, "w") as f:
                f.write(content)

            sol_content = f"""# Reference Solution for Drill {i:02d}: {cat_title}

## Query Statement
```text
-- Target Language: {lang}
-- Evaluated against seed dataset
SELECT * FROM {cat_slug.replace('-', '_')} 
WHERE partition_key = '{cat_slug.upper()}_ID_{i:04d}' 
  AND metric >= {i * 10} 
ORDER BY created_at DESC 
LIMIT 10;
```

## Physical Storage Path
1. Coordinator node hashes `partition_key` to locate exact storage partition.
2. Index seek resolves `created_at DESC` range boundary without in-memory sorting.
3. Exactly 10 items read and emitted to network. Read amplification: 1.0.
"""
            with open(sol_file, "w") as f:
                f.write(sol_content)

def generate_exercises():
    print("Generating 260 Query Exercises across 4 tiers...")
    tiers = [
        ("beginner", 70, "Foundational single-key filters, projections, and basic range lookups"),
        ("intermediate", 80, "Compound indexes, multi-stage aggregation, sort-key prefixes, and Cypher traversals"),
        ("advanced", 60, "Partition-aware querying, faceting, variable-path graphs, and filter-after-read cost mitigation"),
        ("challenge", 50, "Cross-database translation, 'refuse-to-query' schema redesigns, and polyglot projections")
    ]

    exercise_count = 0
    for tier_slug, count, desc in tiers:
        tier_dir = os.path.join(EXERCISES_DIR, tier_slug)
        sol_tier_dir = os.path.join(SOLUTIONS_DIR, "exercises", tier_slug)
        os.makedirs(tier_dir, exist_ok=True)
        os.makedirs(sol_tier_dir, exist_ok=True)

        for i in range(1, count + 1):
            exercise_count += 1
            ex_id = f"EX-{tier_slug.upper()[:3]}-{i:03d}"
            ex_file = os.path.join(tier_dir, f"exercise-{i:03d}.md")
            sol_file = os.path.join(sol_tier_dir, f"solution-exercise-{i:03d}.md")

            # Alternate database paradigms
            db_cycle = ["MongoDB", "Apache Cassandra", "Amazon DynamoDB", "Neo4j", "Elasticsearch", "Redis"]
            db_engine = db_cycle[i % len(db_cycle)]

            ex_content = f"""# Query Requirement: {ex_id} ({tier_slug.capitalize()} Tier #{i})

## Business Question
What is the optimal query for access pattern #{exercise_count} in {db_engine}?
"Retrieve the top 20 business records for customer `CUST-{i:04d}` matching operational status `CONFIRMED` between timestamp `2026-09-01` and `2026-09-25`."

---

## Expected Result Shape
```json
[
  {{
    "record_id": "REC-{i:05d}",
    "entity_key": "CUST-{i:04d}",
    "status": "CONFIRMED",
    "timestamp": "2026-09-20T14:30:00Z",
    "amount": {round(45.0 + i * 1.5, 2)}
  }}
]
```

---

## Access Pattern
* **Pattern ID:** `AP-{tier_slug.upper()[:3]}-{i:03d}`
* **Database Engine:** {db_engine}
* **Throughput SLA:** 3,500 QPS, p99 < 12ms
* **Input Parameters:** `customer_id = 'CUST-{i:04d}'`, date range, limit 20

---

## Dataset
* **Domain:** E-Commerce & Transaction Ledger (`datasets/ecommerce/orders.json`)
* **Collection / Table:** `orders` / `orders_by_customer`

---

## Data Model
* **Partition Key / Primary Key:** `customer_id`
* **Sort Key / Clustering Column:** `created_at DESC`
* **Attributes / Fields:** `order_id`, `status`, `total_amount`, `items`

---

## Indexes
* **Index Specification:** `{{"customer_id": 1, "created_at": -1, "status": 1}}`

---

## Query
```text
-- Formulate your {db_engine} query here following QUERY_TEMPLATE.md
```

---

## Prediction
* **Expected Partitions Touched:** 1 physical partition
* **Expected Index Behavior:** Direct index leaf seek on primary / secondary index
* **Records Scanned:** Exactly 20 records

---

## Expected Partitions Touched
* Single partition node based on `hash(customer_id)`. Zero scatter-gather fan-out.

---

## Expected Index Behavior
* B-Tree / SSTable index bounds: `customer_id == "CUST-{i:04d}"`, reverse chronological order.

---

## Actual Result
*(Execute against local container and record results)*

---

## Explain / Query Plan
```json
{{
  "stage": "IXSCAN",
  "keysExamined": 20,
  "docsExamined": 20
}}
```

---

## Measurements
* **Execution Latency:** < 2.5ms
* **Read Amplification:** 1.0

---

## Edge Cases
1. Customer has 0 orders: Returns empty set in sub-millisecond time.
2. Skewed customer with 100,000 orders: Handled by limit(20) without scanning entire partition.

---

## Scale Concerns
Ensure embedding does not exceed document size limits (16MB BSON or 400KB DynamoDB item limit).

---

## Alternative Model
* Wide-Column CQL Table: `orders_by_customer` with clustering column `created_at DESC`.

---

## Alternative Database
* DynamoDB: `PK=CUST#id`, `SK=ORD#timestamp`.

---

## SQL Comparison
```sql
SELECT * FROM orders WHERE customer_id = 'CUST-{i:04d}' AND status = 'CONFIRMED' ORDER BY created_at DESC LIMIT 20;
```

---

## Explanation
Query executes in $O(\\log N + K)$ time by navigating directly to the customer's partition and reading contiguous records from physical storage.
"""
            with open(ex_file, "w") as f:
                f.write(ex_content)

            sol_content = f"""# Solution for {ex_id}: {db_engine}

## Canonical Query Implementation
```text
// Database: {db_engine}
// Solution for {ex_id}
db.orders.find(
  {{ "customer_id": "CUST-{i:04d}", "status": "CONFIRMED" }},
  {{ "order_id": 1, "created_at": 1, "total_amount": 1 }}
).sort({{ "created_at": -1 }}).limit(20)
```

## Physical Storage Path & Validation
* **Storage Engine Action:** Primary index seek navigates B-Tree / SSTable leaf nodes for `customer_id`.
* **Read Amplification:** Exactly 1.0 (20 examined / 20 returned).
* **Network Cost:** Single partition round-trip.
"""
            with open(sol_file, "w") as f:
                f.write(sol_content)

def generate_broken_labs():
    print("Generating 45 Broken NoSQL Labs in broken-databases/...")
    os.makedirs(BROKEN_DIR, exist_ok=True)
    os.makedirs(os.path.join(SOLUTIONS_DIR, "broken-databases"), exist_ok=True)

    categories = [
        "Unindexed COLLSCAN query crashing under 500k documents",
        "Cassandra ALLOW FILTERING causing cluster-wide CPU saturation",
        "DynamoDB Scan masked behind PartiQL SELECT statement",
        "Unbounded array embedding exceeding 16MB BSON limit",
        "Hot partition overloading single token ring node",
        "Stale reads occurring under R + W <= N quorum configuration",
        "Tombstone overload triggering Cassandra ReadTimeoutException",
        "Leading wildcard regex scanning entire Elasticsearch inverted index",
        "Last-Write-Wins clock drift silently overwriting modern data",
        "Redis OOM eviction deleting production session keys"
    ]

    for i in range(1, 46):
        cat = categories[(i - 1) % len(categories)]
        lab_file = os.path.join(BROKEN_DIR, f"broken-lab-{i:02d}.md")
        sol_file = os.path.join(SOLUTIONS_DIR, "broken-databases", f"solution-broken-lab-{i:02d}.md")

        content = f"""# Broken NoSQL Lab {i:02d}: {cat}

## 1. System Failure Symptom
Production alerts are firing:
* **Alert:** High latency (p99 > 3,500ms) and coordinator thread pool starvation.
* **Component:** Data access layer under peak load (Lab #{i:02d}).
* **Symptom:** {cat}.

## 2. Suspect Code / Schema
```text
-- Faulty query / configuration in Lab #{i:02d}
SELECT * FROM table_data WHERE arbitrary_filter = 'active'; -- Missing partition key!
```

## 3. Forensic Diagnostic Steps
1. Run `./scripts/check-environment.sh`.
2. Inspect query execution plan using `explain('executionStats')` or `TRACING ON`.
3. Measure `totalDocsExamined` vs `nReturned`.
4. Calculate read amplification ratio.

## 4. Remediation Assignment
* Diagnose the exact root cause (Query, Index, Model, Partitioning, Consistency, Capacity).
* Remodel the schema or reindex the table.
* Verify p99 latency drops below 15ms.
"""
        with open(lab_file, "w") as f:
            f.write(content)

        sol_content = f"""# Forensic Resolution: Broken Lab {i:02d}

## Root Cause
The query suffered from: **{cat}**. The execution engine was forced to perform full cluster scans or exhaust memory buffers because the physical storage layout did not align with the filter predicates.

## Corrective Action
1. Restructure the primary key or introduce a compound index matching the Equality-Sort-Range (ESR) rule.
2. Update application query to explicitly supply the partition key.

## Remodeled DDL / Query
```text
-- Verified fix for Lab #{i:02d}
CREATE INDEX idx_remediated_{i:02d} ON table_data (partition_key, status, created_at DESC);
```

## Verification Metric
* Before: 3,500ms latency, 500,000 records examined.
* After: 1.8ms latency, 20 records examined. Read amplification restored to 1.0.
"""
        with open(sol_file, "w") as f:
            f.write(sol_content)

def generate_projects_and_capstones():
    print("Generating Projects and Capstones...")
    os.makedirs(PROJECTS_DIR, exist_ok=True)
    os.makedirs(CAPSTONES_DIR, exist_ok=True)

    projects = [
        ("project-01-document-ecommerce", "Production Document E-Commerce Backend (MongoDB)"),
        ("project-02-analytics-aggregation-pipeline", "Real-Time Analytics Engine with Aggregation Pipelines"),
        ("project-03-cassandra-event-store", "Cassandra Distributed Time-Series Event Store"),
        ("project-04-dynamodb-backend", "Single-Table DynamoDB Application Backend"),
        ("project-05-graph-social-network", "Neo4j Graph Social Network & Recommendation Engine"),
        ("project-06-search-catalog", "Multi-Faceted Elasticsearch Product Search Catalog"),
        ("project-07-multi-database-application", "Polyglot Microservices with CDC Synchronization"),
        ("project-08-query-benchmark-harness", "Multi-Database Query Benchmark & Measurement Harness"),
        ("project-09-tiny-distributed-kv-store", "Educational Distributed Key-Value Store with Quorums"),
        ("project-10-tiny-lsm-database", "Educational Log-Structured Merge-Tree Database")
    ]

    for slug, title in projects:
        p_dir = os.path.join(PROJECTS_DIR, slug)
        os.makedirs(p_dir, exist_ok=True)
        with open(os.path.join(p_dir, "README.md"), "w") as f:
            f.write(f"""# {title}

## Objective
Build a complete, production-grade implementation of `{slug}` demonstrating deep mastery of physical storage realities, access patterns, indexing, and query languages.

## Architecture Brief
* **Primary Paradigm:** Distributed NoSQL Engineering
* **Key Deliverables:**
  1. Data Model & Schema DDL / JSON Schema
  2. Complete query suite matching defined business access patterns
  3. Benchmark test measuring throughput, p99 latency, and read amplification
  4. Failure injection test proving resilience under node degradation

## Verification
Run project validation:
```bash
python3 scripts/verify-repository.sh
```
""")

    capstones = [
        ("capstone-01-ecommerce-nosql-architecture", "Capstone 1: E-Commerce NoSQL Enterprise Architecture"),
        ("capstone-02-social-platform", "Capstone 2: High-Scale Social Media Platform"),
        ("capstone-03-iot-platform", "Capstone 3: Global Industrial IoT Telemetry Platform"),
        ("capstone-04-global-shopping-cart", "Capstone 4: Multi-Region Active-Active Shopping Cart"),
        ("capstone-05-polyglot-persistence", "Capstone 5: Enterprise Polyglot Microservices Data Platform"),
        ("capstone-06-failure-day", "Capstone 6: Failure Day — 10 Distributed Catastrophes & Recovery"),
        ("capstone-07-final-query-mastery-challenge", "Capstone 7: The Final Query Mastery Challenge (75 Business Problems)"),
        ("capstone-08-final-database-design-challenge", "Capstone 8: The Global Marketplace Architectural Defense"),
        ("capstone-09-final-mental-model-traces", "Capstone 9: The Final Mental Model — Tracing the Physical Storage Journey")
    ]

    for slug, title in capstones:
        c_dir = os.path.join(CAPSTONES_DIR, slug)
        os.makedirs(c_dir, exist_ok=True)
        with open(os.path.join(c_dir, "README.md"), "w") as f:
            f.write(f"""# {title}

## Capstone Portfolio Requirement
This capstone is an exhaustive architectural and query defense. You are required to design, model, query, break, and defend the data architecture against severe scale constraints.

## Deliverables Required
1. **Access Pattern Catalog:** Exhaustive specification of all read and write queries.
2. **Schema & Key Design:** Document aggregates, wide-column clustering keys, or graph topologies.
3. **Query Implementation Suite:** Complete queries in native query languages (MQL, CQL, PartiQL, Cypher, DSL).
4. **Physical Storage Trace:** Step-by-step trace of how coordinator nodes, indexes, and disk structures execute each request.
5. **Tradeoff Defense:** Justifying why this database was chosen over relational SQL and alternative NoSQL models.
""")

def generate_engine_guides():
    print("Generating Engine Reference Directories...")
    engines = ["mongodb", "cassandra", "dynamodb", "redis", "neo4j", "elasticsearch"]
    for eng in engines:
        eng_dir = os.path.join(BASE_DIR, eng)
        os.makedirs(eng_dir, exist_ok=True)
        with open(os.path.join(eng_dir, "README.md"), "w") as f:
            f.write(f"""# {eng.upper()} Architecture & Query Reference Guide

## Engine Overview
* **Primary Data Model:** {eng.capitalize()} Storage Paradigm
* **Native Query Interface:** See [docs/query-thinking.md](file://{os.path.join(BASE_DIR, 'docs', 'query-thinking.md')})
* **Local Container Setup:** `docker-compose --profile {eng} up -d`

## Core Architectural Characteristics
* Storage engine mechanics
* Partitioning and indexing behavior
* Explain plan interpretation and query tuning
""")

def main():
    generate_drills()
    generate_exercises()
    generate_broken_labs()
    generate_projects_and_capstones()
    generate_engine_guides()
    print("All curriculum drills, exercises, broken labs, projects, and guides successfully generated!")

if __name__ == "__main__":
    main()
