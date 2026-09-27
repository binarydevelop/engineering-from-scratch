#!/usr/bin/env python3
"""
build_curriculum_part5.py - Generates Phases 56 to 68 for elasticsearch-from-scratch.
Covers Caching, Deep Pagination, Point-in-Time, Sorting, Slow Queries, Profiling,
Backpressure, Memory, Disk Watermarks, Snapshots, ILM, Time-Series, and Ingest Pipelines.
"""

import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PHASES_DIR = os.path.join(BASE_DIR, "phases")

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    if path.endswith(".sh") or path.endswith(".py"):
        os.chmod(path, 0o755)

def evidence_template(phase_title, phase_num):
    return f"""# Evidence Log: Phase {phase_num:02d} - {phase_title}

Date: 2026-09-23
Elasticsearch Version: 8.17.0
Lucene Version: 9.12.0
Working Directory: phases/{phase_num:02d}-{phase_title.lower().replace(' ', '-').replace('/', '-')}

## Prediction
Before executing the experiment, record your hypothesis here:

## Commands Executed
```bash
./experiments/run_experiment.sh
```

## Important Terminal Output
```text
```

## Measurements
* Metric 1:
* Metric 2:

## What Actually Happened?

## What Did I Intentionally Break?

## How Did I Diagnose It?

## How Did I Recover?

## Explain the Concept in My Own Words:
"""

def generate_phases_56_to_68():
    phases = [
        (56, "Search Caching",
         "Caches store bitsets and aggregation results, not whole HTTP payloads: understand Node Query Cache and Shard Request Cache.",
         """# Lesson 56.1: Search Caching

## Motto
"Caches store bitsets and aggregation results, not whole HTTP payloads: understand Node Query Cache and Shard Request Cache."

## Problem
Engineers frequently assume Elasticsearch caches entire HTTP search responses like Redis or Varnish. When they see identical full-text queries taking 20ms every time, they wonder why "the cache is not working".

## Prediction
Does Elasticsearch cache the results of scored full-text queries, or only deterministic filter bitsets?

## Why this matters
Elasticsearch has sophisticated caching tiers. Knowing what is eligible for caching allows architecting queries for maximum cache reuse.

## First principles
The Two Primary Caches:
1. **Node Query Cache (Filter Cache):** Caches the matching document bitsets (Roaring Bitmaps) of clauses executed in **filter context**.
   * Only caches filters that run frequently (tracked by a frequency heuristic).
   * Per-segment bitset: if a segment does not change, its cached bitset remains valid forever!
2. **Shard Request Cache:** Caches local shard-level results of queries with `size: 0` (pure aggregations).
   * Automatically invalidated as soon as the shard is refreshed.

## Mental model
```text
Filter: "category: electronics"
  Segment _0 (Immutable) ──► Evaluated once ──► Bitset [1, 0, 1, 1...] cached in RAM!
  Next 1,000 queries ────► Bitwise AND in 0.001 ms! Zero Lucene index reads!
```

## Build it
See `code/filter_cache_sim.py` demonstrating bitset reuse in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/56-search-caching/experiments/run_experiment.sh
```

## Inspect it
Check cache hit and miss stats across nodes:
```bash
curl -s "http://localhost:9200/_nodes/stats/indices/query_cache,request_cache?pretty"
```

## Measure it
Measure latency of a repeated filter query on first run vs tenth run.

## Break it
Put non-deterministic terms like `now` in filters (`created_at >= now-1m`). Because `now` changes every millisecond, each query is unique and the cache misses 100% of the time!

## Recover it
Round timestamps using date math: `created_at >= now-1m/m`.

## Modify it
Explicitly enable or disable request caching: `"request_cache": true`.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does the Node Query Cache cache bitsets per Lucene segment rather than per index?
2. What invalidates the Shard Request Cache on a shard? (A refresh).

## Guarantees
* Unchanged segments retain their cached filter bitsets across query executions.

## Non-guarantees
* Scored queries in query context (`must`, `should`) are never cached in the Node Query Cache.

## When to use this
* Reusable categorical filters, status flags, and recurring dashboards.

## When not to use this
* Queries with high-precision unique timestamps (`now` without rounding).

## What comes next
In Phase 57, we contrast `from + size` with `search_after` for Deep Pagination.
""",
"""#!/usr/bin/env python3

class BitsetCacheSim:
    def __init__(self):
        self.cache = {}
        self.hits = 0
        self.misses = 0

    def query_filter(self, segment_id, filter_term, doc_stream):
        key = (segment_id, filter_term)
        if key in self.cache:
            self.hits += 1
            return self.cache[key]
        self.misses += 1
        # Build bitset
        bitset = [1 if d.get("category") == filter_term else 0 for d in doc_stream]
        self.cache[key] = bitset
        return bitset

if __name__ == "__main__":
    docs = [{"id": i, "category": "tech" if i % 2 == 0 else "home"} for i in range(100)]
    c = BitsetCacheSim()
    print("Executing query 10 times for category='tech':")
    for _ in range(10):
        _ = c.query_filter("seg_0", "tech", docs)
    print(f"Results: Hits={c.hits}, Misses={c.misses} (First query built bitset, next 9 were instant cache hits!)")
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 56: Search Caching Mechanics ==="
python3 phases/56-search-caching/code/56_search_caching.py
"""),

        (57, "Pagination",
         "from + size is O(N) in depth: deep pagination forces every shard to score and sort N documents only to discard them.",
         """# Lesson 57.1: Pagination

## Motto
"from + size is O(N) in depth: deep pagination forces every shard to score and sort N documents only to discard them."

## Problem
A user jumps to Page 1,000 using `{"from": 10000, "size": 10}`. On an index with 5 shards, each of the 5 shards must collect, score, and sort 10,010 documents (50,050 total candidates), send them to the coordinator, and the coordinator sorts 50,050 items only to return 10. The coordinator runs out of memory and crashes!

## Prediction
What default safety error does Elasticsearch return if `from + size > 10000`?

## Why this matters
Deep pagination is an exponential killer of search clusters. Understanding `search_after` is mandatory for scalable pagination.

## First principles
* **`from + size`:** Offsets results. Cost is $O(\text{from} + \text{size})$. Discards everything before `from`.
* **`index.max_result_window`:** Defaults to **10,000**. Protects the cluster from deep paging crashes.
* **`search_after`:** Cursor-based pagination. Uses the sort values of the last document on the current page to start the next page in $O(\text{size})$ time, without skipping!

## Mental model
```text
from: 10,000, size: 10:
  Coordinator sorts 10,010 documents ──► Discards first 10,000 ──► Extreme Waste!

search_after: [149.99, "doc_999"]:
  Shards jump directly to items WHERE (price <= 149.99 AND id > doc_999) ──► Reads ONLY 10 items!
```

## Build it
See `code/deep_pagination_bench.py` contrasting `from` offsets vs cursor iteration in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/57-pagination/experiments/run_experiment.sh
```

## Inspect it
Test `from + size` up to the safety window:
```bash
curl -X POST http://localhost:9200/products_phase06/_search -H "Content-Type: application/json" -d '{
  "from": 10001,
  "size": 10
}'
```
Read the `illegal_argument_exception`: `"Result window is too large..."`.

## Measure it
Compare latency: page 1 vs page 500 using `from` vs `search_after`.

## Break it
Increase `index.max_result_window: 1000000` and query page 50,000 to watch JVM heap exhaustion.

## Recover it
Keep `max_result_window: 10000` and implement cursor pagination using `search_after`.

## Modify it
Use `search_after` with sort on `["price", "_id"]`:
```json
{
  "size": 10,
  "sort": [ { "price": "desc" }, { "_id": "asc" } ],
  "search_after": [ 149.99, "1042" ]
}
```

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does `from: 50000, size: 10` force every shard to score 50,010 documents?
2. Why must `search_after` always include a tie-breaker field (like `_id`) in the sort?

## Guarantees
* `search_after` executes page $N$ with the same constant speed as page 1.

## Non-guarantees
* `search_after` does not allow jumping directly to arbitrary arbitrary distant page numbers (e.g. "Jump to page 47").

## When to use this
* Infinite scroll feeds, web scrapers, data exports, and deep result browsing.

## When not to use this
* Simple top-10 search results where `from: 0` is all that is needed.

## What comes next
In Phase 58, we stabilize pagination across concurrent updates using Point in Time (PIT).
""",
"""#!/usr/bin/env python3
import time

def simulate_from_size(data, from_offset, size):
    # Simulates sorting and discarding
    sorted_data = sorted(data, key=lambda x: x["val"], reverse=True)
    return sorted_data[from_offset:from_offset + size]

def simulate_search_after(data, last_val, last_id, size):
    # Direct cursor filtering
    candidates = [d for d in data if (d["val"] < last_val) or (d["val"] == last_val and d["id"] > last_id)]
    sorted_candidates = sorted(candidates, key=lambda x: (-x["val"], x["id"]))
    return sorted_candidates[:size]

if __name__ == "__main__":
    items = [{"id": i, "val": 100000 - i} for i in range(50000)]
    t0 = time.perf_counter()
    p1 = simulate_from_size(items, from_offset=40000, size=10)
    t_from = (time.perf_counter() - t0) * 1000

    t0 = time.perf_counter()
    p2 = simulate_search_after(items, last_val=60001, last_id=39999, size=10)
    t_cursor = (time.perf_counter() - t0) * 1000

    print(f"Deep Paging (from=40000): {t_from:.2f} ms")
    print(f"Cursor (search_after):    {t_cursor:.2f} ms")
    print(f"Cursor pagination was {t_from / t_cursor:.1f}x faster!")
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 57: Deep Pagination vs search_after ==="
python3 phases/57-pagination/code/57_pagination.py
"""),

        (58, "Point in Time",
         "Point-in-Time freezes a lightweight search view of segments, preventing documents from shifting or disappearing during pagination.",
         """# Lesson 58.1: Point in Time (PIT)

## Motto
"Point-in-Time freezes a lightweight search view of segments, preventing documents from shifting or disappearing during pagination."

## Problem
You are paginating through 50,000 results using `search_after`. While the user is browsing page 3, background updates and deletions insert new items and delete old ones. The document IDs shift, causing duplicate hits on page 4 or missed records entirely!

## Prediction
Can you freeze a consistent snapshot view of an index for search queries without copying the underlying data?

## Why this matters
The **Point in Time (PIT)** API (Elasticsearch 8.x) locks the set of Lucene segments participating in search. It guarantees consistent pagination even while the index is actively being modified.

## First principles
* **Lightweight Snapshot:** A PIT does not duplicate data; it simply retains open file handles to existing immutable segments, preventing the merge policy from deleting them until the PIT expires.
* Combines with `search_after` for consistent, reliable pagination.
* Must be closed explicitly (`DELETE /_pit`) when finished to release disk space.

## Mental model
```text
Live Index:
  Segments constantly refreshing, updating, and merging.

Point-in-Time (PIT Token):
  Retains references to [Segment _0, Segment _1] as they existed at Time T0.
  Subsequent updates do not alter this PIT search view!
```

## Build it
See `code/pit_simulation.py` simulating consistent read snapshots in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/58-point-in-time/experiments/run_experiment.sh
```

## Inspect it
Open a Point in Time:
```bash
PIT_ID=$(curl -s -X POST "http://localhost:9200/products_phase06/_pit?keep_alive=1m" | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
echo "Opened PIT ID: $PIT_ID"
```
Query using the PIT:
```bash
curl -X POST http://localhost:9200/_search -H "Content-Type: application/json" -d "{
  \"size\": 5,
  \"pit\": { \"id\": \"$PIT_ID\", \"keep_alive\": \"1m\" }
}"
```
Close the PIT:
```bash
curl -X DELETE http://localhost:9200/_pit -H "Content-Type: application/json" -d "{\"id\": \"$PIT_ID\"}"
```

## Measure it
Verify query consistency: index new documents while paginating with PIT and confirm they do NOT appear in the PIT view.

## Break it
Open 1,000 PITs with `keep_alive: 24h` and never close them. Segment merging cannot reclaim deleted documents, causing disk usage to swell!

## Recover it
Delete lingering PITs via `DELETE /_pit` with `{"id": "_all"}`.

## Modify it
Combine PIT with `search_after` for zero-drift infinite scrolling.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does keeping a PIT open prevent disk space from being reclaimed after segment merges?
2. What is the difference between a Point-in-Time view and a database transaction?

## Guarantees
* A PIT view is completely frozen and consistent across multiple sequential search requests.

## Non-guarantees
* A PIT is not an ACID transaction (it is read-only).

## When to use this
* Large-scale data exports, audit pagination, and reliable cursor browsing.

## When not to use this
* Quick single-page queries.

## What comes next
In Phase 59, we compare Relevance Sorting with Field Sorting on Doc Values.
""",
"""#!/usr/bin/env python3

class PITSimulator:
    def __init__(self, current_data):
        # Freezes references to segments at this instant
        self.frozen_data = list(current_data)

    def search(self, query):
        return [d for d in self.frozen_data if query in d["text"]]

if __name__ == "__main__":
    live_database = [{"id": 1, "text": "initial item 1"}, {"id": 2, "text": "initial item 2"}]
    print("Opening Point In Time (PIT)...")
    pit = PITSimulator(live_database)

    print("Concurrent Write: Appending item 3 to live database...")
    live_database.append({"id": 3, "text": "newly added item 3"})

    print(f"Live database now has: {len(live_database)} items.")
    print(f"PIT frozen search sees: {len(pit.search('item'))} items! (Completely isolated from concurrent writes)")
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 58: Point in Time (PIT) ==="
python3 phases/58-point-in-time/code/58_point_in_time.py
"""),

        (59, "Sorting",
         "Relevance sort evaluates BM25; field sorting bypasses BM25 completely to read columnar doc values.",
         """# Lesson 59.1: Sorting

## Motto
"Relevance sort evaluates BM25; field sorting bypasses BM25 completely to read columnar doc values."

## Problem
When users sort by `price: asc` or `date: desc`, calculating BM25 relevance scores for millions of documents is pure wasted CPU.

## Prediction
Does sorting by an explicit field disable BM25 relevance scoring by default?

## Why this matters
Sorting by non-relevance criteria can be drastically optimized using Lucene's index-sorting and columnar doc values.

## First principles
* **Relevance Sort (`_score: desc`):** BM25 score must be computed for every candidate document.
* **Field Sort (`price: asc`):** Score calculation is bypassed completely (`_score: null`). Shards read contiguous values directly from columnar Doc Values.
* **Index Sorting:** Pre-sorting documents on disk at segment-write time (e.g. sort segment by `created_at desc`). Allows queries sorting by `created_at` to terminate early after reading the first $K$ hits!

## Mental model
```text
Relevance Sort:
  Query ──► Compute BM25 for all 100k hits ──► Sort by score ──► Return top 10

Field Sort on Doc Values:
  Query ──► Read Price column directly from disk cache ──► Return top 10 (Zero BM25 math!)

Index Sorted Segment:
  Segment pre-sorted by date ──► Read first 10 items off disk ──► EARLY TERMINATION! (Instant!)
```

## Build it
See `code/sorting_bench.py` demonstrating doc values sort vs scored sort in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/59-sorting/experiments/run_experiment.sh
```

## Inspect it
Sort by price and inspect the response:
```bash
curl -X POST http://localhost:9200/products_phase06/_search -H "Content-Type: application/json" -d '{
  "query": { "match_all": {} },
  "sort": [{ "price": "asc" }]
}'
```
Notice `_score: null` in the returned hits!

## Measure it
Compare query latency: sorting by `_score` vs sorting by an indexed numeric field.

## Break it
Sort on an analyzed `text` field without a keyword subfield:
`"Field [title] of type [text] does not support sorting. Use keyword multi-field."`

## Recover it
Sort on `title.keyword` backed by doc values.

## Modify it
Configure index-time sorting in index settings (`"index.sort.field": "created_at"`).

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does explicit field sorting set `_score: null` by default?
2. How does Index Sorting allow early termination during query execution?

## Guarantees
* Field sorting on doc values scales independently of document text length.

## Non-guarantees
* Sorting on unindexed or dynamic scripting expressions will degrade performance.

## When to use this
* Filtering products by price, news by timestamp, or logs by severity.

## When not to use this
* Pure relevance search where user intent depends on term match quality.

## What comes next
In Phase 60, we diagnose and mitigate Slow Queries.
""",
"""#!/usr/bin/env python3
import time

def benchmark_sorting(n=100000):
    # Simulated documents
    docs = [{"id": i, "price": (i * 37) % 1000, "score": (i * 17) % 100 / 10.0} for i in range(n)]

    # 1. Sort by score
    t0 = time.perf_counter()
    s1 = sorted(docs, key=lambda x: x["score"], reverse=True)[:10]
    t_score = (time.perf_counter() - t0) * 1000

    # 2. Sort by price
    t0 = time.perf_counter()
    s2 = sorted(docs, key=lambda x: x["price"])[:10]
    t_field = (time.perf_counter() - t0) * 1000

    return t_score, t_field

if __name__ == "__main__":
    t_s, t_f = benchmark_sorting(100000)
    print(f"Sort 100,000 items by score: {t_s:.2f} ms")
    print(f"Sort 100,000 items by price: {t_f:.2f} ms")
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 59: Field Sorting vs Relevance ==="
python3 phases/59-sorting/code/59_sorting.py
"""),

        (60, "Slow Queries",
         "Slow queries are caused by predictable anti-patterns: leading wildcards, script scoring, deep paging, and giant aggs.",
         """# Lesson 60.1: Slow Queries

## Motto
"Slow queries are caused by predictable anti-patterns: leading wildcards, script scoring, deep paging, and giant aggs."

## Problem
A search endpoint intermittently spikes from 10ms to 8,000ms, causing cascading timeouts in upstream microservices. How do you identify which specific queries are responsible?

## Prediction
Can you configure Elasticsearch to automatically log any query that takes longer than 200ms to a dedicated slow-log file?

## Why this matters
Slow queries block search thread pool queues. Finding and optimizing slow queries is the core operational duty of search engineering.

## First principles
The Four Horsemen of Slow Queries:
1. **Leading Wildcards / Unanchored Regex:** `*search*` scans the entire term dictionary.
2. **Deep Pagination:** `from: 50000` forces massive coordinator sorting.
3. **High-Cardinality Deep Aggregations:** Combinatorial explosion of bucket allocations.
4. **Painless Script Filters:** Running runtime scripts on every document bypasses Lucene indexes.
* **Search Slow Log:** Automatically records slow queries exceeding configurable latency thresholds (`warn`, `info`, `debug`, `trace`).

## Mental model
```text
Client Query ──► Executes on Shard
                        │
                [ Query took 450ms ]
                        │
              Is 450ms > threshold (200ms)?
                        │
                        ▼ YES
            Append full query JSON & shard details
            to 'elasticsearch_index_search_slowlog.log'!
```

## Build it
See `code/slow_query_detector.py` analyzing query complexity patterns in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/60-slow-queries/experiments/run_experiment.sh
```

## Inspect it
Configure dynamic slow log thresholds on an index:
```bash
curl -X PUT http://localhost:9200/products_phase06/_settings -H "Content-Type: application/json" -d '{
  "index.search.slowlog.threshold.query.warn": "200ms",
  "index.search.slowlog.threshold.query.info": "50ms"
}'
```

## Measure it
Run an expensive wildcard query and inspect slow log output.

## Break it
Execute a regex query with multiple wildcards across millions of documents to trigger slow logs.

## Recover it
Replace slow wildcards with `wildcard` field types or edge n-grams.

## Modify it
Set `index.indexing.slowlog.threshold.index.warn` to audit slow write operations.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does a Painless script filter execute slower than an equivalent Lucene boolean query?
2. What information does the Elasticsearch search slow log capture?

## Guarantees
* Slow logs provide an exact audit trail of offending queries and their execution times.

## Non-guarantees
* Slow logs record slow queries after they complete; they do not automatically cancel them.

## When to use this
* Production query auditing and latency SLA enforcement.

## When not to use this
* Setting slowlog thresholds to `0ms` in high-QPS production (will flood disk with logging I/O).

## What comes next
In Phase 61, we profile queries using the Search Profiling API.
""",
"""#!/usr/bin/env python3

def analyze_query_risk(query_json):
    risks = []
    q_str = str(query_json)
    if ".*" in q_str or "*?" in q_str:
        risks.append("CRITICAL: Leading wildcard or broad regex detected (Dictionary scan).")
    if query_json.get("from", 0) > 5000:
        risks.append("WARNING: Deep pagination detected (Coordinator sorting penalty).")
    if "script" in q_str:
        risks.append("WARNING: Scripting query detected (Bypasses Lucene inverted index).")
    return risks

if __name__ == "__main__":
    sample_query = {
        "from": 8000,
        "size": 10,
        "query": {"wildcard": {"title": "*phone*"}}
    }
    print("Analyzing Query for Performance Risks:")
    detected = analyze_query_risk(sample_query)
    for d in detected:
        print("  -", d)
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 60: Slow Queries & Diagnostics ==="
python3 phases/60-slow-queries/code/60_slow_queries.py
"""),

        (61, "Search Profiling",
         "The profile API is a microsecond x-ray: dissect Lucene query timing, Lucene scorers, and shard-level bottlenecks.",
         """# Lesson 61.1: Search Profiling

## Motto
"The profile API is a microsecond x-ray: dissect Lucene query timing, Lucene scorers, and shard-level bottlenecks."

## Problem
Your query is slow, but you do not know *which specific clause* is causing the delay. Is it the boolean `must`, the geo filter, the phrase match, or the aggregation?

## Prediction
Can Elasticsearch break down query execution time per Lucene component (e.g. `TermQuery`, `BooleanQuery`, `PointRangeQuery`) down to nanoseconds?

## Why this matters
The `_profile` API breaks open the black box. It measures exact execution time for every Lucene query component across every shard.

## First principles
Profile breakdown fields:
* `type`: The underlying Lucene class (e.g. `TermQuery`, `BlockMaxConjunctionScorer`).
* `time_in_nanos`: Exact duration spent in that component.
* `breakdown`:
  * `create_weight`: Building query scoring weight.
  * `build_scorer`: Initializing posting iterators.
  * `next_doc`: Advancing iterator across matching documents.
  * `score`: Computing BM25 score.
  * `match`: Testing candidate match.

## Mental model
```text
Profile Output Tree:
BooleanQuery: 12.4ms
  ├── TermQuery (title: wireless): 2.1ms (score: 1.2ms, next_doc: 0.8ms)
  └── PointRangeQuery (price: [0 TO 100]): 0.3ms (BKD tree evaluation)
```

## Build it
See `code/profile_parser.py` parsing and summarizing verbose profile responses into readable tables in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/61-search-profiling/experiments/run_experiment.sh
```

## Inspect it
Run a search with `"profile": true`:
```bash
curl -X POST http://localhost:9200/products_phase06/_search -H "Content-Type: application/json" -d '{
  "profile": true,
  "query": {
    "bool": {
      "must": [{ "match": { "title": "keyboard" } }],
      "filter": [{ "term": { "category": "furniture" } }]
    }
  }
}'
```

## Measure it
Compare nanoseconds spent in `score` vs `next_doc`.

## Break it
Run `"profile": true` in production during peak load: profiling instruments every Lucene method call and can slow down queries by 2x to 5x!

## Recover it
Only use `profile: true` during development, testing, and isolated staging environments.

## Modify it
Inspect aggregation profiling: `profile.shards[].aggregations`.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does running `"profile": true` add significant execution overhead to a query?
2. What does high `next_doc` time indicate compared to high `score` time?

## Guarantees
* Profiling reveals exact nanosecond execution times for every Lucene sub-query.

## Non-guarantees
* The profile numbers reflect execution with profiling overhead attached, not clean production speed.

## When to use this
* Query optimization, dissecting complex boolean trees, and comparing query rewrite strategies.

## When not to use this
* Production customer traffic.

## What comes next
In Phase 62, we study Indexing Backpressure and queue saturation.
""",
"""#!/usr/bin/env python3

def parse_profile_sample(sample_profile):
    queries = sample_profile.get("shards", [])[0].get("searches", [])[0].get("query", [])
    report = []
    for q in queries:
        report.append({
            "type": q.get("type"),
            "description": q.get("description"),
            "time_ms": round(q.get("time_in_nanos", 0) / 1_000_000, 3)
        })
    return report

if __name__ == "__main__":
    mock_profile = {
        "shards": [{
            "searches": [{
                "query": [
                    {"type": "TermQuery", "description": "title:keyboard", "time_in_nanos": 4200000},
                    {"type": "PointRangeQuery", "description": "price:[50 TO 150]", "time_in_nanos": 800000}
                ]
            }]
        }]
    }
    parsed = parse_profile_sample(mock_profile)
    print("Parsed Lucene Query Profile:")
    for p in parsed:
        print(f"  {p['type']:20s} | {p['description']:25s} | Time: {p['time_ms']} ms")
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 61: Search Profiling ==="
python3 phases/61-search-profiling/code/61_search_profiling.py
"""),

        (62, "Indexing Backpressure",
         "Search clusters have finite write capacity: when bulk queues fill, client requests must back off.",
         """# Lesson 62.1: Indexing Backpressure

## Motto
"Search clusters have finite write capacity: when bulk queues fill, client requests must back off."

## Problem
During peak traffic, ingestion workers submit bulk batches at 100,000 docs/sec, but disk write speed on data nodes caps out at 30,000 docs/sec. The cluster thread pool write queue fills up, and Elasticsearch begins returning HTTP 429 Too Many Requests (`EsRejectedExecutionException`).

## Prediction
What happens if clients ignore HTTP 429 errors and immediately retry at full speed?

## Why this matters
Elasticsearch is not an unbounded message broker like Kafka. It uses fixed-capacity thread pool queues. Responding to backpressure with exponential backoff prevents cluster crashes.

## First principles
* **Write Thread Pool:** Fixed number of worker threads (typically equal to CPU cores).
* **Write Queue:** Fixed-size queue (default **10,000** tasks).
* When queue is full, new requests are rejected with **HTTP 429** (`EsRejectedExecutionException`).
* Clients must implement **Exponential Backoff with Jitter**.

## Mental model
```text
Client Workers ──► Submitting 100k docs/sec
                         │
        ┌────────────────┴────────────────┐
        ▼                                 ▼
Write Threads (8 cores)           Write Queue (Capacity: 10,000)
(Pinned at 100% CPU)              (Full! 10,000 tasks waiting!)
                                          │
                                          ▼
                               HTTP 429 Too Many Requests!
                               (Client MUST back off!)
```

## Build it
See `code/backoff_simulator.py` demonstrating exponential backoff with jitter in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/62-indexing-backpressure/experiments/run_experiment.sh
```

## Inspect it
Monitor write queue depth and rejections:
```bash
curl -s "http://localhost:9200/_cat/thread_pool/write?v&h=node_name,name,active,queue,rejected,completed"
```

## Measure it
Measure retry latency and success rate during induced queue saturation.

## Break it
Launch 50 parallel Python processes submitting massive bulk payloads to induce HTTP 429 rejections.

## Recover it
Implement client retry logic:
$$\text{sleep} = \min(\text{max\_sleep}, \text{base} \times 2^{\text{attempt}}) \pm \text{jitter}$$

## Modify it
Inspect ingest node backpressure metrics: `node_stats.indexing.throttle_time_in_millis`.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does Elasticsearch reject writes with HTTP 429 instead of expanding its queue infinitely in memory?
2. What is "jitter" and why is it critical when retrying after backpressure?

## Guarantees
* Fixed write queues protect the JVM from running out of heap memory under write floods.

## Non-guarantees
* Elasticsearch does not buffer rejected writes for you; the client is responsible for retrying.

## When to use this
* Every production ingestion pipeline, Kafka consumer, and log shipper.

## When not to use this
* Low-volume systems where write queue saturation is physically impossible.

## What comes next
In Phase 63, we analyze JVM Heap and Operating System Memory.
""",
"""#!/usr/bin/env python3
import time
import random

def retry_with_backoff(operation_fn, max_retries=5, base_delay=0.1, max_delay=2.0):
    for attempt in range(max_retries):
        try:
            return operation_fn(attempt)
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            # Exponential backoff + full jitter
            delay = min(max_delay, base_delay * (2 ** attempt))
            jitter = random.uniform(0, delay)
            print(f"  Attempt {attempt + 1} rejected ({e}). Backing off for {jitter:.3f}s...")
            time.sleep(jitter)

if __name__ == "__main__":
    def flaky_write(attempt):
        if attempt < 2:
            raise RuntimeError("HTTP 429: EsRejectedExecutionException (Write Queue Full)")
        return "HTTP 200 OK: Bulk Indexed Successfully"

    print("Simulating Client-Side Retry with Exponential Backoff & Jitter:")
    result = retry_with_backoff(flaky_write)
    print("Final Result:", result)
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 62: Indexing Backpressure & Retries ==="
python3 phases/62-indexing-backpressure/code/62_indexing_backpressure.py
"""),

        (63, "Heap and Memory",
         "Never give all RAM to JVM heap: 50% belongs to heap (max 31GB), 50% belongs to OS page cache for Lucene.",
         """# Lesson 63.1: Heap and Memory

## Motto
"Never give all RAM to JVM heap: 50% belongs to heap (max 31GB), 50% belongs to OS page cache for Lucene."

## Problem
An administrator deploys an Elasticsearch node on a 64 GB RAM server and sets `-Xmx62g`, assuming more heap equals more performance. Within hours, search queries take 15 seconds and disk I/O thrashes!

## Prediction
Why does giving 62 GB of a 64 GB machine to JVM heap destroy search performance?

## Why this matters
Lucene is NOT a Java program that keeps everything in objects. Lucene relies on the **Operating System Page Cache** to memory-map immutable segment files.

## First principles
The Golden Memory Rule:
* **Max 50% to JVM Heap:** Leave at least 50% of physical RAM free for the OS page cache!
* **Max 31 GB Heap:** Never exceed ~31 GB (the threshold where JVM Compressed OOPs or Ordinary Object Pointers are disabled). Crossing 32 GB switches from 32-bit compressed pointers to 64-bit pointers, wasting gigabytes of RAM on pointer padding!

## Mental model
```text
64 GB RAM Machine:
┌───────────────────────────────────────┬───────────────────────────────────────┐
│ JVM Heap: 30 GB (-Xms30g -Xmx30g)     │ OS Page Cache: 34 GB                  │
├───────────────────────────────────────┼───────────────────────────────────────┤
│ - Cluster State                       │ - Lucene Segments (.doc, .tim)        │
│ - Index Buffers                       │ - Doc Values (.dvd) for sorting & aggs│
│ - Short-lived query aggregations      │ - Ultra-fast memory-mapped disk I/O   │
└───────────────────────────────────────┴───────────────────────────────────────┘
```

## Build it
See `code/compressed_oops_calc.py` calculating pointer overhead above 32GB in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/63-heap-and-memory/experiments/run_experiment.sh
```

## Inspect it
Check JVM heap usage and compressed pointers on your node:
```bash
curl -s "http://localhost:9200/_nodes/stats/jvm?pretty" | grep -A 10 "mem"
```

## Measure it
Inspect heap percent and garbage collector activity via `_cat/nodes?v&h=name,heap.percent,ram.percent`.

## Break it
Simulate high heap pressure by setting `-Xms128m -Xmx128m` and running an expensive query. Observe rapid GC pauses.

## Recover it
Configure balanced memory settings: `-Xms512m -Xmx512m` for lab, up to 30GB for production.

## Modify it
Inspect GC logs for Stop-The-World pause durations.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does allocating 33 GB of heap give you LESS usable memory than allocating 31 GB?
2. What role does the OS page cache play in Lucene search execution?

## Guarantees
* Compressed OOPs keep 64-bit JVM object references 32-bits wide below ~31 GB.

## Non-guarantees
* Having 31 GB of heap does not prevent OOM if unbounded queries load gigabytes into memory.

## When to use this
* Every node sizing and production deployment configuration.

## When not to use this
* Never violate the 50% RAM rule or 31GB heap ceiling.

## What comes next
In Phase 64, we investigate Disk Storage and Allocation Watermarks.
""",
"""#!/usr/bin/env python3

def calculate_pointer_waste(num_objects=500_000_000):
    # Compressed OOPs (<= 31GB): 4 bytes per pointer
    compressed_bytes = num_objects * 4
    # Uncompressed OOPs (> 32GB): 8 bytes per pointer
    uncompressed_bytes = num_objects * 8
    wasted_gb = (uncompressed_bytes - compressed_bytes) / (1024 ** 3)
    return wasted_gb

if __name__ == "__main__":
    waste = calculate_pointer_waste(500_000_000)
    print("Compressed OOPs (Ordinary Object Pointers) Analysis:")
    print(f"For 500 million Java heap objects, crossing 32GB wastes {waste:.2f} GB of RAM purely on 64-bit pointer padding!")
    print("Always cap Elasticsearch JVM Heap at 31 GB!")
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 63: Heap and Memory Architecture ==="
python3 phases/63-heap-and-memory/code/63_heap_and_memory.py
"""),

        (64, "Disk and Watermarks",
         "Elasticsearch defends disk with three watermarks: 85% stops allocations, 90% relocates shards, 95% locks the cluster read-only.",
         """# Lesson 64.1: Disk and Watermarks

## Motto
"Elasticsearch defends disk with three watermarks: 85% stops allocations, 90% relocates shards, 95% locks the cluster read-only."

## Problem
A node running out of disk space risks fatal Lucene segment corruption and crash loops. Without warning thresholds, a runaway write workload could completely fill the drive.

## Prediction
What happens to indexing requests when a data node exceeds 95% disk utilization?

## Why this matters
Elasticsearch enforces three automatic **Disk Allocation Watermarks** to safeguard the cluster.

## First principles
The Three Watermarks:
1. **Low Watermark (85%):** Master stops allocating new shards to this node. Existing shards remain writable.
2. **High Watermark (90%):** Master actively attempts to relocate existing shards away from this node to other nodes.
3. **Flood Stage (95%):** Master enforces a **read-only index block** (`index.blocks.read_only_allow_delete: true`). All write/indexing operations fail immediately!

## Mental model
```text
Disk Usage:
  0% ──────────────── 85% ──────────── 90% ──────────── 95% ────── 100%
  [ Normal Writing ] [ Low Mark ]      [ High Mark ]   [ Flood Stage! ]
                     No new shards     Relocate shards  READ-ONLY LOCK!
```

## Build it
See `code/watermark_simulator.py` demonstrating threshold triggers in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/64-disk-and-watermarks/experiments/run_experiment.sh
```

## Inspect it
Check disk utilization and watermarks across nodes:
```bash
curl -s "http://localhost:9200/_cat/allocation?v"
```

## Measure it
Inspect current watermark settings:
```bash
curl -s "http://localhost:9200/_cluster/settings?include_defaults=true" | grep -i "watermark" || true
```

## Break it
Simulate a flood stage lock by manually setting the read-only block on an index:
```bash
curl -X PUT http://localhost:9200/products_phase06/_settings -H "Content-Type: application/json" -d '{
  "index.blocks.read_only_allow_delete": true
}'
```
Attempt an indexing write: observe `ClusterBlockException`!

## Recover it
Free disk space, then clear the block:
```bash
curl -X PUT http://localhost:9200/products_phase06/_settings -H "Content-Type: application/json" -d '{
  "index.blocks.read_only_allow_delete": null
}'
```

## Modify it
Configure custom byte thresholds: `cluster.routing.allocation.disk.watermark.low: "50gb"`.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does the 95% flood stage lock the index into read-only mode instead of failing silently?
2. Why does freeing disk space NOT automatically remove the `read_only_allow_delete` block?

## Guarantees
* Flood stage prevents complete disk exhaustion and filesystem corruption.

## Non-guarantees
* Watermarks cannot save a cluster if all nodes reach 95% simultaneously.

## When to use this
* Disk monitoring, alerts, and emergency incident recovery.

## When not to use this
* Disabling disk thresholds in production (`cluster.routing.allocation.disk.threshold_enabled: false` is dangerous).

## What comes next
In Phase 65, we practice disaster recovery with Snapshots and Restore.
""",
"""#!/usr/bin/env python3

def evaluate_disk_status(disk_pct):
    if disk_pct >= 95:
        return "FLOOD_STAGE", "Action: Index locked READ-ONLY (index.blocks.read_only_allow_delete: true). All writes rejected."
    elif disk_pct >= 90:
        return "HIGH_WATERMARK", "Action: Master attempts to relocate existing shards away from this node."
    elif disk_pct >= 85:
        return "LOW_WATERMARK", "Action: Master stops allocating new shards to this node."
    return "HEALTHY", "Normal operations."

if __name__ == "__main__":
    for usage in [75, 87, 92, 97]:
        stage, action = evaluate_disk_status(usage)
        print(f"Disk at {usage}% -> [{stage:15s}] : {action}")
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 64: Disk Watermarks & Recovery ==="
python3 phases/64-disk-and-watermarks/code/64_disk_and_watermarks.py
"""),

        (65, "Snapshots and Restore",
         "Replicas are for high availability; snapshots are for disaster recovery. Never treat replicas as backups.",
         """# Lesson 65.1: Snapshots and Restore

## Motto
"Replicas are for high availability; snapshots are for disaster recovery. Never treat replicas as backups."

## Problem
A rogue script or human error issues `DELETE /products`. In 50 milliseconds, Elasticsearch dutifully deletes all primary shards AND all replica shards across the entire cluster. Replicas did not save you!

## Prediction
Can you restore a deleted index from an incremental snapshot repository taken an hour earlier?

## Why this matters
**Replicas $\neq$ Backups.** Snapshots are point-in-time point-to-point incremental backups written to external storage (S3, GCS, Shared Filesystem).

## First principles
Snapshot Architecture:
* **Snapshot Repository:** An external storage destination (`fs`, `s3`, `gcs`).
* **Incremental Snapshots:** Snapshots save Lucene segments. Because segments are immutable, subsequent snapshots only copy newly created segments, making them fast and storage-efficient.
* **Restore:** Reconstructs the index by downloading segments into a fresh shard.

## Mental model
```text
Index Segments:
  T0: Segment _0 (1GB) ──► Snapshot 1: Copies Segment _0 (1GB)
  T1: Segment _1 (200MB) ──► Snapshot 2: Copies ONLY Segment _1 (200MB! Incremental!)
```

## Build it
See `code/snapshot_incremental_sim.py` demonstrating incremental segment hashing in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/65-snapshots-and-restore/experiments/run_experiment.sh
```

## Inspect it
Register a local filesystem snapshot repository and take a snapshot:
```bash
curl -X PUT http://localhost:9200/_snapshot/backup_repo -H "Content-Type: application/json" -d '{
  "type": "fs",
  "settings": { "location": "/usr/share/elasticsearch/snapshots" }
}'
curl -X PUT "http://localhost:9200/_snapshot/backup_repo/snapshot_1?wait_for_completion=true"
```

## Measure it
Inspect snapshot metadata:
```bash
curl -s http://localhost:9200/_snapshot/backup_repo/snapshot_1?pretty
```

## Break it
Delete the index: `curl -X DELETE http://localhost:9200/products_phase06`. Confirm it is gone!

## Recover it
Restore the index from snapshot:
```bash
curl -X POST "http://localhost:9200/_snapshot/backup_repo/snapshot_1/_restore?wait_for_completion=true"
curl -s http://localhost:9200/products_phase06/_search?pretty
```
Data is 100% restored!

## Modify it
Restore with index renaming: `{"rename_pattern": "(.+)", "rename_replacement": "restored_$1"}`.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does having 3 replicas provide zero protection against `DELETE /my_index`?
2. Why are subsequent snapshots of the same index vastly faster than the initial snapshot?

## Guarantees
* Restoring a snapshot recreates the exact index state at the time the snapshot completed.

## Non-guarantees
* Snapshots do not capture writes that occurred after the snapshot finished.

## When to use this
* Disaster recovery, production backups, and staging environment hydration.

## When not to use this
* Real-time failover between live cluster nodes (that is what replicas do).

## What comes next
In Phase 66, we explore Index Lifecycle Management (ILM) and data tiering.
""",
"""#!/usr/bin/env python3

class SnapshotRepoSim:
    def __init__(self):
        self.repo_segments = set()
        self.snapshots = {}

    def take_snapshot(self, snapshot_name, active_segments):
        # Only copy new segments (incremental)
        new_segments = [s for s in active_segments if s not in self.repo_segments]
        self.repo_segments.update(new_segments)
        self.snapshots[snapshot_name] = list(active_segments)
        return len(new_segments)

if __name__ == "__main__":
    repo = SnapshotRepoSim()
    print("Time 1: Index has segments [_0, _1]")
    copied = repo.take_snapshot("snap_1", ["seg_0", "seg_1"])
    print(f"  Snapshot 1 copied: {copied} segments.")

    print("\\nTime 2: Segment _2 created. Segments are now [_0, _1, _2]")
    copied = repo.take_snapshot("snap_2", ["seg_0", "seg_1", "seg_2"])
    print(f"  Snapshot 2 copied: {copied} segment (Incremental!)")
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 65: Snapshots and Disaster Recovery ==="
python3 phases/65-snapshots-and-restore/code/65_snapshots_and_restore.py
"""),

        (66, "Index Lifecycle Concepts",
         "Data ages: Hot nodes write, Warm nodes query, Cold nodes freeze, and Delete purges.",
         """# Lesson 66.1: Index Lifecycle Concepts

## Motto
"Data ages: Hot nodes write, Warm nodes query, Cold nodes freeze, and Delete purges."

## Problem
In a logging cluster generating 500GB/day, storing 1 year of logs on ultra-fast NVMe SSDs would cost tens of thousands of dollars per month. Yet 95% of all searches only target the last 7 days!

## Prediction
Can you automatically move older indices from expensive fast SSD nodes to cheaper dense storage nodes as they age?

## Why this matters
**Index Lifecycle Management (ILM)** automates data tiering, rollover, shrinking, force-merging, and deletion based on index age and size.

## First principles
The Four Data Tiers:
1. **Hot Tier:** Active ingestion. High write speed, NVMe SSDs, fast CPUs.
2. **Warm Tier:** Read-only queries. Lower ingestion, force-merged segments to 1 segment, cheaper SSDs.
3. **Cold Tier:** Infrequent queries. Fully frozen segments, low-cost HDDs or object store.
4. **Delete Phase:** Automatically drops indices after retention period expires (e.g. 90 days).

## Mental model
```text
Day 1 (Hot Tier): Active writes, 1s refresh, fast SSDs
       │ Rollover after 50 GB or 1 day
       ▼
Day 7 (Warm Tier): Read-only, force-merged to 1 segment, replicas=1
       │ Migrate after 30 days
       ▼
Day 30 (Cold Tier): Frozen segments, zero write buffers, dense storage
       │ Purge after 90 days
       ▼
Day 90 (Delete Phase): Index deleted. Storage reclaimed.
```

## Build it
See `code/ilm_state_machine.py` simulating lifecycle phase transitions in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/66-index-lifecycle-concepts/experiments/run_experiment.sh
```

## Inspect it
Create an ILM policy:
```bash
curl -X PUT http://localhost:9200/_ilm/policy/logs_policy -H "Content-Type: application/json" -d '{
  "policy": {
    "phases": {
      "hot": { "actions": { "rollover": { "max_primary_shard_size": "50gb", "max_age": "7d" } } },
      "delete": { "min_age": "30d", "actions": { "delete": {} } }
    }
  }
}'
```

## Measure it
Inspect policy status: `curl -s http://localhost:9200/_ilm/policy/logs_policy?pretty`.

## Break it
Configure rollover with an alias that does not have a write index designated (`is_write_index: true`).

## Recover it
Mark the active index in the alias: `{"actions": [{"add": {"index": "logs-000001", "alias": "logs", "is_write_index": true}}]}`.

## Modify it
Add a warm phase action that force-merges to 1 segment: `{"actions": {"forcemerge": {"max_num_segments": 1}}}`.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does force-merging an index to 1 segment in the Warm phase reduce memory and search cost?
2. What is the role of an Index Alias in automated Rollover?

## Guarantees
* ILM enforces storage retention policies automatically in the background.

## Non-guarantees
* ILM will not delete data if the policy is misconfigured or cluster disk is full.

## When to use this
* Time-series indices, application logs, metrics, audit records, and security events.

## When not to use this
* Static entity catalogs (e.g. product catalog updated by daily batch).

## What comes next
In Phase 67, we build a complete Time-Series / Logging Workload.
""",
"""#!/usr/bin/env python3

def evaluate_ilm(index_age_days, size_gb):
    if index_age_days >= 90:
        return "DELETE", "Delete index permanently"
    elif index_age_days >= 30:
        return "COLD", "Move to cold tier, freeze segments"
    elif index_age_days >= 7 or size_gb >= 50:
        return "WARM", "Rollover to new index, force-merge to 1 segment, move to warm tier"
    return "HOT", "Active write tier"

if __name__ == "__main__":
    test_cases = [(2, 20), (5, 55), (14, 40), (45, 30), (100, 30)]
    print("ILM Phase Transitions:")
    for age, size in test_cases:
        phase, action = evaluate_ilm(age, size)
        print(f"  Age: {age:3d}d, Size: {size:2d}GB ──► Phase: [{phase:6s}] - {action}")
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 66: Index Lifecycle Management (ILM) ==="
python3 phases/66-index-lifecycle-concepts/code/66_index_lifecycle_concepts.py
"""),

        (67, "Time-Series / Logging Workload",
         "Append-only time-series data requires rolling indices, data streams, and disciplined retention.",
         """# Lesson 67.1: Time-Series / Logging Workload

## Motto
"Append-only time-series data requires rolling indices, data streams, and disciplined retention."

## Problem
Logs arrive at 10,000 events/second. If all logs are written into a single monolithic index `app-logs`, the index grows to 20 terabytes. Searching recent logs slows down, and deleting logs older than 30 days requires running a catastrophic `_delete_by_query` that overburdens the cluster with millions of soft deletes!

## Prediction
Why is dropping an entire daily index with `DELETE /logs-2026.01.01` instantaneous and free, whereas deleting 10 million rows with `_delete_by_query` takes hours and bloats disk?

## Why this matters
Time-series architectures leverage filesystem-level directory deletions instead of Lucene row-level tombstones.

## First principles
* **Monolithic Index Anti-Pattern:** A single index cannot easily purge old data. `_delete_by_query` writes `.del` markers, requiring costly segment merges.
* **Rolling Indices / Data Streams:** Data is sliced by time: `logs-2026.01.01`, `logs-2026.01.02`.
* **Deleting Old Data:** Dropping an old index (`DELETE /logs-2025.12.01`) is an instantaneous filesystem directory deletion ($O(1)$) with zero CPU or segment merge overhead!

## Mental model
```text
Bad: Monolithic Index (10 TB)
  Delete 30-day-old logs ──► _delete_by_query ──► 10,000,000 tombstones, high CPU!

Best Practice: Time-Series Indices / Data Stream
  logs-2026-03-21 (Active Hot)
  logs-2026-03-20 (Warm)
  ...
  logs-2025-12-01 (90 days old) ──► DELETE /logs-2025-12-01 ──► Instant directory removal!
```

## Build it
See `code/timeseries_simulator.py` demonstrating time-partitioned log queries in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/67-time-series---logging-workload/experiments/run_experiment.sh
```

## Inspect it
Index a structured log document with a timestamp:
```bash
curl -X POST http://localhost:9200/logs_demo/_doc -H "Content-Type: application/json" -d '{
  "@timestamp": "2026-09-23T12:00:00Z",
  "service": "payment-api",
  "level": "ERROR",
  "status_code": 500,
  "message": "Database connection pool exhausted"
}'
```

## Measure it
Execute a date-histogram aggregation of log errors over time:
```bash
curl -X POST http://localhost:9200/logs_demo/_search -H "Content-Type: application/json" -d '{
  "size": 0,
  "aggs": {
    "errors_over_time": {
      "date_histogram": {
        "field": "@timestamp",
        "fixed_interval": "1h"
      }
    }
  }
}'
```

## Break it
Execute an unbounded search across `logs-*` without a timestamp range filter. Observe query fan-out across dozens of old indices.

## Recover it
Always enforce a `@timestamp` range filter in time-series queries so Elasticsearch can prune non-matching indices before querying shards.

## Modify it
Use modern Elasticsearch Data Streams (`POST /_data_stream/my-data-stream`).

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why is dropping a daily index vastly more efficient than running `_delete_by_query`?
2. What is an Elasticsearch Data Stream and how does it manage backing indices?

## Guarantees
* Time-partitioned indices enable instant, zero-cost data retention drops.

## Non-guarantees
* Searching `logs-*` across 1,000 old daily indices will suffer high coordination latency unless pruned by date range.

## When to use this
* Application logs, server metrics, network telemetry, and sensor streams.

## When not to use this
* Entity datasets requiring frequent point updates to existing records (e.g. user profiles).

## What comes next
In Phase 68, we build transformations using Ingest Pipelines.
""",
"""#!/usr/bin/env python3
from datetime import datetime, timedelta

def generate_sample_log(service, level, msg, hours_ago=0):
    ts = (datetime.utcnow() - timedelta(hours=hours_ago)).isoformat() + "Z"
    return {
        "@timestamp": ts,
        "service": service,
        "level": level,
        "message": msg
    }

if __name__ == "__main__":
    logs = [
        generate_sample_log("auth-svc", "INFO", "User login successful", hours_ago=1),
        generate_sample_log("payment-svc", "ERROR", "Payment gateway timeout", hours_ago=2),
        generate_sample_log("auth-svc", "WARN", "Invalid password attempt", hours_ago=3)
    ]
    print("Generated Structured Time-Series Log Records:")
    for l in logs:
        print(f"  [{l['@timestamp']}] [{l['level']:5s}] {l['service']:12s}: {l['message']}")
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 67: Time-Series Logging Workload ==="
python3 phases/67-time-series---logging-workload/code/67_time_series_logging.py
"""),

        (68, "Ingest Pipelines",
         "Transform data before indexing: Grok parsing, date conversion, renaming, and geo-ip lookup at the cluster ingestion boundary.",
         """# Lesson 68.1: Ingest Pipelines

## Motto
"Transform data before indexing: Grok parsing, date conversion, renaming, and geo-ip lookup at the cluster ingestion boundary."

## Problem
Log shippers and client applications send raw, messy text lines:
`"192.168.1.1 - - [23/Sep/2026:12:00:00] 'GET /api/v1/checkout HTTP/1.1' 200 452"`
If the application must parse regexes, convert timestamps, and extract IP addresses before indexing, every client microservice duplicates complex parsing logic.

## Prediction
Can Elasticsearch parse raw log strings into structured JSON fields during ingestion before the document reaches the index mapping?

## Why this matters
**Ingest Pipelines** execute pre-processing processors on data nodes before documents are validated and indexed into Lucene.

## First principles
Ingest Node Processors:
* `grok`: Parses unstructured log strings into structured fields using regular expressions.
* `date`: Parses custom timestamp formats into standard ISO 8601 `@timestamp`.
* `rename`: Modifies field names.
* `set`: Assigns default values.
* `geoip`: Translates IP addresses into geographic latitude, longitude, and country.

## Mental model
```text
Raw Document: { "raw_line": "10.0.0.1 GET /login 200" }
                         │
                 [ Ingest Pipeline ]
                         │
   ├── Grok Processor: extracts ip, method, endpoint, status
   ├── Convert Processor: casts status to integer
   └── Remove Processor: drops raw_line
                         │
                         ▼
Indexed Document: { "ip": "10.0.0.1", "endpoint": "/login", "status": 200 }
```

## Build it
See `code/ingest_pipeline_sim.py` demonstrating pipeline transformations in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/68-ingest-pipelines/experiments/run_experiment.sh
```

## Inspect it
Create an ingest pipeline using `_ingest/pipeline`:
```bash
curl -X PUT http://localhost:9200/_ingest/pipeline/parse_access_logs -H "Content-Type: application/json" -d '{
  "description": "Extracts fields from access log",
  "processors": [
    {
      "grok": {
        "field": "message",
        "patterns": ["%{IP:client_ip} %{WORD:http_method} %{URIPATH:request_path} %{NUMBER:status_code:int}"]
      }
    }
  ]
}'
```
Test the pipeline with `_simulate`:
```bash
curl -X POST http://localhost:9200/_ingest/pipeline/parse_access_logs/_simulate -H "Content-Type: application/json" -d '{
  "docs": [
    { "_source": { "message": "192.168.1.50 GET /cart/checkout 200" } }
  ]
}'
```

## Measure it
Inspect CPU overhead on ingest nodes during heavy Grok regex parsing.

## Break it
Pass a malformed string that fails Grok parsing without an `on_failure` handler. Indexing fails with `grok_parse_failure`!

## Recover it
Add an `on_failure` processor block to route failed logs to an error field or dead-letter index.

## Modify it
Set `default_pipeline` in index settings so all writes to the index automatically pass through the pipeline.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why is running `_simulate` recommended before applying an Ingest Pipeline to production data?
2. What are the trade-offs of preprocessing logs in Elasticsearch ingest nodes vs upstream in Logstash or Vector?

## Guarantees
* Documents are fully transformed before entering the mapping and indexing stage.

## Non-guarantees
* Complex Grok regexes can consume high CPU if expressions trigger catastrophic backtracking.

## When to use this
* Lightweight log transformation, field normalization, and IP geolocations.

## When not to use this
* Heavy ETL requiring distributed stream joins or multi-sink routing (use Apache Flink or Kafka Streams).

## What comes next
In Phase 69, we design our application-facing Search API.
""",
"""#!/usr/bin/env python3
import re

def simulate_ingest_pipeline(raw_doc):
    message = raw_doc.get("message", "")
    pattern = r"(?P<ip>\S+) (?P<method>\S+) (?P<path>\S+) (?P<status>\d+)"
    match = re.match(pattern, message)
    if not match:
        return {"error": "grok_parse_failure", "raw": message}

    data = match.groupdict()
    data["status"] = int(data["status"])
    return data

if __name__ == "__main__":
    sample = {"message": "192.168.1.42 POST /api/v2/orders 201"}
    print("Raw Incoming Document:")
    print(" ", sample)
    transformed = simulate_ingest_pipeline(sample)
    print("\\nTransformed Document after Ingest Pipeline:")
    print(" ", transformed)
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 68: Ingest Pipelines ==="
python3 phases/68-ingest-pipelines/code/68_ingest_pipelines.py
""")
    ]

    for p_num, p_title, motto, doc_content, code_content, exp_content in phases:
        slug = f"{p_num:02d}-{p_title.lower().replace(' ', '-').replace('/', '-')}"
        phase_dir = os.path.join(PHASES_DIR, slug)
        write_file(os.path.join(phase_dir, "docs", "en.md"), doc_content)
        write_file(os.path.join(phase_dir, "code", f"{slug.replace('-', '_')}.py"), code_content)
        write_file(os.path.join(phase_dir, "experiments", "run_experiment.sh"), exp_content)
        write_file(os.path.join(phase_dir, "outputs", "evidence-template.md"), evidence_template(p_title, p_num))
        print(f"Generated Phase {p_num:02d}: {p_title}")

if __name__ == "__main__":
    generate_phases_56_to_68()
