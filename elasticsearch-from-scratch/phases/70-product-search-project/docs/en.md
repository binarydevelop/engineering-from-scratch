# Lesson 70.1: Product Search Project (Capstone 1)

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
