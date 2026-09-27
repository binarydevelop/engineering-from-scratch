#!/usr/bin/env python3
from collections import defaultdict

def build_nested_aggs(items):
    # Category -> Brand -> list of prices
    tree = defaultdict(lambda: defaultdict(list))
    for it in items:
        tree[it["category"]][it["brand"]].append(it["price"])

    results = {}
    for cat, brands in tree.items():
        results[cat] = {"brands": {}}
        for brand, prices in brands.items():
            results[cat]["brands"][brand] = {
                "count": len(prices),
                "avg_price": round(sum(prices) / len(prices), 2)
            }
    return results

if __name__ == "__main__":
    catalog = [
        {"category": "tech", "brand": "apple", "price": 1200},
        {"category": "tech", "brand": "apple", "price": 800},
        {"category": "tech", "brand": "sony", "price": 400},
        {"category": "home", "brand": "ikea", "price": 150},
        {"category": "home", "brand": "ikea", "price": 250}
    ]
    report = build_nested_aggs(catalog)
    print("Nested Aggregation Tree:")
    for cat, data in report.items():
        print(f"[{cat.upper()}]")
        for b, stats in data["brands"].items():
            print(f"  └── Brand '{b}': count={stats['count']}, avg_price=${stats['avg_price']}")
