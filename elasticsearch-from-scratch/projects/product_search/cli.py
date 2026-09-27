#!/usr/bin/env python3
"""
projects/product_search/cli.py - Capstone 1 E-Commerce Search CLI.
Supports loading data, search with filters & facets, and autocomplete.
"""

import json
import os
import sys
import urllib.request
import urllib.error

ES_HOST = os.environ.get("ES_URL", "http://localhost:9200")
INDEX_NAME = "ecommerce_catalog"
DIR = os.path.dirname(os.path.abspath(__file__))

def http_request(path, method="GET", data=None):
    url = f"{ES_HOST}{path}"
    headers = {"Content-Type": "application/json"}
    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8")
        print(f"HTTP Error {e.code} on {method} {url}: {err}", file=sys.stderr)
        return None

def init_index():
    print(f"Creating index '{INDEX_NAME}' with custom analyzers and schema...")
    http_request(f"/{INDEX_NAME}", method="DELETE")
    with open(os.path.join(DIR, "schema.json"), "r") as f:
        schema = json.load(f)
    resp = http_request(f"/{INDEX_NAME}", method="PUT", data=schema)
    print("Index creation response:", resp)

def seed_catalog():
    print("Loading catalog data...")
    with open(os.path.join(DIR, "catalog.json"), "r") as f:
        items = json.load(f)
    bulk_lines = []
    for item in items:
        bulk_lines.append(json.dumps({"index": {"_index": INDEX_NAME, "_id": item["id"]}}))
        bulk_lines.append(json.dumps(item))
    payload = "\n".join(bulk_lines) + "\n"
    
    url = f"{ES_HOST}/_bulk?refresh=true"
    req = urllib.request.Request(url, data=payload.encode("utf-8"), headers={"Content-Type": "application/x-ndjson"}, method="POST")
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        print(f"Bulk indexed {len(items)} products. Errors: {res.get('errors')}")

def search(query=None, category=None, max_price=None, in_stock_only=False):
    must = []
    if query:
        must.append({
            "multi_match": {
                "query": query,
                "fields": ["title^3", "description", "brand^2"],
                "fuzziness": "AUTO"
            }
        })
    else:
        must.append({"match_all": {}})

    filters = []
    if category:
        filters.append({"term": {"category": category}})
    if max_price:
        filters.append({"range": {"price": {"lte": float(max_price)}}})
    if in_stock_only:
        filters.append({"term": {"in_stock": True}})

    dsl = {
        "size": 10,
        "query": {
            "bool": {
                "must": must,
                "filter": filters
            }
        },
        "aggs": {
            "categories": {"terms": {"field": "category"}},
            "brands": {"terms": {"field": "brand"}},
            "price_stats": {"stats": {"field": "price"}}
        }
    }

    res = http_request(f"/{INDEX_NAME}/_search", method="POST", data=dsl)
    if not res:
        return

    hits = res.get("hits", {}).get("hits", [])
    print(f"\nSearch Results (Found {len(hits)} hits):")
    print(f"{'Title':45s} | {'Brand':12s} | {'Price':8s} | {'Score':6s}")
    print("-" * 80)
    for h in hits:
        src = h["_source"]
        print(f"{src['title'][:44]:45s} | {src['brand'][:11]:12s} | ${src['price']:7.2f} | {h['_score']:6.2f}")

    aggs = res.get("aggregations", {})
    print("\nFacet Counts (Categories):")
    for b in aggs.get("categories", {}).get("buckets", []):
        print(f"  - {b['key']}: {b['doc_count']} items")

def autocomplete(prefix):
    dsl = {
        "size": 5,
        "query": {
            "match": {
                "title.autocomplete": {
                    "query": prefix
                }
            }
        }
    }
    res = http_request(f"/{INDEX_NAME}/_search", method="POST", data=dsl)
    if not res:
        return
    hits = res.get("hits", {}).get("hits", [])
    print(f"\nAutocomplete Suggestions for prefix '{prefix}':")
    for h in hits:
        print(f"  * {h['_source']['title']}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 cli.py [init|seed|search <q>|suggest <prefix>]")
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "init":
        init_index()
    elif cmd == "seed":
        seed_catalog()
    elif cmd == "search":
        q = sys.argv[2] if len(sys.argv) > 2 else None
        search(query=q)
    elif cmd == "suggest":
        prefix = sys.argv[2] if len(sys.argv) > 2 else "wire"
        autocomplete(prefix)
