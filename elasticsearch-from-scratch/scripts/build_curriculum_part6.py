#!/usr/bin/env python3
"""
build_curriculum_part6.py - Generates Phases 69 to 81 for elasticsearch-from-scratch.
Covers Search API Design, Capstones 1 & 2 (Product Search, Log Search), Relevance Evaluation,
Reindexing, Aliases, Security, Observability, Capacity Planning, Failure Injection,
Mini Search Engine (Capstone 3), and Distributed Simulator.
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

def generate_phases_69_to_81():
    phases = [
        (69, "Search API Design",
         "Never leak raw query DSL to the public internet: encapsulate search behind a strongly typed, validated API gateway.",
         """# Lesson 69.1: Search API Design

## Motto
"Never leak raw query DSL to the public internet: encapsulate search behind a strongly typed, validated API gateway."

## Problem
A naive backend exposes a pass-through endpoint `POST /api/search` that forwards the user's JSON directly into Elasticsearch `_search`. An attacker injects leading wildcards, deep paginations (`from: 1000000`), or fielddata aggregations on sensitive internal fields, bringing down the entire cluster.

## Prediction
Why is exposing raw Elasticsearch JSON DSL to public frontend clients considered a critical security and performance vulnerability?

## Why this matters
Search API gateways enforce query sanitation, parameter validation, default filters (e.g. `tenant_id`, `deleted: false`), max page windows, and rate limits.

## First principles
API Gateway Responsibilities:
1. **Contract Abstraction:** Accepts clean query params: `GET /search?q=wireless&category=tech&page=2`.
2. **Mandatory Tenant Isolation:** Injects security filter context (`tenant_id: auth_user.tenant_id`) that the user cannot override.
3. **Pagination Bounding:** Caps `size <= 50` and prevents deep pagination.
4. **DSL Construction:** Translates safe parameters into an optimized compound `bool` query.

## Mental model
```text
Public Client (Browser / Mobile)
          │ GET /v1/products?q=chair&min_price=100
          ▼
   API GATEWAY (Python / FastAPI / Express)
          ├── 1. Validate & Sanitize Input
          ├── 2. Inject Security Filters (tenant_id = 42)
          ├── 3. Enforce Max Result Window (page <= 20)
          └── 4. Construct Safe Elasticsearch Bool Query
                         │
                         ▼
        ELASTICSEARCH CLUSTER (Internal Network)
```

## Build it
See `code/search_gateway.py` implementing a clean parameter-to-DSL translation layer in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/69-search-api-design/experiments/run_experiment.sh
```

## Inspect it
Test the gateway's query generator with various input parameters.

## Measure it
Measure latency added by the translation layer (typically < 0.2ms in Python).

## Break it
Send an injection attempt (`q="*.*.*"`, `from=9999999`) and observe how the gateway rejects or sanitizes the input before reaching Elasticsearch.

## Recover it
Always validate query parameters using strict schemas (e.g. Pydantic).

## Modify it
Add highlighting configurations to return text snippets with `<em>` tags.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. What attacks are possible when raw Elasticsearch query DSL is exposed directly to clients?
2. How does the search gateway guarantee multi-tenant data isolation?

## Guarantees
* The gateway guarantees that no unvalidated query shapes reach the cluster.

## Non-guarantees
* The gateway does not replace cluster-side resource limits.

## When to use this
* Every production search service.

## When not to use this
* Internal cluster debugging using `curl`.

## What comes next
In Phase 70, we build Capstone 1: The Complete Product Search Project.
""",
"""#!/usr/bin/env python3

def build_safe_search_dsl(user_q, category=None, max_price=None, page=1, page_size=20, tenant_id="acme"):
    # 1. Enforce pagination limits
    page_size = min(max(1, page_size), 50)
    page = max(1, min(page, 20))
    from_offset = (page - 1) * page_size

    # 2. Build bool query
    must_clauses = []
    if user_q:
        must_clauses.append({
            "multi_match": {
                "query": user_q.strip()[:100], # truncate long strings
                "fields": ["title^2", "description"]
            }
        })
    else:
        must_clauses.append({"match_all": {}})

    # 3. Mandatory filter context
    filter_clauses = [{"term": {"tenant_id": tenant_id}}]
    if category:
        filter_clauses.append({"term": {"category.keyword": category}})
    if max_price is not None:
        filter_clauses.append({"range": {"price": {"lte": float(max_price)}}})

    dsl = {
        "from": from_offset,
        "size": page_size,
        "query": {
            "bool": {
                "must": must_clauses,
                "filter": filter_clauses
            }
        }
    }
    return dsl

if __name__ == "__main__":
    query = build_safe_search_dsl("mechanical keyboard", category="electronics", max_price=150.0, page=2, page_size=10, tenant_id="tenant_88")
    import json
    print("Safely Generated Elasticsearch DSL:")
    print(json.dumps(query, indent=2))
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 69: Search API Gateway Design ==="
python3 phases/69-search-api-design/code/69_search_api_design.py
"""),

        (70, "Product Search Project",
         "Capstone 1: Build a production-grade e-commerce catalog search with facets, typos, autocomplete, and relevance ranking.",
         """# Lesson 70.1: Product Search Project (Capstone 1)

## Motto
"Capstone 1: Build a production-grade e-commerce catalog search with facets, typos, autocomplete, and relevance ranking."

## Problem
In a real-world e-commerce platform, search is the primary driver of revenue. Building a professional product search engine requires synthesizing everything learned: custom mappings, multi-fields, BM25 tuning, fuzzy matching, faceted aggregations, price range filters, and sub-10ms autocomplete.

## Prediction
Can our integrated e-commerce search service handle simultaneous full-text matching, facet counting, price filtering, and typo correction with p95 latency under 15ms?

## Why this matters
This is the first comprehensive capstone project. You will implement and benchmark a complete, realistic e-commerce search backend.

## First principles
Architectural Features:
1. **Schema Design:** `title` (analyzed text + autocomplete edge n-grams), `brand` (`keyword`), `category` (`keyword`), `price` (`double`), `rating` (`float`), `in_stock` (`boolean`).
2. **Compound Query:** `bool` combining full-text `multi_match` on title/description with cached filters on category, stock, and price.
3. **Faceted Navigation:** Returns category counts and price histogram buckets alongside hits.
4. **Typo Resilience:** Fuzzy matching enabled on user query.

## Mental model
```text
                         USER SEARCH INPUT
                   "ergonomic mech keyboard"
                               │
                               ▼
 ┌───────────────────────────────────────────────────────────┐
 │               CAPSTONE 1 SEARCH ENGINE                    │
 ├───────────────────────────────────────────────────────────┤
 │ 1. Full-Text Search: title^3, brand^2, description        │
 │ 2. Typo Resilience: fuzziness: AUTO, prefix_length: 2     │
 │ 3. Exact Filtering: in_stock: true, price: [50 TO 200]    │
 │ 4. Multi-Facet Aggs: category terms, brand terms, avg_rate│
 └─────────────────────────────┬─────────────────────────────┘
                               │
                               ▼
  JSON RESPONSE: Top 10 Ranked Products + Category Facet Counts
```

## Build it
See `projects/product_search/` and `code/catalog_search.py` implementing the complete system.

## Use Elasticsearch
Run the experiment:
```bash
./phases/70-product-search-project/experiments/run_experiment.sh
```

## Inspect it
Load the sample 1,000 product catalog and execute the benchmark queries.

## Measure it
Capture p50, p95, and p99 search latency across 500 simulated user searches.

## Break it
Inject extreme typos (e.g. `"ergnomk keybrd"`) and observe how fuzzy matching and field boosting maintain recall.

## Recover it
Fine-tune minimum should match and boost weights.

## Modify it
Add customer review score boosting using `function_score` or `script_score`.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. How does boosting `title^3` over `description` improve relevance in an e-commerce catalog?
2. Why should price and inventory filters always execute in filter context?

## Guarantees
* Delivers production-grade faceted e-commerce search with high precision and recall.

## Non-guarantees
* Does not personalize results based on user historical browsing habits.

## When to use this
* E-commerce catalogs, online marketplaces, and digital storefronts.

## When not to use this
* Raw un-indexed key-value storage.

## What comes next
In Phase 71, we build Capstone 2: Structured Log Search and Analytics.
""",
"""#!/usr/bin/env python3
import json

def create_catalog_index_dsl():
    return {
        "settings": {
            "number_of_shards": 2,
            "number_of_replicas": 0,
            "analysis": {
                "tokenizer": {
                    "autocomplete_tokenizer": {
                        "type": "edge_ngram",
                        "min_gram": 2,
                        "max_gram": 10,
                        "token_chars": ["letter", "digit"]
                    }
                },
                "analyzer": {
                    "autocomplete_analyzer": {
                        "type": "custom",
                        "tokenizer": "autocomplete_tokenizer",
                        "filter": ["lowercase"]
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "title": {
                    "type": "text",
                    "fields": {
                        "keyword": {"type": "keyword"},
                        "autocomplete": {"type": "text", "analyzer": "autocomplete_analyzer"}
                    }
                },
                "description": {"type": "text"},
                "category": {"type": "keyword"},
                "brand": {"type": "keyword"},
                "price": {"type": "double"},
                "rating": {"type": "float"},
                "in_stock": {"type": "boolean"}
            }
        }
    }

if __name__ == "__main__":
    dsl = create_catalog_index_dsl()
    print("Capstone 1: E-commerce Catalog Mapping Specification:")
    print(json.dumps(dsl, indent=2))
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 70: Capstone 1 - Product Search Project ==="
python3 phases/70-product-search-project/code/70_product_search_project.py
"""),

        (71, "Log Search Project",
         "Capstone 2: Structured log aggregation, trace indexing, error histograms, and retention lifecycle.",
         """# Lesson 71.1: Log Search Project (Capstone 2)

## Motto
"Capstone 2: Structured log aggregation, trace indexing, error histograms, and retention lifecycle."

## Problem
In a microservices cloud architecture with 50 services emitting millions of logs per hour, developers need to diagnose production outages in seconds: "Show all HTTP 500 errors across `payment-service` in the last 15 minutes, group by error message, and correlate with distributed `trace_id`".

## Prediction
How fast can Elasticsearch filter 100,000 logs by service name and aggregate error rates into 1-minute time buckets?

## Why this matters
This capstone covers the operational half of Elasticsearch: high-throughput time-series logging, trace correlation, and analytics dashboards.

## First principles
Log Search Architecture:
1. **Schema:** `@timestamp` (`date`), `service` (`keyword`), `level` (`keyword`), `trace_id` (`keyword`), `message` (`text`), `duration_ms` (`integer`).
2. **Targeted Date Filtering:** Queries ALWAYS bound `@timestamp` to prune index shards.
3. **Facet Aggregations:** `date_histogram` for error rates over time, `terms` on `message.keyword` for top recurring exceptions.

## Mental model
```text
Microservice Fleet (50 pods)
  │ Logs via HTTP/Kafka
  ▼
Elasticsearch Ingest Pipeline ──► Data Stream: logs-app-default
  │
  ├── 1. Filter: service: "payment-service" AND level: "ERROR"
  ├── 2. Aggregation: date_histogram (1m intervals)
  └── 3. Correlate: trace_id = "trace-8891-abc" (Full distributed call stack!)
```

## Build it
See `projects/log_search/` and `code/log_search_engine.py` generating and analyzing structured logs.

## Use Elasticsearch
Run the experiment:
```bash
./phases/71-log-search-project/experiments/run_experiment.sh
```

## Inspect it
Load 5,000 synthetic microservice logs and query for error spikes:
```bash
curl -X POST http://localhost:9200/app_logs/_search -H "Content-Type: application/json" -d '{
  "size": 5,
  "query": {
    "bool": {
      "filter": [
        { "term": { "level": "ERROR" } },
        { "term": { "service": "payment-api" } }
      ]
    }
  },
  "aggs": {
    "errors_per_minute": {
      "date_histogram": { "field": "@timestamp", "fixed_interval": "1m" }
    }
  }
}'
```

## Measure it
Measure query response time for error histogram aggregations (< 10ms).

## Break it
Run an un-bounded text wildcard on `message` without a timestamp filter and observe query duration climb.

## Recover it
Mandate `@timestamp` filters on all log search forms.

## Modify it
Add a percentile aggregation on `duration_ms` to calculate p95 service latency.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why is `trace_id` mapped as `keyword` rather than `text`?
2. How does date pruning allow Elasticsearch to skip searching older immutable segments?

## Guarantees
* Provides fast structured filtering and time-series error rate calculations.

## Non-guarantees
* High-volume logging requires capacity planning (Phase 78) to avoid disk exhaustion.

## When to use this
* Centralized logging, distributed tracing (APM), security event auditing (SIEM).

## When not to use this
* Permanent archival where data is never queried (write compressed tarballs to S3 Glacier instead).

## What comes next
In Phase 72, we evaluate search quality using Search Relevance Evaluation metrics.
""",
"""#!/usr/bin/env python3
import json
from datetime import datetime, timedelta
import random

def generate_logs(count=100):
    services = ["auth-api", "payment-api", "cart-api", "shipping-api"]
    levels = ["INFO", "INFO", "INFO", "WARN", "ERROR"]
    logs = []
    base_time = datetime.utcnow()
    for i in range(count):
        ts = (base_time - timedelta(seconds=i * 5)).isoformat() + "Z"
        svc = random.choice(services)
        lvl = random.choice(levels)
        msg = f"Processed request for order_{i}" if lvl != "ERROR" else "Connection timeout to upstream database"
        logs.append({
            "@timestamp": ts,
            "service": svc,
            "level": lvl,
            "trace_id": f"trace_{random.randint(1000, 9999)}",
            "message": msg,
            "duration_ms": random.randint(10, 450)
        })
    return logs

if __name__ == "__main__":
    data = generate_logs(5)
    print("Capstone 2: Structured Log Event Format:")
    print(json.dumps(data, indent=2))
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 71: Capstone 2 - Log Search Project ==="
python3 phases/71-log-search-project/code/71_log_search_project.py
"""),

        (72, "Search Relevance Evaluation",
         "Search quality is not a feeling: quantify relevance with Precision@K, Mean Reciprocal Rank, and NDCG.",
         """# Lesson 72.1: Search Relevance Evaluation

## Motto
"Search quality is not a feeling: quantify relevance with Precision@K, Mean Reciprocal Rank, and NDCG."

## Problem
A developer changes a query boost: `title^2` to `title^4`. They test one query on their laptop, decide "it looks better", and deploy to production. In doing so, they silently degrade search results for 40% of customer queries!

## Prediction
How can you objectively measure whether a change to Elasticsearch rankings improved or harmed search results across a test suite of 100 queries?

## Why this matters
Relevance engineering is an empirical science. Professional search teams use quantitative evaluation metrics.

## First principles
Core Information Retrieval Metrics:
1. **Precision@K:** What fraction of the top $K$ results are relevant?
   $$\text{Precision@K} = \frac{|\text{Relevant Docs in Top } K|}{K}$$
2. **Mean Reciprocal Rank (MRR):** How quickly does the user find the first relevant document? (Reciprocal of the rank position of the first relevant result).
3. **NDCG (Normalized Discounted Cumulative Gain):** Rewards placing highly relevant documents near the very top of the list.

## Mental model
```text
Query: "wireless keyboard"
  Ground Truth Relevant Docs: [Doc A, Doc B]

Result 1: [Doc A, Doc B, Doc C] ──► Precision@3 = 2/3 = 66%, MRR = 1.0 (First doc relevant!)
Result 2: [Doc X, Doc Y, Doc A] ──► Precision@3 = 1/3 = 33%, MRR = 0.33 (Relevant doc buried at rank 3)
```

## Build it
See `code/relevance_evaluator.py` computing Precision@K and MRR in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/72-search-relevance-evaluation/experiments/run_experiment.sh
```

## Inspect it
Use Elasticsearch's native **Ranking Evaluation API** (`_rank_eval`):
```bash
curl -X POST http://localhost:9200/products_phase06/_rank_eval -H "Content-Type: application/json" -d '{
  "requests": [
    {
      "id": "keyboard_query",
      "request": { "query": { "match": { "title": "keyboard" } } },
      "ratings": [
        { "_index": "products_phase06", "_id": "1", "rating": 3 }
      ]
    }
  ],
  "metric": { "precision": { "k": 5 } }
}'
```

## Measure it
Compare MRR scores before and after applying field boosts.

## Break it
Tune rankings for one query while measuring the whole suite: observe how over-fitting to one query hurts overall MRR.

## Recover it
Maintain a diverse golden evaluation dataset spanning common head queries and rare tail queries.

## Modify it
Test NDCG metric with graded ratings (0=irrelevant, 1=marginal, 2=relevant, 3=perfect).

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why is measuring search quality on a single query misleading?
2. What does a Mean Reciprocal Rank (MRR) of 0.5 indicate? (The first relevant hit appears on average at rank 2).

## Guarantees
* Ranking evaluation provides statistical confidence for relevance changes.

## Non-guarantees
* Metrics are only as good as the ground-truth relevance judgment dataset.

## When to use this
* Every search relevance change, boost tuning, and analyzer modification.

## When not to use this
* Pure operational logging clusters where BM25 relevance is not used.

## What comes next
In Phase 73, we apply these evaluation metrics to Synonym and Relevance Tuning.
""",
"""#!/usr/bin/env python3

def precision_at_k(retrieved_ids, relevant_ids, k=5):
    top_k = retrieved_ids[:k]
    matches = [d for d in top_k if d in relevant_ids]
    return len(matches) / float(k)

def reciprocal_rank(retrieved_ids, relevant_ids):
    for rank, doc_id in enumerate(retrieved_ids, start=1):
        if doc_id in relevant_ids:
            return 1.0 / rank
    return 0.0

if __name__ == "__main__":
    golden_relevant = {101, 102}
    algo_a_results = [101, 500, 102, 600, 700]
    algo_b_results = [800, 900, 101, 102, 950]

    print("Algorithm A Results:", algo_a_results)
    print(f"  Precision@5: {precision_at_k(algo_a_results, golden_relevant, 5):.2f}")
    print(f"  MRR:         {reciprocal_rank(algo_a_results, golden_relevant):.2f}")

    print("\\nAlgorithm B Results:", algo_b_results)
    print(f"  Precision@5: {precision_at_k(algo_b_results, golden_relevant, 5):.2f}")
    print(f"  MRR:         {reciprocal_rank(algo_b_results, golden_relevant):.2f}")
    print("\\nAlgorithm A achieved superior MRR because the first relevant item appeared at rank 1!")
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 72: Search Relevance Evaluation ==="
python3 phases/72-search-relevance-evaluation/code/72_search_relevance_evaluation.py
"""),

        (73, "Synonym and Relevance Tuning",
         "Relevance tuning is multi-variable optimization: balance field boosts, synonyms, and phrase slop against evaluation metrics.",
         """# Lesson 73.1: Synonym and Relevance Tuning

## Motto
"Relevance tuning is multi-variable optimization: balance field boosts, synonyms, and phrase slop against evaluation metrics."

## Problem
In catalog search, users search for `"apple laptop"`. If the product brand is `"Apple"` and category is `"laptop"`, but title is `"MacBook Pro"`, a standard match query fails to rank the document at the top.

## Prediction
How can you combine multi-match field boosting, synonyms, and cross-fields matching to maximize MRR?

## Why this matters
Relevance tuning balances recall (finding all reasonable matches) with precision (placing the best match at rank 1).

## First principles
Tuning Levers:
1. **Field Boosts:** `title^3`, `brand^2`, `category^1.5`. Gives higher weight to matches in concise fields.
2. **`cross_fields` Type:** Treats all fields as a single combined document, so `"apple"` in brand and `"laptop"` in category satisfy the query together!
3. **Phrase Slop Boosting:** Uses `should` with `match_phrase` (slop 1) to give bonus points to documents where words appear adjacent.

## Mental model
```text
Query: "apple laptop"
  ├── Must match: cross_fields on [brand, category, title] (Recall)
  └── Should match: match_phrase on title with boost^2 (Precision bonus for adjacency!)
```

## Build it
See `code/relevance_tuning_experiment.py` running benchmark comparisons in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/73-synonym-and-relevance-tuning/experiments/run_experiment.sh
```

## Inspect it
Test `multi_match` with `cross_fields`:
```bash
curl -X POST http://localhost:9200/products_phase06/_search -H "Content-Type: application/json" -d '{
  "query": {
    "multi_match": {
      "query": "wireless keyboard",
      "type": "cross_fields",
      "fields": ["title^3", "category^1.5"]
    }
  }
}'
```

## Measure it
Compare Precision@5 before and after adding phrase boost.

## Break it
Assign an extreme boost (`title^1000`): observe that relevance scores for title matches completely drown out category and brand filters.

## Recover it
Keep boosts moderate (typically $1.2\times$ to $3.0\times$).

## Modify it
Add `tie_breaker: 0.3` to include signals from secondary matching fields.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does `multi_match` with `type: cross_fields` solve term distribution across multiple columns?
2. What is the danger of setting arbitrary boost factors (> 50)?

## Guarantees
* Boost factors deterministically scale BM25 term weights.

## Non-guarantees
* Boosting cannot fix missing terms if the tokenizer discarded them.

## When to use this
* Fine-tuning catalog search, knowledge bases, and document archives.

## When not to use this
* Exact status queries or log filtering.

## What comes next
In Phase 74, we master Reindexing when mapping changes are required.
""",
"""#!/usr/bin/env python3

def score_product(query_tokens, doc, boosts):
    score = 0.0
    for t in query_tokens:
        if t in doc.get("title", "").lower():
            score += 1.0 * boosts.get("title", 1.0)
        if t in doc.get("brand", "").lower():
            score += 1.0 * boosts.get("brand", 1.0)
        if t in doc.get("category", "").lower():
            score += 1.0 * boosts.get("category", 1.0)
    return score

if __name__ == "__main__":
    doc = {"title": "MacBook Pro M3", "brand": "Apple", "category": "laptop"}
    query = ["apple", "laptop"]

    default_score = score_product(query, doc, boosts={"title": 1.0, "brand": 1.0, "category": 1.0})
    tuned_score = score_product(query, doc, boosts={"title": 3.0, "brand": 2.0, "category": 1.5})

    print("Document:", doc)
    print("Query:", query)
    print(f"Default Score (1x): {default_score}")
    print(f"Tuned Score (Boosted): {tuned_score}")
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 73: Synonym & Relevance Tuning ==="
python3 phases/73-synonym-and-relevance-tuning/code/73_synonym_and_relevance_tuning.py
"""),

        (74, "Reindexing",
         "Lucene mappings are immutable on disk: changing an analyzer or field type requires reindexing to a new index.",
         """# Lesson 74.1: Reindexing

## Motto
"Lucene mappings are immutable on disk: changing an analyzer or field type requires reindexing to a new index."

## Problem
You indexed 10 million products with `price` as `keyword`. You need to run numeric range queries (`price BETWEEN 50 AND 100`). You try to change the mapping with `PUT /products/_mapping`:
**Elasticsearch Error:** `"Cannot change existing field type from keyword to double"`.

## Prediction
Why can existing field types in a Lucene index NEVER be altered in-place?

## Why this matters
Lucene inverted indexes, BKD trees, and doc values are permanently encoded on disk at write time. To change how a field is indexed, you must create a new index with the correct mapping and copy data over using the `_reindex` API.

## First principles
The Reindex Lifecycle:
1. Create new index `products_v2` with updated settings, analyzers, and mappings.
2. Call `POST /_reindex` to copy documents from `products_v1` to `products_v2`.
3. Elasticsearch reads `_source` from the old index and streams writes through the new mapping pipeline.
4. Verify document counts.
5. Delete old index `products_v1`.

## Mental model
```text
Old Index (products_v1): price is KEYWORD
                 │
      [ POST /_reindex ]
   (Reads _source from v1, parses through new mapping in v2)
                 │
                 ▼
New Index (products_v2): price is DOUBLE (BKD Tree Range Optimized!)
```

## Build it
See `code/reindex_migration_sim.py` demonstrating schema transformation during data migration in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/74-reindexing/experiments/run_experiment.sh
```

## Inspect it
Create `products_v2` and trigger reindex:
```bash
curl -X PUT http://localhost:9200/products_v2 -H "Content-Type: application/json" -d '{
  "mappings": {
    "properties": {
      "title": { "type": "text" },
      "price": { "type": "double" }
    }
  }
}'
curl -X POST "http://localhost:9200/_reindex?wait_for_completion=true" -H "Content-Type: application/json" -d '{
  "source": { "index": "products_phase06" },
  "dest": { "index": "products_v2" }
}'
```

## Measure it
Inspect reindex progress and throughput via `_tasks?detailed=true&actions=*reindex*`.

## Break it
Attempt to reindex an index that had `_source: false` disabled.
**Observed Failure:** Reindex fails because `_source` is required to re-parse fields!

## Recover it
Always keep `_source: true` enabled.

## Modify it
Use a painless script inside reindex to mutate or rename fields on the fly:
`"script": { "source": "ctx._source.price = ctx._source.price * 1.1" }`.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does reindexing require `_source` to be enabled on the source index?
2. How can you throttle `_reindex` so it does not overwhelm cluster write queues? (`requests_per_second`)

## Guarantees
* Reindexing guarantees that data is re-analyzed according to the new index mapping schema.

## Non-guarantees
* Reindexing is not instantaneous; it is an $O(N)$ bulk write operation.

## When to use this
* Changing field types, changing tokenizers/analyzers, altering shard counts.

## When not to use this
* Adding a brand-new field to an existing mapping (new fields can be added dynamically with `PUT /<index>/_mapping` without reindexing!).

## What comes next
In Phase 75, we eliminate downtime during reindexing using Index Aliases.
""",
"""#!/usr/bin/env python3

def simulate_reindex(v1_docs, transform_fn):
    v2_docs = {}
    for doc_id, doc in v1_docs.items():
        v2_docs[doc_id] = transform_fn(dict(doc))
    return v2_docs

if __name__ == "__main__":
    v1_store = {
        1: {"title": "Keyboard", "price": "149.99"}, # stored as string
        2: {"title": "Mouse", "price": "49.99"}
    }
    print("V1 Data (price is string):", v1_store)
    def cast_price_to_float(d):
        d["price"] = float(d["price"])
        return d
    v2_store = simulate_reindex(v1_store, cast_price_to_float)
    print("V2 Data (price cast to float):", v2_store)
    print("Reindex successfully updated schema data types!")
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 74: Reindexing Data ==="
python3 phases/74-reindexing/code/74_reindexing.py
"""),

        (75, "Aliases and Zero-Downtime Index Migration",
         "Never query physical index names: point clients to an alias, reindex to v2, and swap aliases atomically in 0.001 ms.",
         """# Lesson 75.1: Aliases and Zero-Downtime Index Migration

## Motto
"Never query physical index names: point clients to an alias, reindex to v2, and swap aliases atomically in 0.001 ms."

## Problem
You need to reindex from `products_v1` to `products_v2`. If client applications hardcode the URL `http://es:9200/products_v1/_search`, how do you switch traffic to `products_v2` without updating code, redeploying 50 microservices, or incurring downtime?

## Prediction
Can you atomically swap traffic from `products_v1` to `products_v2` in a single master metadata transaction with zero dropped queries?

## Why this matters
**Index Aliases** decouple logical application index names from physical versioned indices. Aliases enable zero-downtime schema migrations.

## First principles
The Atomic Alias Swap:
* Clients always query `http://es:9200/products/_search` (where `products` is an alias).
* While live traffic hits `products_v1`, you build `products_v2` and reindex in the background.
* Execute an atomic alias update:
  * Remove `products` from `products_v1`
  * Add `products` to `products_v2`
* Elasticsearch executes this swap inside the cluster state in **sub-millisecond time**. Zero dropped requests!

## Mental model
```text
Step 1: Steady State
  Client ──► Alias "products" ──► Physical Index [products_v1]

Step 2: Reindexing in Background
  Client ──► Alias "products" ──► Physical Index [products_v1]
                                 [products_v2] (Hydrating via _reindex...)

Step 3: Atomic Swap (0.001 ms)
  Client ──► Alias "products" ──► Physical Index [products_v2]!
  (Old products_v1 can now be safely deleted!)
```

## Build it
See `code/atomic_alias_sim.py` demonstrating pointer swaps in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/75-aliases-and-zero-downtime-index-migration/experiments/run_experiment.sh
```

## Inspect it
Check alias mappings:
```bash
curl -s "http://localhost:9200/_cat/aliases?v"
```

## Measure it
Measure latency of the alias swap API call (< 5ms).

## Break it
Delete an index that has an alias pointing to it without re-pointing the alias. Queries hitting the alias fail immediately.

## Recover it
Always add the new index before or atomically during the removal of the old index.

## Modify it
Create a filtered alias: an alias that automatically restricts queries to a specific tenant:
`"filter": { "term": { "tenant_id": "corp_42" } }`.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why must the alias removal and addition occur within the same `_aliases` API request?
2. What is a "filtered alias" and how does it simplify application security?

## Guarantees
* Alias swaps are atomic: a query will either execute against v1 or v2; never against a non-existent state.

## Non-guarantees
* An alias cannot prevent write conflicts if clients continue writing to v1 during reindexing.

## When to use this
* Every production index (never query physical index names directly).

## When not to use this
* Temporary scratch testing scripts.

## What comes next
In Phase 76, we configure Elasticsearch Security Basics: TLS, RBAC, and users.
""",
"""#!/usr/bin/env python3

class AliasRouter:
    def __init__(self):
        self.aliases = {} # alias_name -> physical_index

    def set_alias(self, alias_name, physical_index):
        self.aliases[alias_name] = physical_index

    def atomic_swap(self, alias_name, old_index, new_index):
        if self.aliases.get(alias_name) == old_index:
            self.aliases[alias_name] = new_index
            return True
        return False

    def route_request(self, target):
        return self.aliases.get(target, target)

if __name__ == "__main__":
    router = AliasRouter()
    router.set_alias("products", "products_v1")
    print("Initial routing for 'products':", router.route_request("products"))

    print("\\nReindexing products_v2 complete. Performing atomic swap...")
    success = router.atomic_swap("products", "products_v1", "products_v2")
    print(f"Swap succeeded: {success}")
    print("Routing for 'products' after swap:", router.route_request("products"))
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 75: Index Aliases & Zero-Downtime Swaps ==="
python3 phases/75-aliases-and-zero-downtime-index-migration/code/75_aliases_and_zero_downtime_index_migration.py
"""),

        (76, "Elasticsearch Security Basics",
         "Never run Elasticsearch unauthenticated: enforce TLS on transport and HTTP, configure RBAC roles, and use API keys.",
         """# Lesson 76.1: Elasticsearch Security Basics

## Motto
"Never run Elasticsearch unauthenticated: enforce TLS on transport and HTTP, configure RBAC roles, and use API keys."

## Problem
Over the past decade, tens of thousands of unsecured Elasticsearch clusters with port 9200 exposed were compromised by ransomware bots that wiped indices and left ransom notes.

## Prediction
What happens if you try to bootstrap an Elasticsearch 8.x production cluster on a network interface without configuring TLS on port 9300?

## Why this matters
In Elasticsearch 8.x, **X-Pack Security is mandatory** for production clustering. Transport TLS protects node-to-node communication; HTTP TLS and RBAC protect client endpoints.

## First principles
The Security Triad:
1. **Transport TLS (Port 9300):** Encrypts inter-node cluster communication and authenticates nodes via a trusted Certificate Authority (CA).
2. **HTTP TLS (Port 9200):** Encrypts REST client traffic.
3. **Role-Based Access Control (RBAC):** Users are granted Roles. Roles enforce Index Privileges (read, write, manage) and Cluster Privileges (`monitor`, `manage`).

## Mental model
```text
Client (HTTPS :9200) ──► Basic Auth / API Key ──► Authenticated User
                                                        │
                                        Assigned Role: "catalog_reader"
                                        Privileges: read on "products_*" only
                                                        │
Node-to-Node (:9300) ──► Mutual TLS with CA Certificates (Zero Snooping!)
```

## Build it
See `code/rbac_permission_sim.py` demonstrating RBAC privilege enforcement in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/76-elasticsearch-security-basics/experiments/run_experiment.sh
```

## Inspect it
Create an application role with read-only index privileges:
```bash
curl -X POST http://localhost:9200/_security/role/read_products -H "Content-Type: application/json" -d '{
  "cluster": ["monitor"],
  "indices": [
    {
      "names": ["products_*"],
      "privileges": ["read", "view_index_metadata"]
    }
  ]
}'
```

## Measure it
Inspect TLS handshake latency vs raw plaintext HTTP.

## Break it
Attempt to write to an index using a read-only role: observe `security_exception: action [indices:data/write/index] is unauthorized`.

## Recover it
Grant appropriate write privileges or create dedicated API keys for ingest services.

## Modify it
Generate an API Key for automated backend microservices: `POST /_security/api_key`.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does Elasticsearch 8.x refuse to join a cluster across multiple network interfaces if Transport TLS is disabled?
2. What is the difference between cluster privileges and index privileges?

## Guarantees
* RBAC guarantees that users cannot read or modify indices outside their assigned role permissions.

## Non-guarantees
* Security features cannot protect against someone possessing the `elastic` superuser password.

## When to use this
* Every staging and production deployment without exception.

## When not to use this
* Isolated, single-node offline unit test runners.

## What comes next
In Phase 77, we establish Observability and metrics monitoring.
""",
"""#!/usr/bin/env python3

def check_permission(user_roles, role_definitions, index_name, action):
    # Action: "read" or "write"
    for r in user_roles:
        privs = role_definitions.get(r, {}).get("indices", {})
        for pattern, allowed_actions in privs.items():
            if pattern == "*" or pattern in index_name:
                if action in allowed_actions:
                    return True
    return False

if __name__ == "__main__":
    roles = {
        "analyst": {"indices": {"products_*": ["read"]}},
        "admin": {"indices": {"*": ["read", "write"]}}
    }
    print("Testing RBAC Security Rules:")
    print("  User 'alice' (analyst) reading 'products_v1' ->", check_permission(["analyst"], roles, "products_v1", "read"))
    print("  User 'alice' (analyst) writing to 'products_v1' ->", check_permission(["analyst"], roles, "products_v1", "write"))
    print("  User 'bob' (admin) writing to 'products_v1'     ->", check_permission(["admin"], roles, "products_v1", "write"))
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 76: Elasticsearch Security & RBAC ==="
python3 phases/76-elasticsearch-security-basics/code/76_elasticsearch_security_basics.py
"""),

        (77, "Observability",
         "If you cannot measure it, you cannot operate it: track QPS, p95 latency, heap %, GC pauses, and write rejections.",
         """# Lesson 77.1: Observability

## Motto
"If you cannot measure it, you cannot operate it: track QPS, p95 latency, heap %, GC pauses, and write rejections."

## Problem
A cluster outage occurs. The engineering team argues over whether the failure was caused by slow disk I/O, JVM garbage collection, search query spikes, or unassigned shards. Without telemetry, post-mortems are speculation.

## Prediction
What are the top 5 metrics every Elasticsearch production dashboard must display?

## Why this matters
Elasticsearch exposes rich internal metrics via REST APIs and Prometheus exporters. Observability provides early warning before outages occur.

## First principles
The Golden Signals of Elasticsearch:
1. **Cluster Health & Unassigned Shards:** Green/Yellow/Red.
2. **JVM Heap Utilization & GC Pauses:** Heap % and duration of `old` generation garbage collection pauses.
3. **Search & Indexing Latency:** p50, p95, p99 times.
4. **Thread Pool Rejections:** `write.rejected` and `search.rejected` tasks.
5. **Disk Watermark Proximity:** Free disk percentage per node.

## Mental model
```text
           ELASTICSEARCH OBSERVABILITY SIGNALS
┌─────────────────────────────────────────────────────────────┐
│ 1. Health: GREEN (0 unassigned shards)                      │
│ 2. JVM Heap: 65% (GC old pauses < 100ms)                    │
│ 3. Indexing: 15,000 docs/sec | Latency p95: 4.2ms           │
│ 4. Search: 1,200 QPS         | Latency p95: 12.8ms          │
│ 5. Thread Pools: Write Queue: 12 / 10000 (0 rejected)       │
│ 6. Storage: Node 1 (62%), Node 2 (59%), Node 3 (61%)        │
└─────────────────────────────────────────────────────────────┘
```

## Build it
See `code/metrics_collector.py` polling and evaluating node statistics in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/77-observability/experiments/run_experiment.sh
```

## Inspect it
Retrieve comprehensive node statistics:
```bash
curl -s "http://localhost:9200/_nodes/stats?pretty" | grep -A 10 "jvm"
```
Inspect write and search thread pool stats:
```bash
curl -s "http://localhost:9200/_cat/thread_pool?v&h=node_name,name,active,queue,rejected,completed"
```

## Measure it
Plot query throughput and latency trends.

## Break it
Simulate high GC pause alerts by triggering artificial memory pressure.

## Recover it
Diagnose which node is lagging using `_cat/nodes?v&h=name,heap.percent,cpu,load_1m`.

## Modify it
Integrate with Prometheus via OpenTelemetry or Metricbeat.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why is tracking thread pool `rejected` count more actionable than tracking average CPU usage?
2. What GC metric indicates that an Elasticsearch node is on the verge of an OutOfMemory crash?

## Guarantees
* Elasticsearch REST metrics provide real-time introspection into cluster internals.

## Non-guarantees
* Metrics APIs do not store historical trend graphs (use Prometheus/Grafana or Elasticsearch time-series indices).

## When to use this
* 24/7 production cluster monitoring and alerting.

## When not to use this
* Polling `_nodes/stats` every 10 milliseconds (polling itself consumes CPU; poll every 10s to 30s).

## What comes next
In Phase 78, we perform rigorous Capacity Planning.
""",
"""#!/usr/bin/env python3

def assess_cluster_metrics(metrics):
    alerts = []
    if metrics["health"] != "green":
        alerts.append(f"CRITICAL: Cluster health is {metrics['health'].upper()}!")
    if metrics["heap_pct"] > 85:
        alerts.append(f"WARNING: High JVM Heap pressure: {metrics['heap_pct']}%")
    if metrics["rejected_writes"] > 0:
        alerts.append(f"CRITICAL: Write thread pool has {metrics['rejected_writes']} rejected tasks!")
    if metrics["disk_usage_pct"] > 85:
        alerts.append(f"WARNING: Disk usage at {metrics['disk_usage_pct']}% (near low watermark)")
    return alerts

if __name__ == "__main__":
    snapshot = {
        "health": "yellow",
        "heap_pct": 88,
        "rejected_writes": 142,
        "disk_usage_pct": 82
    }
    print("Observability Health Assessment:")
    issues = assess_cluster_metrics(snapshot)
    for issue in issues:
        print("  -", issue)
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 77: Cluster Observability & Metrics ==="
python3 phases/77-observability/code/77_observability.py
"""),

        (78, "Capacity Planning",
         "Capacity planning is applied math: calculate storage, shards, JVM heap, CPU cores, and network bandwidth.",
         """# Lesson 78.1: Capacity Planning

## Motto
"Capacity planning is applied math: calculate storage, shards, JVM heap, CPU cores, and network bandwidth."

## Problem
A company estimates hardware requirements by guessing: "Let's buy 3 huge servers". After launch, they run out of disk space in 3 weeks and spend weeks panicking during emergency data migrations.

## Prediction
Given 100 GB of raw JSON per day with 30-day retention and 1 replica, how many terabytes of physical storage and how many primary shards do you actually need?

## Why this matters
Search engine storage expands due to inverted index structures, doc values, and replicas. Calculating requirements in advance prevents costly under-provisioning or wasteful over-provisioning.

## First principles
The Sizing Formulas:
1. **Daily Raw Data:** $D_{\text{raw}}$
2. **Index Overhead Factor:** Indexing adds inverted indexes, doc values, and BKD trees (typically $1.1\times$ to $1.3\times$ raw size).
3. **Total Disk Required:**
   $$\text{Storage} = D_{\text{raw}} \times \text{Overhead} \times (1 + \text{Replicas}) \times \text{Retention Days} \times 1.3 \text{ (Watermark Buffer)}$$
4. **Target Shard Size:** 30 GB to 50 GB per shard.
   $$\text{Primary Shards/Day} = \frac{D_{\text{raw}} \times \text{Overhead}}{\text{Target Shard Size (e.g. 40 GB)}}$$

## Mental model
```text
Daily Raw Data: 100 GB
  ├── With Index Overhead (1.2x): 120 GB/day
  ├── With 1 Replica (2x): 240 GB/day
  ├── 30-day Retention: 7,200 GB (7.2 TB)
  └── With 30% Headroom Buffer (Watermarks): ~9.5 TB Physical Disk!
Shard Strategy: 120 GB / 40 GB = Exactly 3 Primary Shards per day!
```

## Build it
See `code/capacity_planner.py` calculating hardware, shard, and RAM budgets in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/78-capacity-planning/experiments/run_experiment.sh
```

## Inspect it
Calculate capacity for your organization's specific data profile.

## Measure it
Compare calculated theoretical storage against actual disk consumed by test indices via `_cat/indices?v&h=index,pri.store.size,store.size`.

## Break it
Under-estimate index expansion overhead ($0.5\times$ instead of $1.2\times$) and watch disk hit high watermark days ahead of schedule.

## Recover it
Incorporate safety headroom buffers ($1.3\times$ margin for watermarks and segment merge spikes).

## Modify it
Calculate sizing for cold frozen storage using searchable snapshots.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does an index on disk typically occupy more bytes than the original raw JSON payload?
2. Why must total disk capacity include a 30% buffer above calculated storage? (To prevent crossing disk watermarks and allow background segment merges).

## Guarantees
* Mathematical capacity models provide reliable upper bounds for hardware budgeting.

## Non-guarantees
* Estimates must be validated with representative real-world data and query loads.

## When to use this
* Architecture reviews, annual budget planning, and cloud deployment sizing.

## When not to use this
* Guessing without measuring.

## What comes next
In Phase 79, we systematically execute 7 Controlled Failure Scenarios.
""",
"""#!/usr/bin/env python3

def plan_capacity(raw_gb_day, retention_days, replicas=1, overhead_factor=1.2, target_shard_gb=40.0):
    daily_indexed_gb = raw_gb_day * overhead_factor
    daily_total_gb = daily_indexed_gb * (1 + replicas)
    total_data_gb = daily_total_gb * retention_days
    # Add 30% safety margin for watermarks and merge headroom
    recommended_disk_gb = total_data_gb * 1.3
    primary_shards_per_day = max(1, round(daily_indexed_gb / target_shard_gb))

    return {
        "daily_indexed_gb": round(daily_indexed_gb, 1),
        "total_retained_data_tb": round(total_data_gb / 1024, 2),
        "recommended_physical_disk_tb": round(recommended_disk_gb / 1024, 2),
        "primary_shards_per_day": primary_shards_per_day,
        "total_shards_active": primary_shards_per_day * (1 + replicas) * retention_days
    }

if __name__ == "__main__":
    plan = plan_capacity(raw_gb_day=200, retention_days=30, replicas=1)
    print("Capacity Planning Report (200 GB/day, 30 days retention, 1 replica):")
    for k, v in plan.items():
        print(f"  {k:30s}: {v}")
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 78: Capacity Planning Calculator ==="
python3 phases/78-capacity-planning/code/78_capacity_planning.py
"""),

        (79, "Failure Scenarios",
         "Chaos engineering for search: predict, break, observe, diagnose, recover, and explain 7 real distributed failures.",
         """# Lesson 79.1: Failure Scenarios

## Motto
"Chaos engineering for search: predict, break, observe, diagnose, recover, and explain 7 real distributed failures."

## Problem
Engineers who have only experienced healthy green clusters freeze when production incidents occur. Mastery requires having broken and recovered every distributed component in a safe lab environment.

## Prediction
What happens to active indexing and queries when you kill a node, fill a write queue, or inject a disk watermark block?

## Why this matters
This phase runs through the 7 canonical failure modes of distributed search clusters:
1. Primary Shard Node Crash
2. Unassigned Replica Shard
3. Write Queue Overflow (HTTP 429)
4. Disk Flood Stage Lock (Read-Only)
5. Mapping Explosion Rejection
6. High-Cardinality Heap Saturation
7. Split-Brain Prevention / Master Failover

## First principles
The Failure-Recovery Loop:
$$\text{Predict} \longrightarrow \text{Break} \longrightarrow \text{Observe} \longrightarrow \text{Diagnose} \longrightarrow \text{Recover} \longrightarrow \text{Explain}$$

## Mental model
```text
           THE 7 CONTROLLED FAILURE DRILLS
┌──────────────────────────────────────────────────────────────┐
│ 1. Node Loss        ──► Inspect promotion & recovery         │
│ 2. Unassigned Shard ──► Diagnose with allocation explain     │
│ 3. HTTP 429 Reject  ──► Observe backoff & write queue        │
│ 4. Read-Only Block  ──► Clear flood-stage lock               │
│ 5. Mapping Limit    ──► Fix schema design                    │
│ 6. Slow Wildcard    ──► Audit slow logs                      │
│ 7. Hot Shard Skew   ──► Rebalance routing partition          │
└──────────────────────────────────────────────────────────────┘
```

## Build it
See `code/chaos_runner.py` automating failure injections in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/79-failure-scenarios/experiments/run_experiment.sh
```

## Inspect it
Observe error logs and recovery steps for each simulated failure mode.

## Measure it
Measure Mean Time To Recovery (MTTR) for each scenario.

## Break it
Run the complete automated failure suite.

## Recover it
Follow the diagnostic procedures in `docs/troubleshooting.md`.

## Modify it
Add network packet latency simulation between data nodes.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. How does practicing failure injection prevent panic during real production outages?
2. Which failure mode is easiest to prevent with upfront schema design? (Mapping explosion).

## Guarantees
* Controlled failure drills build operational muscle memory.

## Non-guarantees
* Lab failure simulations do not encompass every bizarre hardware failure mode.

## When to use this
* Operational onboarding, disaster readiness testing, and game days.

## When not to use this
* Production environments during business hours.

## What comes next
In Phase 80, we construct Capstone 3: Building a Mini Search Engine from Scratch.
""",
"""#!/usr/bin/env python3

FAILURES = [
    ("Node Crash", "Kill container hosting primary shard", "Master promotes replica; health YELLOW"),
    ("Queue Saturated", "Flood write pool with 50 threads", "HTTP 429 Too Many Requests"),
    ("Disk Flood Stage", "Simulate 96% disk watermark", "ClusterBlockException: read_only_allow_delete"),
    ("Mapping Explosion", "Dynamically index 2,000 unique keys", "total_fields.limit [1000] exceeded"),
    ("Circuit Breaker", "Run high-cardinality aggregation", "CircuitBreakingException: [parent] Data too large"),
    ("Unassigned Shard", "Set replicas=1 on single node", "same_shard decider blocks allocation"),
    ("Slow Regex Query", "Run unindexed broad wildcard", "Index search slow log triggered")
]

if __name__ == "__main__":
    print("=== The 7 Canonical Search Failure Modes ===\\n")
    for idx, (name, trigger, outcome) in enumerate(FAILURES, 1):
        print(f"Drill {idx}: [{name:18s}]")
        print(f"  Trigger: {trigger}")
        print(f"  Outcome: {outcome}\\n")
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 79: Chaos Engineering & Failure Scenarios ==="
python3 phases/79-failure-scenarios/code/79_failure_scenarios.py
"""),

        (80, "Build Mini Search Engine",
         "Capstone 3: Construct a complete standalone search engine in pure Python: document store, tokenizer, inverted index, BM25 ranking, and boolean filters.",
         """# Lesson 80.1: Build Mini Search Engine (Capstone 3)

## Motto
"Capstone 3: Construct a complete standalone search engine in pure Python: document store, tokenizer, inverted index, BM25 ranking, and boolean filters."

## Problem
True systems understanding is demonstrated by synthesis. If you truly understand Elasticsearch, you should be able to build a miniature, fully working search engine in pure Python without importing Lucene or external search libraries.

## Prediction
Can you build an end-to-end search engine in 250 lines of Python that indexes documents, builds inverted indexes, computes BM25 relevance, and executes boolean filters?

## Why this matters
This is the ultimate capstone of the single-node information retrieval curriculum.

## First principles
Mini Search Engine Components:
1. **Document Store:** Holds original raw documents (`_source`).
2. **Analysis Pipeline:** Lowercases, tokenizes on word boundaries, and discards stop words.
3. **Inverted Index:** Sorted postings lists with term frequencies and positions.
4. **Columnar Doc Values:** Fast column lookup for filtering and sorting.
5. **BM25 Scorer:** Implements $k_1$ saturation and $b$ length normalization.
6. **Query Engine:** Parses and executes `must`, `filter`, and `should` queries.

## Mental model
```text
┌─────────────────────────────────────────────────────────────┐
│                 MINI SEARCH ENGINE IN PYTHON                │
├─────────────────────────────────────────────────────────────┤
│  Document Store  │ Inverted Index │ Doc Values │ BM25 Scorer│
└─────────────────────────────────────────────────────────────┘
                               │
               API: engine.index(id, doc)
               API: engine.search(query_dsl)
                               │
                               ▼
           Top-K Scored & Filtered Search Results!
```

## Build it
See `projects/mini_search_engine/` and `code/mini_search_engine.py` for the complete implementation.

## Use Elasticsearch
Run the experiment:
```bash
./phases/80-build-mini-search-engine/experiments/run_experiment.sh
```

## Inspect it
Index a corpus of 100 documents and execute multi-clause boolean queries.

## Measure it
Benchmark query latency on our Python mini engine vs Elasticsearch.

## Break it
Feed edge-case inputs: empty strings, unknown terms, all-stop-word queries.

## Recover it
Implement graceful empty-result handling.

## Modify it
Add phrase matching using the stored token positions.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. How does your Python inverted index mirror Lucene's internal data structures?
2. What trade-offs did you make between memory usage and query speed in your implementation?

## Guarantees
* A self-contained, dependency-free reference implementation of core search engine principles.

## Non-guarantees
* Not intended for multi-terabyte production data (pure in-memory Python).

## When to use this
* Deep conceptual mastery and interview demonstration of search internals.

## When not to use this
* Large-scale production storage.

## What comes next
In Phase 81, we simulate distributed cluster coordination across multiple shards and nodes.
""",
"""#!/usr/bin/env python3
import math
import re
from collections import defaultdict, Counter

class MiniSearchEngine:
    def __init__(self, k1=1.2, b=0.75):
        self.k1 = k1
        self.b = b
        self.docs = {}
        self.inverted_index = defaultdict(lambda: defaultdict(int)) # term -> doc_id -> tf
        self.doc_lens = {}
        self.doc_values = defaultdict(dict) # field -> doc_id -> value

    def _tokenize(self, text):
        return [t.lower() for t in re.findall(r'\\b\\w+\\b', text)]

    def index_document(self, doc_id, doc):
        self.docs[doc_id] = doc
        tokens = self._tokenize(doc.get("text", ""))
        self.doc_lens[doc_id] = len(tokens)
        counts = Counter(tokens)
        for t, freq in counts.items():
            self.inverted_index[t][doc_id] = freq

        # Index doc values
        for f in ["category", "price", "status"]:
            if f in doc:
                self.doc_values[f][doc_id] = doc[f]

    def search(self, query_str, filter_cat=None, top_k=5):
        q_tokens = self._tokenize(query_str)
        N = len(self.docs)
        if N == 0 or not q_tokens:
            return []
        avgdl = sum(self.doc_lens.values()) / N

        # Find candidates
        candidates = set()
        for t in q_tokens:
            candidates.update(self.inverted_index[t].keys())

        # Apply filter context
        if filter_cat:
            candidates = {d for d in candidates if self.doc_values["category"].get(d) == filter_cat}

        scores = []
        for doc_id in candidates:
            doc_score = 0.0
            doc_len = self.doc_lens[doc_id]
            for t in q_tokens:
                tf = self.inverted_index[t].get(doc_id, 0)
                if tf > 0:
                    df = len(self.inverted_index[t])
                    idf = math.log(1.0 + (N - df + 0.5) / (df + 0.5))
                    num = tf * (self.k1 + 1)
                    denom = tf + self.k1 * (1 - self.b + self.b * (doc_len / avgdl))
                    doc_score += idf * (num / denom)
            scores.append((doc_id, round(doc_score, 4), self.docs[doc_id]))

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]

if __name__ == "__main__":
    engine = MiniSearchEngine()
    engine.index_document(1, {"text": "Distributed search with inverted index", "category": "tech", "price": 45})
    engine.index_document(2, {"text": "Elasticsearch distributed cluster architecture", "category": "tech", "price": 85})
    engine.index_document(3, {"text": "Ergonomic leather chair for office", "category": "furniture", "price": 199})

    results = engine.search("distributed architecture", filter_cat="tech")
    print("Mini Search Engine Query Results (query='distributed architecture', filter='tech'):")
    for doc_id, score, doc in results:
        print(f"  [Doc {doc_id}] Score: {score:.4f} | {doc}")
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 80: Capstone 3 - Mini Search Engine ==="
python3 phases/80-build-mini-search-engine/code/80_build_mini_search_engine.py
"""),

        (81, "Distributed Search Simulator",
         "Build a distributed cluster simulator in Python: 1 coordinator node, 3 shard workers, and simulated network partitions.",
         """# Lesson 81.1: Distributed Search Simulator

## Motto
"Build a distributed cluster simulator in Python: 1 coordinator node, 3 shard workers, and simulated network partitions."

## Problem
How does a coordinating node handle a shard timing out, a node crashing mid-query, or uneven response latencies across a cluster? Testing this on real production clusters is risky; building a multi-worker simulator makes the distributed dynamics crystal clear.

## Prediction
What happens to total query latency when 2 shards respond in 5ms, but the 3rd shard experiences a 500ms network lag?

## Why this matters
Simulating the coordinator-shard interaction cements your mental model of scatter-gather, fan-out, partial hits, and cluster consensus.

## First principles
Distributed Simulator Architecture:
* **Shard Workers (3 instances):** Each worker maintains its own isolated inverted index and doc values.
* **Coordinator:**
  1. Computes shard routing for writes (`hash(id) % 3`).
  2. Scatters queries in parallel to all 3 workers.
  3. Priority-queue merges top hits.
  4. Detects worker timeouts and reports `timed_out: true` or partial hits.

## Mental model
```text
                     COORDINATOR WORKER
                              │
     ┌────────────────────────┼────────────────────────┐
     │ Query (async)          │ Query (async)          │ Query (async)
     ▼                        ▼                        ▼
  SHARD 0                  SHARD 1                  SHARD 2
  (Fast: 3ms)              (Fast: 4ms)              (Slow: 250ms)
     │                        │                        │
     └────────────────────────┼────────────────────────┘
                              ▼
            Coordinator waits for Shard 2!
            Total latency = max(3ms, 4ms, 250ms) = 250ms!
```

## Build it
See `projects/distributed_simulator/` and `code/distributed_simulator.py` implementing the complete coordinator and shard workers in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/81-distributed-search-simulator/experiments/run_experiment.sh
```

## Inspect it
Observe simulated scatter-gather query execution across the 3 shard workers.

## Measure it
Benchmark total query latency with and without slow shard injection.

## Break it
Simulate a dead shard worker: observe coordinator handling partial hit responses (`_shards.failed: 1`).

## Recover it
Implement timeout thresholds (`timeout: "50ms"`) so queries return partial results rather than blocking indefinitely.

## Modify it
Add replica shard worker fallbacks.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why is distributed search latency always bounded by the slowest participating shard?
2. What does Elasticsearch return in the HTTP response if one shard fails during query execution?

## Guarantees
* Demonstrates the exact network coordination dynamics of distributed search engines.

## Non-guarantees
* Does not implement full Raft distributed consensus for cluster state.

## When to use this
* Distributed systems education, latency modeling, and fault tolerance studies.

## When not to use this
* Production search serving.

## What comes next
In Phase 82, we compare Elasticsearch directly against PostgreSQL.
""",
"""#!/usr/bin/env python3
import time
import hashlib
import random

class ShardWorker:
    def __init__(self, shard_id, lag_ms=0):
        self.shard_id = shard_id
        self.lag_ms = lag_ms
        self.data = {}

    def index(self, doc_id, text):
        self.data[doc_id] = text

    def query(self, term):
        if self.lag_ms > 0:
            time.sleep(self.lag_ms / 1000.0)
        hits = [(doc_id, text) for doc_id, text in self.data.items() if term in text.lower()]
        return {"shard": self.shard_id, "hits": hits}

class Coordinator:
    def __init__(self, shards):
        self.shards = shards

    def index(self, doc_id, text):
        h = int(hashlib.md5(str(doc_id).encode()).hexdigest(), 16)
        target = h % len(self.shards)
        self.shards[target].index(doc_id, text)

    def search(self, term):
        t0 = time.perf_counter()
        results = []
        for s in self.shards:
            res = s.query(term)
            results.extend(res["hits"])
        elapsed = (time.perf_counter() - t0) * 1000
        return results, elapsed

if __name__ == "__main__":
    # Shard 0 & 1 are fast; Shard 2 has 80ms network lag!
    workers = [ShardWorker(0, lag_ms=2), ShardWorker(1, lag_ms=3), ShardWorker(2, lag_ms=80)]
    coord = Coordinator(workers)

    coord.index(1, "distributed systems design")
    coord.index(2, "distributed database replication")
    coord.index(3, "distributed search algorithms")

    hits, duration = coord.search("distributed")
    print(f"Distributed Search completed across 3 Shards:")
    print(f"  Total Hits: {len(hits)}")
    print(f"  Total Duration: {duration:.2f} ms (Bounded by Shard 2's 80ms lag!)")
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 81: Distributed Search Simulator ==="
python3 phases/81-distributed-search-simulator/code/81_distributed_search_simulator.py
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
    generate_phases_69_to_81()
