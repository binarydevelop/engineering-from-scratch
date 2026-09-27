#!/usr/bin/env python3

def boolean_search(docs, must_terms=None, filter_fn=None, should_terms=None, must_not_terms=None):
    must_terms = must_terms or []
    should_terms = should_terms or []
    must_not_terms = must_not_terms or []
    results = []

    for doc_id, doc in docs.items():
        text = doc.get("text", "").lower()
        # 1. Check must_not
        if any(term in text for term in must_not_terms):
            continue
        # 2. Check must
        if not all(term in text for term in must_terms):
            continue
        # 3. Check filter
        if filter_fn and not filter_fn(doc):
            continue
        # 4. Calculate score (must + should boosts)
        score = len(must_terms) * 1.0
        for st in should_terms:
            if st in text:
                score += 1.5
        results.append((doc_id, score, doc))

    results.sort(key=lambda x: x[1], reverse=True)
    return results

if __name__ == "__main__":
    catalog = {
        1: {"text": "mechanical wireless keyboard", "price": 120},
        2: {"text": "membrane quiet keyboard", "price": 40},
        3: {"text": "refurbished mechanical keyboard", "price": 70},
        4: {"text": "ergonomic wireless mouse", "price": 60}
    }
    hits = boolean_search(
        catalog,
        must_terms=["keyboard"],
        filter_fn=lambda d: d["price"] <= 130,
        should_terms=["mechanical"],
        must_not_terms=["refurbished"]
    )
    print("Boolean Search Results:")
    for doc_id, score, doc in hits:
        print(f"  Doc {doc_id} (Score: {score:.1f}): {doc}")
