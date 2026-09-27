#!/usr/bin/env python3
from collections import defaultdict

def run_aggregations(docs, query_fn=None):
    category_counts = defaultdict(int)
    category_prices = defaultdict(list)

    for doc in docs:
        if query_fn and not query_fn(doc):
            continue
        cat = doc.get("category", "unknown")
        category_counts[cat] += 1
        category_prices[cat].append(doc.get("price", 0.0))

    summary = {}
    for cat, count in category_counts.items():
        prices = category_prices[cat]
        summary[cat] = {
            "doc_count": count,
            "avg_price": round(sum(prices) / count, 2),
            "max_price": max(prices)
        }
    return summary

if __name__ == "__main__":
    catalog = [
        {"title": "Keyboard", "category": "electronics", "price": 100},
        {"title": "Mouse", "category": "electronics", "price": 50},
        {"title": "Monitor", "category": "electronics", "price": 300},
        {"title": "Chair", "category": "furniture", "price": 200},
        {"title": "Desk", "category": "furniture", "price": 400}
    ]
    print("Aggregation Summary (Category Facets):")
    aggs = run_aggregations(catalog)
    for cat, data in aggs.items():
        print(f"  Category '{cat}': Count={data['doc_count']}, AvgPrice=${data['avg_price']}, MaxPrice=${data['max_price']}")
