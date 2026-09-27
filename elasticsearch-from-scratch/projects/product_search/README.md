# Capstone 1: E-Commerce Product Search

A production-grade e-commerce catalog search implementation in Elasticsearch 8.17.0.

---

## 1. Features
* **Full-Text Multi-Match:** Queries across `title^3`, `brand^2`, and `description` with BM25 relevance scoring.
* **Autocomplete & Search-as-You-Type:** Edge N-Gram token analysis (`autocomplete` multi-field) for sub-10ms prefix suggestions.
* **Typo Resilience:** Dynamic Levenshtein edit distance (`fuzziness: "AUTO"`) with `prefix_length: 2`.
* **Faceted Navigation:** Dynamic bucket aggregations across `category` and `brand` with statistical price summaries.
* **Filtered Context:** Cached binary filters for `category`, `in_stock`, and numeric price range queries.

---

## 2. Usage Instructions

```bash
# 1. Initialize Index with Custom Analyzers & Mappings
python3 projects/product_search/cli.py init

# 2. Seed Sample Product Catalog Data
python3 projects/product_search/cli.py seed

# 3. Execute Relevance Search with Facets
python3 projects/product_search/cli.py search "wireless keyboard"

# 4. Execute Prefix Autocomplete Suggestions
python3 projects/product_search/cli.py suggest "logi"
```
